import math
import numpy as np
import scipy.linalg as la
import itertools

class Patch:
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

        self.calculateIndicators(bmeshObj)

    def calculateIndicators(self, bmeshObj):
        """
        Syntaxic sugar to (re-)calculate the geometric descriptors of the patch
        """
        self.calculateTotalArea(bmeshObj)
        self.calculateBarycenter(bmeshObj)
        self.calculateFaceWeights(bmeshObj)
        self.calculatePatchEigenValues(bmeshObj)

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
        normalsConvMat = np.zeros((3,3))

        #Normal tensor voting
        for faceIdx in self.getFacesIdxIterator():
            normalVec = bmeshObj.faces[faceIdx].normal
            normalVec = normalVec / np.linalg.norm(normalVec)
            faceNormal = np.matrix(np.array(normalVec)).T #Transforming the face normal into a vector
            normalsConvMat += (faceNormal @ faceNormal.T) * self.faceWeights[faceIdx]

        #Extracting the orthogonal directions from the tensor
        #The signs of the eigenvectors are unreliable here and will be corrected
        self.eigenVals, self.eigenVecs = la.eigh(normalsConvMat)

        #Correcting the third eigenvector which estimates the patch normal
        centralNormal = bmeshObj.verts[self.centerVertexIdx].normal
        patchNormal = self.eigenVecs[:,2]
        if np.dot(centralNormal, -patchNormal) > 0.0:
            self.eigenVecs[:,2] = -self.eigenVecs[:,2]

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