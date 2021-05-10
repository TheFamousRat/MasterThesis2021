import math
import numpy as np

class Patch:
    def __init__(self, bmeshObj, centralFaceIdx, ringsNum):
        self.bmeshObj = bmeshObj
        #Creates a patch, built from a central face and its ringsNum neighbouring rings
        self.centralFaceIdx = centralFaceIdx
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

        self.__calculatePatchEigenValues()

    def __calculatePatchEigenValues(self):
        #Extracting the eigenvalues from the patch's normals' correlation matrix. Used to compare patches between each other
        normalsConvMat = np.zeros((3,3))

        maxFaceSize = 0.0
        for ring in self.rings:
            for faceIdx in ring:
                maxFaceSize = max(maxFaceSize, self.bmeshObj.faces[faceIdx].calc_area())

        centralFaceCenter = np.array(self.bmeshObj.faces[self.centralFaceIdx].calc_center_median_weighted())
        for ring in self.rings:
            for faceIdx in ring:
                faceNormal = np.matrix(np.array(self.bmeshObj.faces[faceIdx].normal)).T #Transforming the face normal into a vector
                faceCenter = np.array(self.bmeshObj.faces[faceIdx].calc_center_median_weighted())
                sigma = 1.0
                facesDist = np.linalg.norm(centralFaceCenter - faceCenter)
                faceWeight = (self.bmeshObj.faces[faceIdx].calc_area() / maxFaceSize) * math.exp(-facesDist/(sigma/3.0))
                normalsConvMat += faceWeight * (faceNormal @ faceNormal.T)

        self.eigenVals, self.eigenVecs = np.linalg.eig(normalsConvMat)

    def getEigenValues(self):
        return self.eigenVals

    def getEigenVectors(self):
        return self.eigenVecs
        
        