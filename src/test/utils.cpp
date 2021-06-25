
#include "utils.h"

extern "C" {
    int getClosestFaceFromRay(double* facePointsArr, unsigned int faceCount, double* rayOrig_, double* rayDir_)
    {
        return _getClosestFaceFromRay(facePointsArr, faceCount, rayOrig_, rayDir_);
    }
}

bool RayIntersectsTriangle(Eigen::Vector3f v0,
                            Eigen::Vector3f v1,
                            Eigen::Vector3f v2,
                            Eigen::Vector3f rayOrig, 
                            Eigen::Vector3f rayDir, 
                            Eigen::Vector3f& outIntersectionPoint)
{
    //Möller–Trumbore intersection algorithm. Adapted from the Wikipedia version
    Eigen::Vector3f edge1, edge2, h, s, q;
    float a,f,u,v;
    edge1 = v1 - v0;
    edge2 = v2 - v0;
    
    //Checking normal parallelism
    h = rayDir.cross(edge2);
    a = edge1.dot(h);
    if (a > -EPSILON && a < EPSILON)
        return false; 
    
    //Checking intersection using barycentric coordinates
    f = 1.0/a;
    s = rayOrig - v0;
    u = f * s.dot(h);
    if (u < 0.0 || u > 1.0)
        return false;
    
    q = s.cross(edge1);
    v = f * rayDir.dot(q);
    if (v < 0.0 || u + v > 1.0)
        return false;
    
    // At this stage we can compute t to find out where the intersection point is on the line.
    float t = f * edge2.dot(q);
    if (t > EPSILON) // ray intersection
    {
        outIntersectionPoint = rayOrig + rayDir * t;
        return true;
    }
    else // This means that there is a line intersection but not a ray intersection.
        return false;
}

int _getClosestFaceFromRay(double* facePointsArr, unsigned int faceCount, double* rayOrig_, double* rayDir_) {
    Eigen::Vector3f rayOrig(rayOrig_[0], rayOrig_[1], rayOrig_[2]);
    Eigen::Vector3f rayDir(rayDir_[0], rayDir_[1], rayDir_[2]);

    int faceIdxPos = 0;

    //Checking all the faces crossed by the ray (if any)
    std::vector<bool> faceCrossed(faceCount);
    std::vector<Eigen::Vector3f> crossIntersects;
    Eigen::Vector3f intersecPos;
    for (int i(0) ; i < faceCount ; i++) {
        int faceCoordsStart = i * 9;
        Eigen::Vector3f v0(facePointsArr[faceCoordsStart], facePointsArr[faceCoordsStart + 1], facePointsArr[faceCoordsStart + 2]);
        Eigen::Vector3f v1(facePointsArr[faceCoordsStart + 3], facePointsArr[faceCoordsStart + 4], facePointsArr[faceCoordsStart + 5]);
        Eigen::Vector3f v2(facePointsArr[faceCoordsStart + 6], facePointsArr[faceCoordsStart + 7], facePointsArr[faceCoordsStart + 8]);
        faceCrossed[i] = RayIntersectsTriangle(v0, v1, v2, rayOrig, rayDir, intersecPos);
        
        if (faceCrossed[i]) {
            crossIntersects.push_back(intersecPos);
        }
    }

    if (crossIntersects.size() == 1) {
        //Only one triangle crossed : we pick it
        for (int i(0) ; i < faceCount ; i++) {
            if (faceCrossed[i]) {
                faceIdxPos = i;
                break;
            }
        }
    }
    else if (crossIntersects.size() > 1) {
        //More than one triangle crossed : we pick the closest one
        float smallestDist = std::numeric_limits<float>::infinity();
        int crossTriNum = 0;
        for (int i(0) ; i < faceCount ; i++) {
            if (faceCrossed[i]) {
                float dist = (rayOrig - crossIntersects[crossTriNum]).norm();

                if (dist < smallestDist) {
                    smallestDist = dist;
                    faceIdxPos = i;
                }

                crossTriNum++;
            }
        }
    }
    else {
        //No triangle crossed : we pick the closest face the ray was from
        float smallestDist = std::numeric_limits<float>::infinity();

        for (int i(0) ; i < faceCount ; i++) {

            //The ray doesn't intersect with the triangle : its smallest distance is the smallest distance to one of its edges
            float dot_rr = rayDir.dot(rayDir);
            int faceCoordsStart = i * 9;
            float minEdgeDist = std::numeric_limits<float>::infinity();

            for (int j(0) ; j < 3 ; j++) {
                int v0Idx = j;
                int v1Idx = (j+1)%3;
                Eigen::Vector3f v0(facePointsArr[faceCoordsStart + 3 * v0Idx], facePointsArr[faceCoordsStart + 1 + 3 * v0Idx], facePointsArr[faceCoordsStart + 2 + 3 * v0Idx]);
                Eigen::Vector3f v1(facePointsArr[faceCoordsStart + 3 * v1Idx], facePointsArr[faceCoordsStart + 1 + 3 * v1Idx], facePointsArr[faceCoordsStart + 2 + 3 * v1Idx]);

                Eigen::Vector3f C = rayOrig - v0;
                Eigen::Vector3f D = v0 - v1;
                float dot_rD = rayDir.dot(D);
                float u = std::min(1.0f, std::max(0.0f, C.dot(rayDir * dot_rD - D * dot_rr) / (dot_rr * D.dot(D) - dot_rD*dot_rD)));
                float t = - (rayDir.dot(C) + u * dot_rD) / dot_rr;
                minEdgeDist = std::min(minEdgeDist, ((rayOrig + t * rayDir) - (v0 + u * (v1 - v0))).norm());
            }
                
            if (minEdgeDist < smallestDist) {
                smallestDist = minEdgeDist;
                faceIdxPos = i;
            }
        }
    }

    return faceIdxPos;
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