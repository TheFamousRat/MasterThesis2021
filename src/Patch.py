import math
import numpy as np

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

    def __getFaceBarycenter(self, bmeshObj, faceIdx):
        return np.array(bmeshObj.faces[faceIdx].calc_center_median_weighted())

    def __calculatePatchEigenValues(self, bmeshObj):
        #Extracting the eigenvalues from the patch's normals' correlation matrix. Used to compare patches between each other
        normalsConvMat = np.zeros((3,3))

        #Calculating the max face area, to normalize face areas later
        maxFaceSize = 0.0
        for ring in self.rings:
            for faceIdx in ring:
                maxFaceSize = max(maxFaceSize, bmeshObj.faces[faceIdx].calc_area())

        #Baking faces barycenters
        facesBarycenters = {}
        for ring in self.rings:
            for faceIdx in ring:
                facesBarycenters[faceIdx] = np.array(bmeshObj.faces[faceIdx].calc_center_median_weighted())

        #Getting the size of a bounding cube for the patch
        sigma = 0.0
        facesDists = {}
        for ring in self.rings:
            for faceIdx in ring:
                facesDists[faceIdx] = np.linalg.norm(facesBarycenters[self.centralFaceIdx] - facesBarycenters[faceIdx])
        sigma = max(facesDists.values())

        #Normal tensor voting
        for ring in self.rings:
            for faceIdx in ring:
                faceNormal = np.matrix(np.array(bmeshObj.faces[faceIdx].normal)).T #Transforming the face normal into a vector
                faceWeight = (bmeshObj.faces[faceIdx].calc_area() / maxFaceSize) * math.exp(-facesDists[faceIdx]/sigma)
                normalsConvMat += faceWeight * (faceNormal @ faceNormal.T)

        self.eigenVals, self.eigenVecs = np.linalg.eig(normalsConvMat)
