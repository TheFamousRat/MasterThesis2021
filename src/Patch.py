import os
import math
import numpy as np
import scipy.linalg as la
import itertools
import ctypes

import bpy
import mathutils

from PIL import Image
from numpy.lib.function_base import angle
from scipy.spatial.distance import cdist

import debugDrawing

class Patch:
    ##Static constants
    #Related to texture baking
    uvLayerName = "tempProj"
    bakedImgName = "bakedImage"
    bakedImgSize = 16
    imageNodeName = "BakedTextureNode"
    uvLayerNodeName = "BakedUVLayerNode"
    uvExclusionPoint = np.array([2.0, 2.0]) #Location where the UV not to be used are isolated
    textureMargin = 1
    #Related to patch sampling
    planeScale = 0.05
    sampleRes = 16

    def __init__(self, bmeshObj, centerVertexIdx, ringsNum):
        #Creates a patch, built from a central vertex and its ringsNum neighbouring rings
        self.centerVertexIdx = centerVertexIdx
        self.facesCounts = 0

        self.rings = []
        self.rings.append([face.index for face in bmeshObj.verts[self.centerVertexIdx].link_faces]) #Ring one, based on the central vertex's neighbourhood

        for i in range(1,ringsNum):
            self.rings.append([])
            for prevRingFaceIdx in self.rings[-2]:
                for vert in bmeshObj.faces[prevRingFaceIdx].verts:
                    for linkedFace in vert.link_faces:
                        #We check the neighbouring face isn't in the 2 previous rings, as well as the current one
                        cond = linkedFace.index in self.rings[-2] or linkedFace.index in self.rings[-1]
                        if len(self.rings) > 2:
                            cond = cond or (linkedFace.index in self.rings[-3])
                        
                        #Adding the face to the ring
                        if not cond:
                            self.rings[-1].append(linkedFace.index)
                            self.facesCounts += 1

        self.verticesIdxList = set()
        for faceIdx in self.getFacesIdxIterator():
            for vert in bmeshObj.faces[faceIdx].verts:
                self.verticesIdxList.add(vert.index)
        self.verticesIdxList = np.array(list(self.verticesIdxList))

        self.pixels = []

        self.calculateIndicators(bmeshObj)

    def calculateIndicators(self, bmeshObj):
        """
        Syntaxic sugar to (re-)calculate the geometric descriptors of the patch
        """
        self.calculateTotalArea(bmeshObj)
        self.calculateBarycenter(bmeshObj)
        self.calculateFaceWeights(bmeshObj)
        self.calculatePatchEigenValues(bmeshObj)
        #self.samplePatchNormals(bmeshObj)

    def calculateTotalArea(self, bmeshObj):
        """
        Calculates the sum of areas of the triangles of the patch
        """
        self.totalArea = 0.0
        for faceIdx in self.getFacesIdxIterator():
            self.totalArea += bmeshObj.faces[faceIdx].calc_area()

    def calculateBarycenter(self, bmeshObj):
        """
        Calculates the barycenter of the patch by averaging local vertex positions
        """
        self.barycenter = np.array([0.0, 0.0, 0.0])
        verticesSet = self.verticesIdxList

        for vertexIdx in verticesSet:
            self.barycenter += np.array(bmeshObj.verts[vertexIdx].co)

        self.barycenter /= len(verticesSet)

    def calculateFaceWeights(self, bmeshObj):
        self.faceWeights = {}

        #Computing some constant values for tensor voting
        maxFaceSize = 0.0
        facesBarycenters = {}
        facesDists = {}
        centralPos = self.getCentralPos(bmeshObj)

        for faceIdx in self.getFacesIdxIterator():
            #Calculating the max face area, to normalize face areas later
            maxFaceSize = max(maxFaceSize, bmeshObj.faces[faceIdx].calc_area())
            #Baking faces barycenters
            facesBarycenters[faceIdx] = self.getFaceBarycenter(bmeshObj.faces[faceIdx])
            #Finding the largest distance between the central face and a triangle barycenter
            facesDists[faceIdx] = np.linalg.norm(facesBarycenters[faceIdx] - centralPos)

        sigma = max(facesDists.values()) / 3.0

        for faceIdx in self.getFacesIdxIterator():
            self.faceWeights[faceIdx] = (bmeshObj.faces[faceIdx].calc_area() / maxFaceSize) * math.exp(-facesDists[faceIdx]/sigma)

    def calculatePatchEigenValues(self, bmeshObj):
        #Extracting the eigenvalues from the patch's normals' correlation matrix. Used to compare patches between each other
        normalsCovMat = np.zeros((3,3))

        #Normal tensor voting
        for faceIdx in self.getFacesIdxIterator():
            normalVec = bmeshObj.faces[faceIdx].normal
            normalVec = normalVec / np.linalg.norm(normalVec)
            faceNormal = np.matrix(np.array(normalVec)).T #Transforming the face normal into a vector
            normalsCovMat += (faceNormal @ faceNormal.T) * self.faceWeights[faceIdx]

        #Extracting the orthogonal directions from the tensor
        #The signs of the eigenvectors are unreliable here and will be corrected
        self.eigenVals, self.eigenVecs = la.eigh(normalsCovMat)

        #Implementing a proposition by Sheng Ao et al. 2019 "A repeatable and robust local reference frame for 3D surface matching"
        #Correcting the z-axis (normal)
        h2 = 0.0
        for faceIdx in self.getFacesIdxIterator():
            face = bmeshObj.faces[faceIdx]
            h2 += self.faceWeights[faceIdx] * np.dot(face.normal, self.eigenVecs[:,2])

        self.eigenVecs[:,2] = self.eigenVecs[:,2] * np.sign(h2)
        #Correcting the x-axis

        #Finally get the y-axis with the other two corrected vectors
        self.eigenVecs[:,1] = -np.cross(self.eigenVecs[:,0], self.eigenVecs[:,2])

        self.rotMatInv = np.linalg.inv(self.eigenVecs)
    
    def getFacesIdxIterator(self):
        """
        Returns an iterator to iterate over all faces of the patch in one loop
        """
        return itertools.chain.from_iterable(self.rings)

    def getVerticesPos(self, bmeshObj):
        """
        Returns the local translation of the patch's vertices
        """
        vertsIdxSet = self.verticesIdxList
        return np.array([bmeshObj.verts[vertIdx].co for vertIdx in vertsIdxSet])

    def getEdgesIdx(self, bmeshObj):
        """
        Returns a list of the indices of edges contained within the patch
        """
        ret = set()
        for faceIdx in self.getFacesIdxIterator():
            for edge in bmeshObj.faces[faceIdx].edges:
                ret.add(edge.index)
        return ret

    def getCentralPos(self, bmeshObj):
        return np.array(bmeshObj.verts[self.centerVertexIdx].co)

    def getFaceBarycenter(self, face):
        return np.array(face.calc_center_median())

    def calculateFaceNormal(self, face):
        n = np.cross(face.verts[0].co - face.verts[1].co, face.verts[1].co - face.verts[2].co)
        return n / np.linalg.norm(n)

    def computeCurvatureTensor(self, bmeshObj):
        curvatureTensor = np.zeros((3,3))
        edgesSet = self.getEdgesIdx(bmeshObj)

        for edgeIdx in edgesSet:
            edge = bmeshObj.edges[edgeIdx]
            edgeDir = np.array(edge.verts[0].co - edge.verts[1].co)
            edgeDir = np.matrix(edgeDir / np.linalg.norm(edgeDir)).T
            curvatureTensor += edge.calc_length() * edge.calc_face_angle_signed() * (edgeDir @ edgeDir.T)

        curvatureTensor /= self.totalArea

        return curvatureTensor

    def getVertUV(self, bmeshObj, vertIdx, uvLayerName):
        """
        Finds the UV coordinates of a vertex from the patch, by returning the first uv from a loop contained within the patch
        """
        vert = bmeshObj.verts[vertIdx]
        facesList = list(self.getFacesIdxIterator())
        for loop in vert.link_loops:
            if loop.face.index in facesList:
                return loop[bmeshObj.loops.layers.uv[uvLayerName]].uv
        return None

    def setVertUV(self, bmeshObj, vertIdx, uvLayerName, newPos):
        """
        Set the uv to the correct position for every loop of the patch containing it
        """
        vert = bmeshObj.verts[vertIdx]
        facesList = list(self.getFacesIdxIterator())
        for loop in vert.link_loops:
            if loop.face.index in facesList:
                loop[bmeshObj.loops.layers.uv[uvLayerName]].uv = newPos

    @staticmethod
    def setupBakingEnvironment(bmeshObj):
        prevRenderEngine = bpy.context.scene.render.engine
        bpy.context.scene.render.engine = 'CYCLES'

        selecObj = bpy.context.active_object
        #Creating a temporary UV layer
        if not Patch.uvLayerName in selecObj.data.uv_layers:
            selecObj.data.uv_layers.new(name = Patch.uvLayerName)
        
        uvLayer = selecObj.data.uv_layers[Patch.uvLayerName] 
        if not uvLayer.active:
            uvLayer.active = True

        #Creating an image to bake to
        if not Patch.bakedImgName in bpy.data.images:
            bpy.data.images.new(Patch.bakedImgName, Patch.bakedImgSize, Patch.bakedImgSize)
        bpy.data.images[Patch.bakedImgName].source = 'GENERATED'
        bpy.data.images[Patch.bakedImgName].scale(Patch.bakedImgSize, Patch.bakedImgSize)
            
        #Preparing the shaders for baking if they aren't already
        for mat in selecObj.data.materials:
            nodeTree = mat.node_tree #shorthand
            #Preparing the image node
            if not Patch.imageNodeName in mat.node_tree.nodes:
                nodeTree.nodes.new("ShaderNodeTexImage").name = Patch.imageNodeName
                
            imageNode = nodeTree.nodes[Patch.imageNodeName]
            imageNode.location = np.array([0.0, 0.0])
            imageNode.image = bpy.data.images[Patch.bakedImgName]
                
            #Preparing the UV node
            if not Patch.uvLayerNodeName in nodeTree.nodes:
                newNode = nodeTree.nodes.new("ShaderNodeUVMap")
                newNode.name = Patch.uvLayerNodeName
            
            uvNode = nodeTree.nodes[Patch.uvLayerNodeName]
            uvNode.location = np.array(imageNode.location) - np.array([200.0,0.0])
            uvNode.uv_map = Patch.uvLayerName
            
            #Connecting the nodes (if necessary)
            if len(imageNode.inputs['Vector'].links) == 0:
                nodeTree.links.new(uvNode.outputs['UV'], imageNode.inputs[0])
                
            #Setting the Image texture one as the active
            nodeTree.nodes.active = imageNode
            
        #Unselecting every faces
        for face in bmeshObj.faces:
            face.select = False

        #'Resetting' the UV map by putting all UV is a far away corner... Dirty but works !
        for vert in bmeshObj.verts:
            for loop in vert.link_loops:
                loop[bmeshObj.loops.layers.uv[Patch.uvLayerName]].uv = Patch.uvExclusionPoint

    def bakePatchTexture(self, bmeshObj):
        for face in bmeshObj.faces:
            face.select = False
        
        #Unwrap using angle-based approach
        for faceIdx in self.getFacesIdxIterator():
            bmeshObj.faces[faceIdx].select = True
        
        #UV unwrapping using ABF (Angle Based Flattening)
        bpy.ops.uv.unwrap(method = "ANGLE_BASED")

        for faceIdx in self.getFacesIdxIterator():
            bmeshObj.faces[faceIdx].select = False

        #Center the UVs (so that the central vertex is at pos (0.5,0.5)
        uvMapCenter = np.array([0.5, 0.5])
        posShift = uvMapCenter - np.array(self.getVertUV(bmeshObj, self.centerVertexIdx, Patch.uvLayerName))
        
        for vIdx in self.verticesIdxList:
            vertUVCoords = self.getVertUV(bmeshObj, vIdx, Patch.uvLayerName)
            self.setVertUV(bmeshObj, vIdx, Patch.uvLayerName, np.array(vertUVCoords) + posShift)
        
        #Rotate the UVs to match local axis
        #Finding a ref
        linkedEdge = bmeshObj.verts[self.centerVertexIdx].link_edges[0]
        refVertIdx = (linkedEdge.verts[0] if linkedEdge.verts[0].index != self.centerVertexIdx else linkedEdge.verts[1]).index
        
        #Projecting that ref onto the plane
        planeOrigin = np.array(bmeshObj.verts[self.centerVertexIdx].co)
        vertWorldPos = np.array(bmeshObj.verts[refVertIdx].co)
        vertRelPos = vertWorldPos - planeOrigin
        projCoords = np.array([np.dot(vertRelPos, self.eigenVecs[:,0]), np.dot(vertRelPos, self.eigenVecs[:,1])])

        #Angle between the projection and the x-axis (in the world plane)
        angleWorld = -math.atan2(projCoords[1], projCoords[0])
        
        #xAxis in the UV map
        refVecUV = np.matrix(self.getVertUV(bmeshObj, refVertIdx, Patch.uvLayerName)).T
        centerVec = np.matrix(uvMapCenter).T
        centeredRefUV = refVecUV - centerVec
        angleUV = math.atan2(centeredRefUV[1], centeredRefUV[0])
        
        #Rotation matrix
        rotMatInvUV = np.matrix([[math.cos(-angleUV), -math.sin(-angleUV)],[math.sin(-angleUV), math.cos(-angleUV)]])
        rotMatInvAxis = np.matrix([[math.cos(angleWorld), -math.sin(angleWorld)],[math.sin(angleWorld), math.cos(angleWorld)]])
        rotMat = rotMatInvAxis @ rotMatInvUV
        
        #Rotate around the central vec
        for vIdx in self.verticesIdxList:
            vertUVCoords = np.matrix(self.getVertUV(bmeshObj, vIdx, Patch.uvLayerName)).T
            self.setVertUV(bmeshObj, vIdx, Patch.uvLayerName, (rotMat @ (vertUVCoords - centerVec)) + centerVec)
        
        #Bake
        bpy.ops.object.bake(type='DIFFUSE', pass_filter = {'COLOR'}, use_clear = True, margin = Patch.textureMargin)

        #Save image
        self.pixels = bpy.data.images[Patch.bakedImgName].pixels[:]

        #Remove UVs from sight
        for vertIdx in self.verticesIdxList:
            vert = bmeshObj.verts[vertIdx]
            for loop in vert.link_loops:
                loop[bmeshObj.loops.layers.uv[Patch.uvLayerName]].uv = Patch.uvExclusionPoint

    def getFaceRayIntersect(face, rayNorm, rayOrig):
        """
        Returns the point of intersection between a face and a ray emitted from a certain origin (or None if none is found)
        """
        intersPoint = mathutils.geometry.intersect_ray_tri(face.verts[0].co, face.verts[1].co, face.verts[2].co, -rayNorm, rayOrig)
        if intersPoint == None:
            intersPoint = mathutils.geometry.intersect_ray_tri(face.verts[0].co, face.verts[1].co, face.verts[2].co, rayNorm, rayOrig)

        return intersPoint

    def rayFaceDist_inter(foo, faceIdx, samplePos, sampleNormal, bmeshObj):
        """
        Distance between the sample position and the closest point on a given face to that sample's emitted ray
        """
        #Returns the smallest distance between a ray and a face (its triangle)
        face = bmeshObj.faces[faceIdx[0]]
        
        intersPoint = Patch.getFaceRayIntersect(face, sampleNormal, samplePos)
            
        if intersPoint != None:
            #The ray intersects with the triangle : the dist is zero
            return 0.0

            #return np.linalg.norm(np.array(intersPoint) - samplePos)
        else:
            #The ray doesn't intersect with the triangle : its smallest distance is the smallest distance to one of its edges
            r = sampleNormal
            dot_rr = np.dot(r, r)
            
            minDist = float('inf')
            for i in range(3):
                v0 = np.array(face.verts[i].co)
                v1 = np.array(face.verts[(i+1)%3].co)
                C = samplePos - v0
                D = v0 - v1
                dot_rD = np.dot(r, D)
                u = min(1.0, max(0.0, np.dot(C, r * dot_rD - D * dot_rr) / (dot_rr * np.dot(D, D) - dot_rD**2)))
                t = - (np.dot(C, r) + u * dot_rD) / dot_rr
                minDist = min(minDist, np.linalg.norm((samplePos + t * r) - (v0 + u * (v1 - v0))))
                
            return minDist

    def rayFaceDist_noInter(foo, faceIdx, samplePos, sampleNormal, bmeshObj):
        """
        Distance between the ray and the closest triangle edge position (considered that there is no intersection)
        """
        #Returns the smallest distance between a ray and a face (its triangle)
        face = bmeshObj.faces[faceIdx[0]]
        
        #The ray doesn't intersect with the triangle : its smallest distance is the smallest distance to one of its edges
        r = sampleNormal
        dot_rr = np.dot(r, r)
        
        minDist = float('inf')
        for i in range(3):
            v0 = np.array(face.verts[i].co)
            v1 = np.array(face.verts[(i+1)%3].co)
            C = samplePos - v0
            D = v0 - v1
            dot_rD = np.dot(r, D)
            u = min(1.0, max(0.0, np.dot(C, r * dot_rD - D * dot_rr) / (dot_rr * np.dot(D, D) - dot_rD**2)))
            t = - (np.dot(C, r) + u * dot_rD) / dot_rr
            minDist = min(minDist, np.linalg.norm((samplePos + t * r) - (v0 + u * (v1 - v0))))
            
        return minDist 

    #Setting up C++ functions
    testlib = ctypes.CDLL('/home/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/src/test/libutils.so')
    testlib.getClosestFaceFromRay.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_uint, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    testlib.getClosestFaceFromRay.restype = ctypes.c_int

    def samplePatchNormals(self, bmeshObj):
        planeOrigin = np.array(bmeshObj.verts[self.centerVertexIdx].co)
        v1 = self.eigenVecs[:,0]
        v2 = self.eigenVecs[:,1]
        
        #Finding the scale of the plane according to the largest edge length
        maxEdgeLen = 0.0
        for edgeIdx in self.getEdgesIdx(bmeshObj):
            maxEdgeLen = max(maxEdgeLen, bmeshObj.edges[edgeIdx].calc_length())
        planeScale = 2.0 * maxEdgeLen
        
        ##Setting constants for the sampling
        #Python
        scaleFac = planeScale / Patch.sampleRes
        centerFac = (Patch.sampleRes - 1)/2.0
        faceIndices = [faceIdx for faceIdx in self.getFacesIdxIterator()]
        #C++
        samplePlaneNormal = -self.eigenVecs[:,2]
        samplePlaneNormal_ptr = samplePlaneNormal.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        facePoints = np.array([[np.array(bmeshObj.faces[faceIdx].verts[i].co) for i in range(3)] for faceIdx in faceIndices])
        facePoints_ptr = facePoints.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        facePointsCount = len(faceIndices)

        #Sampling
        self.sampledNormals = [np.zeros((3,1)) for i in range(Patch.sampleRes**2)]
        for y in range(Patch.sampleRes):
            for x in range(Patch.sampleRes):
                sampleCoords = planeOrigin + scaleFac * (v1 * (x - centerFac) + v2 * (y - centerFac))
                sampleCoords_ptr = sampleCoords.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
                
                faceIdxPos = Patch.testlib.getClosestFaceFromRay(facePoints_ptr, facePointsCount, sampleCoords_ptr, samplePlaneNormal_ptr)
                faceIdx = faceIndices[faceIdxPos]

                self.sampledNormals[x + y * Patch.sampleRes] = self.rotMatInv @ np.array(bmeshObj.faces[faceIdx].normal)
    
    defaultAxisColors = ["ff0000", "00ff00", "0000ff"]
    def drawLRF(self, gpencil, gp_frame, bmeshObj, lineSize = 0.02, startThck = 0.5, endThck = 3.0, axisColors = defaultAxisColors):
        """
        Draws in a grease pencil canvas the eigenvectors associated to this patch's normal tensor
        """
        patchCentralPos = self.getCentralPos(bmeshObj)
        for i in range(3):
            dir = self.eigenVecs[:,i]
            debugDrawing.draw_line(gpencil, gp_frame, (patchCentralPos, patchCentralPos + lineSize * dir), (startThck, endThck), axisColors[i])

    def drawNormalSamplePlane(self, gpencil, gp_frame, bmeshObj, color = "800080"):
        """
        Draws in a grease pencil canvas the plane used to sample the normals 
        """
        planeOrigin = np.array(bmeshObj.verts[self.centerVertexIdx].co)
        v1 = self.eigenVecs[:,0]
        v2 = self.eigenVecs[:,1]
        
        #Finding the scale of the plane according to the largest edge length
        maxEdgeLen = 0.0
        for edgeIdx in self.getEdgesIdx(bmeshObj):
            maxEdgeLen = max(maxEdgeLen, bmeshObj.edges[edgeIdx].calc_length())
        planeScale = 2.0 * maxEdgeLen
        
        #Setting constants for the sampling
        scaleFac = planeScale / Patch.sampleRes
        centerFac = (Patch.sampleRes - 1)/2.0
        
        #Drawing the frame
        points = [v1 + v2, v1 - v2, -(v1 + v2), v2 - v1]
        for i in range(4):
            p0 = planeOrigin + 0.5 * planeScale * points[i]
            p1 = planeOrigin + 0.5 * planeScale * points[(i+1)%4]
            debugDrawing.draw_line(gpencil, gp_frame, (p0, p1), (0.5, 0.5), color)

        #Sampling
        for y in range(Patch.sampleRes):
            for x in range(Patch.sampleRes):
                sampleCoords = planeOrigin + scaleFac * (v1 * (x - centerFac) + v2 * (y - centerFac))
                debugDrawing.draw_line(gpencil, gp_frame, (sampleCoords, sampleCoords), (2.0, 2.0), color)

    