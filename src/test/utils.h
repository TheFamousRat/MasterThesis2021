#ifndef UTILS_H
#define UTILS_H

#include <iostream>
#include <vector>
#include <limits>

#include <eigen3/Eigen/Dense>

#define EPSILON 0.0000001

/*
 * Returns the id (relative to facePointsArr) of the closest triangle the ray went through
 */
int _getClosestFaceFromRay(double* facePointsArr, unsigned int faceCount, double* rayOrig_, double* rayDir_);

#endif