import math
import numpy as np
import scipy.linalg as la
import itertools

class Patch:
    def __init__(self, bmeshObj, centralFaceIdx, ringsNum):
        #Creates a patch, built from a central face and its ringsNum neighbouring rings
        self.centralFaceIdx = centralFaceIdx
        self.facesCounts = 0

        self.rings = []
        self.rings.append([centralFaceIdx]) #Ring "zero", based on the central face

        for i in range(ringsNum):
            self.rings.append([])
            for prevRingFaceIdx in self.rings[-2]:
                for vert in bmeshObj.faces[prevRingFaceIdx].verts:
                    for linkedFace in vert.link_faces:
                        #We check the neighbouring face isn't in the 2 previous rings, as well as the current one
                        cond = linkedFace.index in self.rings[-2] or linkedFace.index in self.rings[-1]
                        if i > 0:
                            cond = cond or (linkedFace.index in self.rings[-3])
                        
                        #Adding the face to the ring
                        if not cond:
                            self.rings[-1].append(linkedFace.index)
                            self.facesCounts += 1

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
        verticesSet = self.getVerticesIdx(bmeshObj)

        for vertexIdx in verticesSet:
            self.barycenter += np.array(bmeshObj.verts[vertexIdx].co)

        self.barycenter /= len(verticesSet)

    def calculateFaceWeights(self, bmeshObj):
        self.faceWeights = {}

        #Computing some constant values for tensor voting
        maxFaceSize = 0.0
        facesBarycenters = {}
        facesDists = {}

        facesBarycenters[self.centralFaceIdx] = self.getFaceBarycenter(bmeshObj.faces[self.centralFaceIdx])

        for faceIdx in self.getFacesIdxIterator():
            #Calculating the max face area, to normalize face areas later
            maxFaceSize = max(maxFaceSize, bmeshObj.faces[faceIdx].calc_area())
            #Baking faces barycenters
            facesBarycenters[faceIdx] = self.getFaceBarycenter(bmeshObj.faces[faceIdx])
            #Finding the largest distance between the central face and a triangle barycenter
            facesDists[faceIdx] = np.linalg.norm(facesBarycenters[self.centralFaceIdx] - facesBarycenters[faceIdx])

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
            normalsConvMat += self.faceWeights[faceIdx] * (faceNormal @ faceNormal.T)

        self.eigenVals, self.eigenVecs = la.eig(normalsConvMat)
        self.rotMatInv = np.linalg.inv(self.eigenVecs)
    
    def getFacesIdxIterator(self):
        """
        Returns an iterator to iterate over all faces of the patch in one loop
        """
        return itertools.chain.from_iterable(self.rings)

    def getVerticesIdx(self, bmeshObj):
        """
        Returns a list of the indices of vertices forming the patch
        """
        ret = set()
        for faceIdx in self.getFacesIdxIterator():
            for vert in bmeshObj.faces[faceIdx].verts:
                ret.add(vert.index)
        return ret

    def getEdgesIdx(self, bmeshObj):
        """
        Returns a list of the indices of edges contained within the patch
        """
        ret = set()
        for faceIdx in self.getFacesIdxIterator():
            for edge in bmeshObj.faces[faceIdx].edges:
                ret.add(edge.index)
        return ret

    def getFaceBarycenter(self, face):
        return np.array(face.calc_center_median())

    def normalizePosition(self, bmeshObj, pos, isGlobalPos):
        """
        Returns the transformed position (unrotated and centered if global) of a given vector pos
        """
        centeredPos = pos - (self.getFaceBarycenter(bmeshObj.faces[self.centralFaceIdx]) if isGlobalPos else np.array([0,0,0]))
        return np.asarray(self.rotMatInv @ np.matrix(centeredPos).T).reshape(-1)

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