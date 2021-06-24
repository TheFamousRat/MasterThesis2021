#include <iostream>
#include <eigen3/Eigen/Dense>

/*
 * Returns the id (relative to facePointsArr) of the closest triangle the ray went through
 */
int _getClosestFaceFromRay(double* facePointsArr, int faceCount, double* rayOrig_, double* rayDir_);