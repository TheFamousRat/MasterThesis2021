import numpy as np
import ctypes
import time

testlib = ctypes.CDLL('/home/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/src/c_utils/libutils.so')
testlib.getDepressedCubicRoots.argtypes = (ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_float))

arr = (ctypes.c_float*3)()

p = -539.3279613200449
q = 0.5

start = time.time()

testlib.getDepressedCubicRoots(p, q, arr)
print("Roots : ", [x for x in arr])
print([x**3 + p * x + q for x in arr])

end = time.time()

print(end - start)
