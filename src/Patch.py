import os
import math
import numpy as np
import scipy.linalg as la
import itertools
import ctypes

import bpy

import debugDrawing

class PatchBuildingError(Exception):
    pass

class Patch:
    ##Static constants
    #Related to texture baking
    uvLayerName = "tempProj"
    bakedImgName = "bakedImage"
    bakedImgSize = 64
    imageNodeName = "BakedTextureNode"
    uvLayerNodeName = "BakedUVLayerNode"
    uvExclusionPoint = np.array([2.0, 2.0]) #Location where the UV not to be used are isolated
    uvMapCenter = np.array([0.5, 0.5])
    textureMargin = 1
    #Related to patch sampling
    planeScale = 0.05
    sampleRes = 8
    samplesCount = sampleRes**2
    centerPatchIdx = (samplesCount // 2) + 1 if ((sampleRes%2) != 0) else ((sampleRes*(sampleRes - 1))//2) + np.array([-1,0,sampleRes-1,sampleRes])

    def __init__(self, bmeshObj, centerFaceIdx, ringsNum):
        #Creates a patch, built from a central vertex and its ringsNum neighbouring rings
        self.centerFaceIdx = centerFaceIdx
        self.facesCounts = 0
        #self.isValid = True

        self.rings = [[self.centerFaceIdx]]
        #self.rings.append([face.index for face in bmeshObj.faces[self.centerFaceIdx].link_faces]) #Ring one, based on the central vertex's neighbourhood

        for i in range(ringsNum):
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


        #if len(self.rings[0]) == 0:
        #    self.isValid = False
        #    raise PatchBuildingError("Empty patch rings")

        self.verticesIdxList = set()
        for faceIdx in self.getFacesIdxIterator():
            for vert in bmeshObj.faces[faceIdx].verts:
                self.verticesIdxList.add(vert.index)
        self.verticesIdxList = np.array(list(self.verticesIdxList))

        self.pixels = np.array([])
        
        self.computeProperties(bmeshObj)

    def computeProperties(self, bmeshObj):
        """
        Syntaxic sugar to (re-)calculate the geometric descriptors of the patch
        """
        self.calculateSurfaceStats(bmeshObj)
        self.calculatePatchEigenValues(bmeshObj)
        self.samplePatchNormals(bmeshObj)

    def calculateSurfaceStats(self, bmeshObj):
        """
        Calculates the sum of areas of the triangles of the patch
        """
        #Total area (sum of triangle areas)
        self.totalArea = np.sum([bmeshObj.faces[faceIdx].calc_area() for faceIdx in self.getFacesIdxIterator()])

        #Max edge length
        self.avgEdgeLen = np.average([bmeshObj.edges[edgeIdx].calc_length() for edgeIdx in self.getEdgesIdx(bmeshObj)])

        #Barycenter (unweighted average of vertices)
        #self.barycenter = np.average([np.array(bmeshObj.verts[vertexIdx].co) for vertexIdx in self.verticesIdxList], axis = 0) 

    def calculateFaceWeights(self, bmeshObj):
        """
        Calculates weights for each face, based on the face's relative distance to the patch's center and on faces' areas
        """
        faceWeights = {}

        #Computing some constant values for tensor voting
        maxFaceSize = 0.0
        facesBarycenters = {}
        facesDists = {}
        centralPos = self.getOrigin(bmeshObj)

        for faceIdx in self.getFacesIdxIterator():
            #Calculating the max face area, to normalize face areas later
            maxFaceSize = max(maxFaceSize, bmeshObj.faces[faceIdx].calc_area())
            #Baking faces barycenters
            facesBarycenters[faceIdx] = Patch.getFaceBarycenter(bmeshObj.faces[faceIdx])
            #Finding the largest distance between the central face and a triangle barycenter
            facesDists[faceIdx] = np.linalg.norm(facesBarycenters[faceIdx] - centralPos)

        sigma = max(facesDists.values()) / 3.0

        for faceIdx in self.getFacesIdxIterator():
            faceWeights[faceIdx] = (bmeshObj.faces[faceIdx].calc_area() / maxFaceSize) * math.exp(-facesDists[faceIdx]/sigma)

        return faceWeights

    def calculatePatchEigenValues(self, bmeshObj):
        """
        Calculates the LRF and the eigenvalues of the patch's tensor
        """
        #Extracting the eigenvalues from the patch's normals' correlation matrix. Used to compare patches between each other
        faceWeights = self.calculateFaceWeights(bmeshObj)
        normalsCovMat = np.zeros((3,3))

        #Normal tensor voting
        for faceIdx in self.getFacesIdxIterator():
            normalVec = bmeshObj.faces[faceIdx].normal
            normalVec = normalVec / np.linalg.norm(normalVec)
            faceNormal = np.matrix(np.array(normalVec)).T #Transforming the face normal into a vector
            normalsCovMat += (faceNormal @ faceNormal.T) * faceWeights[faceIdx]

        #Extracting the orthogonal directions from the tensor
        #The signs of the eigenvectors are unreliable here and will be corrected
        self.eigenVals, self.eigenVecs = la.eigh(normalsCovMat)

        if True:
            #Implementing a proposition by Sheng Ao et al. 2019 "A repeatable and robust local reference frame for 3D surface matching"
            #Correcting the z-axis (normal)
            h2 = 0.0
            for faceIdx in self.getFacesIdxIterator():
                face = bmeshObj.faces[faceIdx]
                h2 += np.dot(face.normal, self.eigenVecs[:,2]) * faceWeights[faceIdx]

            self.eigenVecs[:,2] = self.eigenVecs[:,2] * np.sign(h2)

        
            #Correcting the x-axis
            centerPos = self.getOrigin(bmeshObj)
            xAxis = np.array([0.0, 0.0, 0.0])
            for faceIdx in self.getFacesIdxIterator():
                face = bmeshObj.faces[faceIdx]
                facePos = Patch.getFaceBarycenter(bmeshObj.faces[faceIdx])
                faceCenterVec = facePos - centerPos
                dot_zProj = np.dot(self.eigenVecs[:,2], faceCenterVec)
                
                faceProjRel = faceCenterVec - self.eigenVecs[:,2] * dot_zProj
                
                #w1 = math.exp(-(np.linalg.norm(faceCenterVec)**2.0)*3.0)
                w2 = dot_zProj**(2.0)
                #w3 = bmeshObj.faces[faceIdx].calc_area()
                xAxis += w2 * faceWeights[faceIdx] * (faceProjRel)

            #Finally get the y-axis from the other two corrected vectors and normalizing them
            self.eigenVecs[:,0] = xAxis#self.eigenVecs[:,0] if np.dot(self.eigenVecs[:,0], xAxis) >= 0.0 else -self.eigenVecs[:,0]#np.cross(self.eigenVecs[:,1], self.eigenVecs[:,2])
            self.eigenVecs[:,0] = self.eigenVecs[:,0] / np.linalg.norm(self.eigenVecs[:,0])
            self.eigenVecs[:,1] = -np.cross(self.eigenVecs[:,0], self.eigenVecs[:,2])
            self.eigenVecs[:,1] = self.eigenVecs[:,1] / np.linalg.norm(self.eigenVecs[:,1])
            
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

    @staticmethod
    def getFaceBarycenter(face):
        """
        Returns the barycenter of a given face, in model space
        """
        return np.array(face.calc_center_median())

    def getOrigin(self, bmeshObj):
        return Patch.getFaceBarycenter(bmeshObj.faces[self.centerFaceIdx])

    def calculateFaceNormal(self, face):
        """
        Calculate the normal of a face using cross product
        """
        n = np.cross(face.verts[0].co - face.verts[1].co, face.verts[1].co - face.verts[2].co)
        return n / np.linalg.norm(n)

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
        """
        Setting up global Blender variables to prepare for texture baking
        """
        prevRenderEngine = bpy.context.scene.render.engine
        bpy.context.scene.render.engine = 'CYCLES'

        selecObj = bpy.context.active_object

        #Creating an image to bake to
        if not Patch.bakedImgName in bpy.data.images:
            bpy.data.images.new(Patch.bakedImgName, Patch.bakedImgSize, Patch.bakedImgSize, alpha = True)
        bpy.data.images[Patch.bakedImgName].source = 'GENERATED'
        bpy.data.images[Patch.bakedImgName].scale(Patch.bakedImgSize, Patch.bakedImgSize)
            
        #Preparing the shaders for baking if they aren't already
        for mat in selecObj.data.materials:
            nodeTree = mat.node_tree #shorthand
            #Reloading the dependent images for faster baking (0 idea why this works, but it does)
            #for node in nodeTree.nodes:
            #    if node.type == 'TEX_IMAGE':
            #        node.image.pack()
            #        node.image.unpack()
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

    def createCenteredUVMap(self, bmeshObj, recenter = True, unrotate = True):
        """
        UV unwrapping the patch
        """
        selecObj = bpy.context.active_object
        #Creating a temporary UV layer
        if not Patch.uvLayerName in selecObj.data.uv_layers:
            selecObj.data.uv_layers.new(name = Patch.uvLayerName)
        
        uvLayer = selecObj.data.uv_layers[Patch.uvLayerName] 
        if not uvLayer.active:
            uvLayer.active = True

        for face in bmeshObj.faces:
            face.select = False

        #Unwrap using angle-based approach
        for faceIdx in self.getFacesIdxIterator():
            bmeshObj.faces[faceIdx].select = True
        
        #UV unwrapping using ABF (Angle Based Flattening)
        bpy.ops.uv.unwrap(method = "ANGLE_BASED")

        for faceIdx in self.getFacesIdxIterator():
            bmeshObj.faces[faceIdx].select = False

        self.verticesUVs = {vIdx : np.array(self.getVertUV(bmeshObj, vIdx, Patch.uvLayerName)) for vIdx in self.verticesIdxList}

        #Center the UVs (so that the area-weighted centroid is at pos uvMapCenter)
        if recenter:
            w = np.array([bmeshObj.faces[faceIdx].calc_area() for faceIdx in self.getFacesIdxIterator()])
            facesUVBarycenters = [np.average([self.verticesUVs[vert.index] for vert in bmeshObj.faces[faceIdx].verts], axis = 0) for faceIdx in self.getFacesIdxIterator()]
            weightedBarycenter = np.average(facesUVBarycenters, axis = 0, weights = w)
            posShift = Patch.uvMapCenter - weightedBarycenter

            for vIdx in self.verticesIdxList:
                self.verticesUVs[vIdx] = self.verticesUVs[vIdx] + posShift
        
        ##Rotate the UVs to match local axis
        if unrotate:
            #Finding a ref
            #linkedEdge = bmeshObj.verts[self.centerVertexIdx].link_edges[0]
            refVertIdx = self.verticesIdxList[0]#(linkedEdge.verts[0] if linkedEdge.verts[0].index != self.centerVertexIdx else linkedEdge.verts[1]).index
            
            #Projecting that ref onto the plane
            planeOrigin = self.getOrigin(bmeshObj)
            vertWorldPos = np.array(bmeshObj.verts[refVertIdx].co)
            vertRelPos = vertWorldPos - planeOrigin
            projCoords = np.array([np.dot(vertRelPos, self.eigenVecs[:,0]), np.dot(vertRelPos, self.eigenVecs[:,1])])

            #Angle between the projection and the x-axis (in the world plane)
            angleWorld = math.atan2(projCoords[1], projCoords[0])

            #xAxis in the UV map
            refVecUV = np.matrix(self.verticesUVs[refVertIdx]).T
            centerVec = np.matrix(Patch.uvMapCenter).T
            centeredRefUV = refVecUV - centerVec
            angleUV = math.atan2(centeredRefUV[1], centeredRefUV[0])
            
            #Rotation matrix
            angleDiff = angleWorld - angleUV
            rotMat = np.matrix([[math.cos(angleDiff), -math.sin(angleDiff)],[math.sin(angleDiff), math.cos(angleDiff)]])
            
            #Rotate around the central vec
            for vIdx in self.verticesIdxList:
                self.verticesUVs[vIdx] = np.asarray((rotMat @ (np.matrix(self.verticesUVs[vIdx]).T - centerVec)) + centerVec)

    def getUVMapSurface(self, bmeshObj):
        return np.sum([np.cross(self.verticesUVs[face.verts[0].index] - self.verticesUVs[face.verts[1].index], self.verticesUVs[face.verts[0].index] - self.verticesUVs[face.verts[2].index], axis = 0)[0] / 2.0 for face in [bmeshObj.faces[faceIdx] for faceIdx in self.getFacesIdxIterator()]])

    def scaleUVMap(self, scaleFac):
        cntr = Patch.uvMapCenter.reshape(2,1)
        for vIdx in self.verticesUVs:
            self.verticesUVs[vIdx] = scaleFac * (self.verticesUVs[vIdx] - cntr) + cntr

    def applyUVMap(self, bmeshObj):
        for vert in bmeshObj.verts:
            for loop in vert.link_loops:
                loop[bmeshObj.loops.layers.uv[Patch.uvLayerName]].uv = Patch.uvExclusionPoint

        for vIdx in self.verticesIdxList:
            self.setVertUV(bmeshObj, vIdx, Patch.uvLayerName, self.verticesUVs[vIdx])

    def bakePatchTexture(self, bmeshObj):
        """
        Extracts an image texture associated with the patch's location of the mesh
        """
        #Extracting the UV map
        self.applyUVMap(bmeshObj)
        
        #Bake
        bpy.ops.object.bake(type='DIFFUSE', pass_filter = {'COLOR'}, use_clear = True, margin = Patch.textureMargin)

        #Save image
        self.pixels = np.array(bpy.data.images[Patch.bakedImgName].pixels[:], dtype=np.float16)

        #Remove UVs from sight
        #for vertIdx in self.verticesIdxList:
        #    vert = bmeshObj.verts[vertIdx]
        #    for loop in vert.link_loops:
        #        loop[bmeshObj.loops.layers.uv[Patch.uvLayerName]].uv = Patch.uvExclusionPoint

    def getNormalSamplesPosition(self, bmeshObj):
        """
        Produces a list of position corresponding to samples' origins in the model space
        """
        planeOrigin = self.getOrigin(bmeshObj)
        v1 = self.eigenVecs[:,0]
        v2 = self.eigenVecs[:,1]
        
        #Finding the scale of the plane according to the largest edge length
        planeScale = 2.0 * self.avgEdgeLen
        
        scaleFac = planeScale / Patch.sampleRes
        centerFac = (Patch.sampleRes - 1)/2.0

        ret = [None] * Patch.samplesCount
        for y in range(Patch.sampleRes):
            for x in range(Patch.sampleRes):
                ret[x + y * Patch.sampleRes] = planeOrigin + scaleFac * (v1 * (x - centerFac) + v2 * (y - centerFac))

        return ret

    #Setting up C++ functions
    testlib = ctypes.CDLL('/home/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/src/c_utils/libutils.so')
    testlib.getClosestFaceFromRay.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_uint, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
    testlib.getClosestFaceFromRay.restype = ctypes.c_int

    def samplePatchNormals(self, bmeshObj):
        """
        Produces a regularly sampled map of the patch's normals
        """
        ##Setting constants for the sampling
        #Python
        faceIndices = [faceIdx for faceIdx in self.getFacesIdxIterator()]
        #C++
        samplePlaneNormal = -self.eigenVecs[:,2]
        samplePlaneNormal_ptr = samplePlaneNormal.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        facePoints = np.array([[np.array(bmeshObj.faces[faceIdx].verts[i].co) for i in range(3)] for faceIdx in faceIndices])
        facePoints_ptr = facePoints.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        facePointsCount = len(faceIndices)

        #Sampling
        samplePos = self.getNormalSamplesPosition(bmeshObj)
        self.sampledNormals = [np.zeros((3,1)) for i in range(Patch.samplesCount)]
        for y in range(Patch.sampleRes):
            for x in range(Patch.sampleRes):
                sampleCoords = samplePos[x + y * Patch.sampleRes]
                sampleCoords_ptr = sampleCoords.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
                
                faceIdxPos = Patch.testlib.getClosestFaceFromRay(facePoints_ptr, facePointsCount, sampleCoords_ptr, samplePlaneNormal_ptr)
                faceIdx = faceIndices[faceIdxPos]

                self.sampledNormals[x + y * Patch.sampleRes] = self.rotMatInv @ np.array(bmeshObj.faces[faceIdx].normal)
        
        self.sampledNormals = np.array(self.sampledNormals)

    
    defaultAxisColors = ["ff0000", "00ff00", "0000ff"]
    def drawLRF(self, gpencil, gp_frame, bmeshObj, lineSize = 0.02, startThck = 0.5, endThck = 3.0, drawAxis = (True, True, True), axisColors = defaultAxisColors):
        """
        Draws in a grease pencil canvas the eigenvectors associated to this patch's normal tensor
        """
        patchCentralPos = self.getOrigin(bmeshObj)
        for i in range(3):
            if drawAxis[i]:
                dir = self.eigenVecs[:,i]
                debugDrawing.draw_line(gpencil, gp_frame, (patchCentralPos, patchCentralPos + lineSize * dir), (startThck, endThck), axisColors[i])

    def drawNormalSamplePlane(self, gpencil, gp_frame, bmeshObj, frameThck = 0.5, sampleThck = 2.0, color = "800080"):
        """
        Draws in a grease pencil canvas the plane used to sample the normals 
        """
        samplePos = self.getNormalSamplesPosition(bmeshObj)

        self.sampledNormals = [np.zeros((3,1)) for i in range(Patch.samplesCount)]
        for y in range(Patch.sampleRes):
            for x in range(Patch.sampleRes):
                sampleCoords = samplePos[x + y * Patch.sampleRes]
                debugDrawing.draw_line(gpencil, gp_frame, (sampleCoords, sampleCoords), (sampleThck, sampleThck), color)
