import numpy as np
import ctypes

testlib = ctypes.CDLL('./libutils.so')

n = 18
dtype = np.float64
input_array = np.array([[[0.0, 2.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]], [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]])
print(input_array)
input_ptr = input_array.ctypes.data_as(ctypes.POINTER(ctypes.c_double))


testlib.getClosestFaceFromRay.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
testlib.getClosestFaceFromRay.restype = ctypes.c_int

ass = testlib.getClosestFaceFromRay(input_ptr, n, input_ptr, input_ptr)

#print(input_ptr)