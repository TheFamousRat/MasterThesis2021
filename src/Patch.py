import math
import numpy as np
import itertools

class Patch:
    def __init__(self, bmeshObj, centralFaceIdx, ringsNum):
        #Creates a patch, built from a central face and its ringsNum neighbouring rings
        self.centralFaceIdx = centralFaceIdx
        self.clusterLabel = None

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

        self.__calculatePatchEigenValues(bmeshObj)

    def __calculatePatchEigenValues(self, bmeshObj):
        #Extracting the eigenvalues from the patch's normals' correlation matrix. Used to compare patches between each other
        normalsConvMat = np.zeros((3,3))

        #Computing some constant values for tensor voting
        maxFaceSize = 0.0
        facesBarycenters = {}
        sigma = 0.0
        facesDists = {}

        for faceIdx in self.getFacesIdxIterator():
            #Calculating the max face area, to normalize face areas later
            maxFaceSize = max(maxFaceSize, bmeshObj.faces[faceIdx].calc_area())
            #Baking faces barycenters
            facesBarycenters[faceIdx] = self.getFaceBarycenter(bmeshObj.faces[faceIdx])
            #Finding the largest distance between the central face and a triangle barycenter
            facesDists[faceIdx] = np.linalg.norm(facesBarycenters[self.centralFaceIdx] - facesBarycenters[faceIdx])

        sigma = max(facesDists.values())

        #Normal tensor voting
        for faceIdx in self.getFacesIdxIterator():
            faceNormal = np.matrix(np.array(bmeshObj.faces[faceIdx].normal)).T #Transforming the face normal into a vector
            faceWeight = (bmeshObj.faces[faceIdx].calc_area() / maxFaceSize) * math.exp(-facesDists[faceIdx]/sigma)
            normalsConvMat += faceWeight * (faceNormal @ faceNormal.T)

        self.eigenVals, self.eigenVecs = np.linalg.eig(normalsConvMat)
        self.rotMat = np.matrix(self.eigenVecs)
        self.rotMatInv = np.linalg.inv(self.rotMat)

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

    def getFaceBarycenter(self, face):
        return np.array(face.calc_center_median())

    def normalizePosition(self, bmeshObj, pos, isGlobalPos):
        """
        Returns the transformed position (unrotated and centered if global) of a given vector pos
        """
        centeredPos = pos - (self.getFaceBarycenter(bmeshObj.faces[self.centralFaceIdx]) if isGlobalPos else np.array([0,0,0]))
        return np.asarray(self.rotMatInv @ np.matrix(centeredPos).T).reshape(-1)