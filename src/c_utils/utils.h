#ifndef UTILS_H
#define UTILS_H

#include <iostream>
#include <vector>
#include <limits>

#include <eigen3/Eigen/Dense>

#define EPSILON 0.0000001
#define INF std::numeric_limits<float>::infinity()
#define INV_3 0.33333333333
#define SQRT_3 1.73205080757

typedef Eigen::Vector3f Vector3f;

void _getDepressedCubicRoots(float c, float d, float* arr);

/*
 * Checks if a ray intersects a triangle (and if yes, returns it)
 */
bool RayIntersectsTriangle(Vector3f vTri[3],
                            Vector3f rayOrig, 
                            Vector3f rayDir, 
                            Vector3f& outIntersectionPoint);

/*
 * Returns the id (relative to facePointsArr) of the closest triangle the ray went through
 */
int _getClosestFaceFromRay(double* facePointsArr, unsigned int faceCount, double* rayOrig_, double* rayDir_);

#endif