
#include "utils.h"
//g++ -fPIC -shared -o libutils.so utils.cpp
extern "C" {
    int getClosestFaceFromRay(double* facePointsArr, unsigned int faceCount, double* rayOrig_, double* rayDir_)
    {
        return _getClosestFaceFromRay(facePointsArr, faceCount, rayOrig_, rayDir_);
    }

    void getDepressedCubicRoots(float p, float q, float* arr) {
        _getDepressedCubicRoots(p, q, arr);
    }
}

void _getDepressedCubicRoots(float c, float d, float* arr) {
    float h = (std::pow(d, 2.0f) / 4.0f + std::pow(c, 3.0f) / 27.0f);

    if (c == 0.0f && d == 0.0f && h == 0.0f) {
        float x = -std::cbrt(d);

        arr[0] = x;  
        arr[1] = x;  
        arr[2] = x;            
    }
    else if (h <= 0) {
        float i = std::sqrt((std::pow(d, 2.0) / 4.0) - h); 
        float j = std::cbrt(i);                    
        float k = std::acos(-(d / (2.0f * i)));       
        float kDiv = k / 3.0f;    
        float L = -j;                              
        float M = std::cos(kDiv);                   
        float N = SQRT_3 * std::sin(kDiv);                 

        arr[0] = 2.0f * j * std::cos(kDiv);
        arr[1] = L * (M + N); 
        arr[2] = L * (M - N); 
    }
    else if (h > 0.0f) {
        float dDiv = d / 2.0f;
        float hSqrt = std::sqrt(h);
        float R = -dDiv + hSqrt;
        float S = std::cbrt(R);          
        float T = -dDiv - hSqrt;
        float U = std::cbrt(T);                   

        arr[0] = (S + U);
        arr[1] = arr[0];
        arr[2] = arr[0];
    }                                                  
}

bool RayIntersectsTriangle(Vector3f vTri[3],
                            Vector3f rayOrig, 
                            Vector3f rayDir, 
                            Vector3f& outIntersectionPoint)
{
    //Checking BBox intersection
    Vector3f triBarycenter = (vTri[0] + vTri[1] + vTri[2]) / 3.0f;
    float largestDist = 0.0f;

    for (int i(0) ; i < 3 ; i++)
        largestDist = std::max(largestDist, (triBarycenter - vTri[i]).norm());

    if (std::abs(rayDir.dot(rayOrig - triBarycenter)) > largestDist)
        return false;

    //Möller–Trumbore intersection algorithm. Adapted from the Wikipedia version
    Vector3f edge1, edge2, h, s, q;
    float a,f,u,v;
    edge1 = vTri[1] - vTri[0];
    edge2 = vTri[2] - vTri[0];

    //Checking normal parallelism
    h = rayDir.cross(edge2);
    a = edge1.dot(h);
    if (a > -EPSILON && a < EPSILON)
        return false; 
    
    //Checking intersection using barycentric coordinates
    f = 1.0/a;
    s = rayOrig - vTri[0];
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
    Vector3f rayOrig(rayOrig_[0], rayOrig_[1], rayOrig_[2]);
    Vector3f rayDir(rayDir_[0], rayDir_[1], rayDir_[2]);

    int faceIdxPos = 0;

    float smallestDist = INF;
    for (int i(0) ; i < faceCount ; i++) {
        int faceCoordsStart = i * 9;
        Vector3f v0(facePointsArr[faceCoordsStart], facePointsArr[faceCoordsStart + 1], facePointsArr[faceCoordsStart + 2]);
        Vector3f v1(facePointsArr[faceCoordsStart + 3], facePointsArr[faceCoordsStart + 4], facePointsArr[faceCoordsStart + 5]);
        Vector3f v2(facePointsArr[faceCoordsStart + 6], facePointsArr[faceCoordsStart + 7], facePointsArr[faceCoordsStart + 8]);
        Vector3f triNorm = (v1 - v0).cross(v2 - v0);

        float dot_rayNormal = rayDir.dot(triNorm);
        if (dot_rayNormal != 0.0f) {
            float dist = std::abs(triNorm.dot(rayOrig - v0));

            if (dist < smallestDist) {
                faceIdxPos = i;
                smallestDist = dist;
            }
        }
    }

    //Checking all the faces crossed by the ray (if any)
    /*std::vector<bool> faceCrossed(faceCount);
    std::vector<Vector3f> crossIntersects;
    Vector3f intersecPos;
    for (int i(0) ; i < faceCount ; i++) {
        int faceCoordsStart = i * 9;
        Vector3f v0(facePointsArr[faceCoordsStart], facePointsArr[faceCoordsStart + 1], facePointsArr[faceCoordsStart + 2]);
        Vector3f v1(facePointsArr[faceCoordsStart + 3], facePointsArr[faceCoordsStart + 4], facePointsArr[faceCoordsStart + 5]);
        Vector3f v2(facePointsArr[faceCoordsStart + 6], facePointsArr[faceCoordsStart + 7], facePointsArr[faceCoordsStart + 8]);
        Vector3f vTri[3] = {v0, v1, v2};
        faceCrossed[i] = RayIntersectsTriangle(vTri, rayOrig, rayDir, intersecPos);
        
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
        float smallestDist = INF;
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
        float smallestDist = INF;
        float dot_rr = rayDir.dot(rayDir);

        for (int i(0) ; i < faceCount ; i++) {

            //The ray doesn't intersect with the triangle : its smallest distance is the smallest distance to one of its edges
            int faceCoordsStart = i * 9;
            float minEdgeDist = INF;

            for (int j(0) ; j < 3 ; j++) {
                int v0Idx = j;
                int v1Idx = (j+1)%3;
                Vector3f v0(facePointsArr[faceCoordsStart + 3 * v0Idx], facePointsArr[faceCoordsStart + 1 + 3 * v0Idx], facePointsArr[faceCoordsStart + 2 + 3 * v0Idx]);
                Vector3f v1(facePointsArr[faceCoordsStart + 3 * v1Idx], facePointsArr[faceCoordsStart + 1 + 3 * v1Idx], facePointsArr[faceCoordsStart + 2 + 3 * v1Idx]);

                Vector3f C = rayOrig - v0;
                Vector3f D = v0 - v1;
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
    }*/

    return faceIdxPos;
}
