
#include "utils.h"

extern "C" {
    int getClosestFaceFromRay(double* facePointsArr, int faceCount, double* rayOrig_, double* rayDir_)
    {
        return _getClosestFaceFromRay(facePointsArr, faceCount, rayOrig_, rayDir_);
    }
}

int _getClosestFaceFromRay(double* facePointsArr, int faceCount, double* rayOrig_, double* rayDir_) {
    Eigen::Vector3f rayOrig(rayOrig_[0], rayOrig_[1], rayOrig_[2]);
    Eigen::Vector3f rayDir(rayDir_[0], rayDir_[1], rayDir_[2]);

    int faceIdx = 0;


    return faceIdx;
}

/*#Checking if one triangle was crossed (and only one)
facesCrossed = [(True if Patch.getFaceRayIntersect(bmeshObj.faces[faceIdx[0]], samplePlaneNormal, sampleCoords) != None else False) for faceIdx in faceIndices]
facesCrossed = np.array(facesCrossed)
triangleCrossedCount = sum(facesCrossed)
#Depending on the crossed (or not) triangles, getting the face to sample from
faceIdx = 0
if triangleCrossedCount == 1:
    #At most one triangle was crossed : we pick the normal from the closest face
    faceIdx = faceIndices[np.where(facesCrossed)[0][0]][0]
elif triangleCrossedCount > 1:
    #More than one triangle was crossed, we pick the closest one
    minDist = float('inf')
    
    crossedFacesPos = np.where(facesCrossed == 0)[1]

    for faceIdxPos in crossedFacesPos:
        faceIdx_ = faceIndices[faceIdxPos][0]
        face = bmeshObj.faces[faceIdx_]
        hitCoords = Patch.getFaceRayIntersect(face, samplePlaneNormal, sampleCoords)
        
        dist = np.linalg.norm(np.array(hitCoords) - sampleCoords)
        if dist < minDist:
            minDist = dist
            faceIdx = faceIdx_
else:
    #Distances of triangles from the RayCast
    triDists = cdist([[0]], faceIndices, Patch.rayFaceDist_noInter, samplePos = sampleCoords, sampleNormal = samplePlaneNormal, bmeshObj = bmeshObj)

    faceIdx = faceIndices[np.argmin(triDists)][0]*/