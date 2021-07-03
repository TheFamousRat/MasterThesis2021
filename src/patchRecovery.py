###Loading libraries
##Pip/standard libraries loading
#Python standard libraries
import os
import sys
import time
import math
#To compress mesh data files efficiently
import pickle
import lzma
#Image processing
from PIL import Image
#Blender libs
import bpy
import bmesh
#Hashing utilies for mesh unique identification
import hashlib
#C communication
import ctypes
#Scikit suite
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.metrics import pairwise_distances_argmin_min
from scipy.optimize import linear_sum_assignment
from sklearn.neighbors import KDTree
#Show progress bar utility
from progress.bar import Bar

##Local libraries (re-)loading
#Loading user-defined modules (subject to frequent changes and needed reloading)
pathsToAdd = ["/home/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/src"]

for pathToAdd in pathsToAdd:
    sys.path.append(pathToAdd)

import Patch
import debugDrawing

import importlib
importlib.reload(Patch)
importlib.reload(debugDrawing)

for pathToAdd in pathsToAdd:
    sys.path.remove(pathToAdd)

###Constants
RINGS_NUM = 2 #Number of rings around the central face to take into the patch
#Used in the process of "correcting" the eigenvectors' signs
COLUMNS_SIGN_MODIFIED = 2
NUMBER_OF_SIGN_COMBINATION = 2**COLUMNS_SIGN_MODIFIED

##GPencil debug drawing global variables
gpencil, gp_layer = debugDrawing.init_grease_pencil()
gp_layer.clear() #Removing the previous GPencils
gp_frame = gp_layer.frames.new(0)
lineSize = 0.015
axisColors = ["ff0000", "00ff00", "0000ff"] #Colors of the XYZ axis

### Functions
def getMeshHash(obj):
    return hashlib.sha224( str(obj.data.vertices).strip('[]').encode('utf-8') ).hexdigest()
    
def createVertexPatch(bmeshObj, vertex):
    return Patch.Patch(bmeshObj, vertex.index, RINGS_NUM)
    
def intToSignedBitList(val, bitsAmount):
    """
    Takes an int as parameter and converts it to a signed bit list (True = -1, False = 1) of size bitsAmount
    """
    return [1-2*bool(val & (1<<j)) for j in range(bitsAmount)]

###Body
#Creating the bmesh
selectedObj = bpy.context.active_object

if selectedObj.type != "MESH":
    raise Exception("Please choose a mesh")
    
bm = bmesh.from_edit_mesh(selectedObj.data)
bm.verts.ensure_lookup_table()
bm.edges.ensure_lookup_table()
bm.faces.ensure_lookup_table()

#Storage for mesh data
meshDataPath = os.path.join(bpy.path.abspath("//"), 'meshesData/{}/'.format(getMeshHash(selectedObj)))
if not os.path.exists(meshDataPath):
    os.makedirs(meshDataPath)

##Covering the mesh with patches
print("===BAKING START===")
meshPatches = []

#Checking in patches were baked/are still up to date
patchesDataPath = os.path.join(meshDataPath, 'patches.pkl')
if os.path.exists(patchesDataPath):
    #Loading binary baked patches file
    print("Baked patches file found in {}. Loading...".format(patchesDataPath))
    with lzma.open(patchesDataPath, 'rb') as f:
        meshPatches = pickle.load(f)  
    
    #Checking equality between two patches for the same mesh
    print("Checking integrity...")
    patchRef = createVertexPatch(bm, bm.verts[0])
    patchBaked = meshPatches[0]
    if pickle.dumps(patchRef) != pickle.dumps(patchBaked):
        print("Outdaded or invalid baked patches found, rebuilding all patches")
        meshPatches = []
    else:
        print("Patch integrity test successful")
    
#Checking if the patchs were correctly loaded
if len(meshPatches) == 0:
    #Patches not found, baking them
    print("Building patches for the mesh")
    start = time.time()
    
    bar = Bar('Creating patches around vertices', max=len(bm.verts))
    for vert in bm.verts:
        meshPatches.append(createVertexPatch(bm, vert))
        bar.next()

    end = time.time()
    print("Time taken : {} seconds".format(end - start))
    
    print("Dumping into a binary file...")
    with lzma.open(patchesDataPath, 'wb') as f:
        pickle.dump(meshPatches, f)
    print("Done")

#Loading sampled textures
if False:
    texturesInfos = []
    Patch.Patch.setupBakingEnvironment(bm)
    patchesTextureFilePath = os.path.join(meshDataPath, 'textures.pkl')

    #Trying to load baked data (if it exists)
    if os.path.exists(patchesTextureFilePath):
        print("Baked textures file found in {}. Loading...".format(patchesTextureFilePath))
        with lzma.open(patchesTextureFilePath, 'rb') as f:
            texturesInfos = pickle.load(f) 
        
        patchRefIdx = 5731
        (meshPatches[patchRefIdx]).bakePatchTexture(bm)
        patchRef = (meshPatches[patchRefIdx]).pixels
        patchBaked = texturesInfos[patchRefIdx]
        
        print("Checking integrity...")
        if pickle.dumps(patchRef) != pickle.dumps(patchBaked):
            print("Outdaded or invalid baked textures found, rebaking all textures")
            texturesInfos = []
        else:
            print("Patch integrity test successful")

    if len(texturesInfos) == 0:#Add here logic for checking whether the texture info of patches is correct
        print("Setting up baking environment...")

        print("Baking patch textures...")

        bar = Bar('Extracting patch textures', max=len(meshPatches))
        for i in range(len(meshPatches)):
            patch = meshPatches[i]
            patch.bakePatchTexture(bm)
            bar.next()
            
        texturesInfos = [meshPatches[i].pixels for i in range(len(meshPatches))]
        
        print("Dumping into a binary file...")
        with lzma.open(patchesTextureFilePath, 'wb') as f:
            pickle.dump(texturesInfos, f)
        print("Done")

    print("Setting texture data...")
    for i in range(len(meshPatches)):
        patch = meshPatches[i]
        patch.pixels = texturesInfos[i]
    print("Done")

#Rest of the logic
print("===LOGIC START===")
print("Drawing the patches' eigenvectors")
for patch in meshPatches:
    patch.drawLRF(gpencil, gp_frame, bm, 0.03, 2.0, 15.0, drawAxis = (True, True, True))

##Low rank recovery
from sklearn.metrics.pairwise import pairwise_kernels
testlib = ctypes.CDLL('/home/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/src/c_utils/libutils.so')
testlib.getDepressedCubicRoots.argtypes = (ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_float))

#Building a KD-tree to find the k nearest neighbours of any point
def getPatchNormalColumnVector(patch):
    return np.concatenate(np.array([patch.sampledNormals[i] for i in range(Patch.Patch.sampleRes**2)]), axis = 0)

#Building the tree
clusterSize = 10
topoFeatures = [patch.eigenVals / np.linalg.norm(patch.eigenVals) for patch in meshPatches]
kdt = KDTree(topoFeatures,  leaf_size = 30, metric = 'euclidean')

#Building the patch matrix for a patch
dists, neighIdx = kdt.query([topoFeatures[0]], k=clusterSize)
neighIdx = neighIdx[0]
patchMatrix = np.zeros((3 * Patch.Patch.sampleRes**2, clusterSize))
for i in range(clusterSize):
    patch = meshPatches[neighIdx[i]]
    patchMatrix[:,i] = getPatchNormalColumnVector(patch)

##Setting ways to compute the matrices
#Kernel params
d = 1
c = 0
#Kernel matrix compute
def getKernelMat(normalsApproxMat, c, d):
    return pairwise_kernels(normalsApproxMat.T, metric = 'poly', degree = d, gamma = 1, coef0 = c)



##Optimizing the matrices (step A and B from the paper)
#Solving low-rank problem (one step starts here)
denoisedNormals = np.copy(patchMatrix)


kernelMatrix = getKernelMat(denoisedNormals, c, d)
u, singVals, vh = np.linalg.svd(kernelMatrix)

#Optimizing C (closed-form solution)
arr = (ctypes.c_float*3)()
tau = 1.0
rho = 20.0
q = tau / (2.0 * rho)

phiVals = np.zeros(clusterSize)
roots = np.zeros(4)
for i in range(clusterSize):
    singVal = singVals[i]
    p = -singVal
    testlib.getDepressedCubicRoots(p, q, arr)
    for j in range(3):
        roots[j] = arr[j]
    
    roots[roots < 0.0] = 0.0
    roots_ = np.unique(roots)
    
    phiVals[i] = roots_[np.argmin([((rho/2.0)*(singVal - root**2.0)**2.0) + (tau * root) for root in roots_])]
    
C = np.diag(phiVals) @ vh

from scipy.optimize import minimize
#Optimizing recovered normals (BCD)

def cost():
    pass