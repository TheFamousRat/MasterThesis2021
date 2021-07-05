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
#
from deepdiff import DeepDiff

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

#cleaning loose geometry    
bpy.ops.mesh.select_mode(type='VERT') 
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.delete_loose()
bpy.ops.mesh.select_all(action='DESELECT')
       

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
    patchIdx = 0
    patchRef = createVertexPatch(bm, bm.verts[patchIdx])
    patchBaked = meshPatches[patchIdx]
    
    if DeepDiff(patchRef, patchBaked) != {}:
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
    
    #meshPatches = [patch for patch in meshPatches if patch.isValid]
    
    print("Dumping into a binary file...")
    with lzma.open(patchesDataPath, 'wb') as f:
        pickle.dump(meshPatches, f)
    print("Done")

#Loading sampled texturesz
texturesInfos = []
Patch.Patch.setupBakingEnvironment(bm)
patchesTextureFilePath = os.path.join(meshDataPath, 'textures.pkl')

#Trying to load baked data (if it exists)
if os.path.exists(patchesTextureFilePath):
    print("Baked textures file found in {}. Loading...".format(patchesTextureFilePath))
    with lzma.open(patchesTextureFilePath, 'rb') as f:
        texturesInfos = pickle.load(f) 
    
    print("Checking integrity...")
    patchRefIdx = 0
    (meshPatches[patchRefIdx]).bakePatchTexture(bm)
    patchRef = np.array((meshPatches[patchRefIdx]).pixels)
    patchBaked = np.array(texturesInfos[patchRefIdx])
    
    if DeepDiff(patchRef, patchBaked) != {}:
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
        print(patch.centerVertexIdx)
        patch.bakePatchTexture(bm)
        bar.next()
        
    texturesInfos = np.array([meshPatches[i].pixels for i in range(len(meshPatches))])
    
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

bpy.ops.mesh.select_all(action='DESELECT')
patchIdx = 518
patch = meshPatches[patchIdx]
for vertIdx in patch.verticesIdxList:
    bm.verts[vertIdx].select = True
bpy.data.images['bakedImage'].pixels = list(patch.pixels[:])

##Low rank recovery
from sklearn.metrics.pairwise import pairwise_kernels
testlib = ctypes.CDLL('/home/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/src/c_utils/libutils.so')
testlib.getDepressedCubicRoots.argtypes = (ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_float))

#Building a KD-tree to find the k nearest neighbours of any point
def getPatchNormalColumnVector(patch):
    return np.concatenate(np.array([patch.sampledNormals[i] for i in range(Patch.Patch.sampleRes**2)]), axis = 0)

#Building the tree
clusterSize = 20
topoFeatures = [patch.eigenVals / np.linalg.norm(patch.eigenVals) for patch in meshPatches]
kdt = KDTree(topoFeatures,  leaf_size = 30, metric = 'euclidean')

#Building the patch matrix for a patch
patchIdx = 34
dists, neighIdx = kdt.query([topoFeatures[patchIdx]], k=clusterSize)
neighIdx = neighIdx[0]
patchMatrix = np.zeros((3 * Patch.Patch.sampleRes**2, clusterSize))
for i in range(clusterSize):
    patch = meshPatches[neighIdx[i]]
    patchMatrix[:,i] = getPatchNormalColumnVector(patch)

print(np.linalg.norm(patchMatrix, ord = 'nuc'))

##Setting ways to compute the matrices
#Kernel params
d = 2.0
c = 1.0
invD = (d-1)/d
#Subproblems params
tau = 1.0
rho = 20.0
lambd = 0.5
q = tau / (2.0 * rho)
alpha = rho / lambd
#Kernel matrix compute
#Note : the letter 'o' is here to indicate "all elements" (of the row or the column), not as the letter 
def getKernelMat(normalsApproxMat, c, d):
    return pairwise_kernels(normalsApproxMat.T, metric = 'poly', degree = d, gamma = 1, coef0 = c)

def getCost(a_oi, i, patchMatLowRank, patchMat, CtC, alpha):
    patchMatLowRank[:,i] = a_oi
    K = pairwise_kernels([a_oi], patchMatLowRank.T, metric = 'poly', degree = d, gamma = 1, coef0 = c)[0]
    
    D = CtC[i,:] - K
    
    return (np.linalg.norm(a_oi - patchMat[:,i])**2) + (alpha/2.0)*(np.linalg.norm(D)**2)

def getGrad(a_oi, i, patchMatLowRank, patchMat, CtC, alpha):
    patchMatLowRank[:,i] = a_oi
    K = pairwise_kernels([a_oi], patchMatLowRank.T, metric = 'poly', degree = d, gamma = 1, coef0 = c)[0]
    
    D = CtC[i,:] - K
    
    P = np.power(K, invD)
    P[i] = 2.0 * P[i]
    
    H = np.multiply(P, D)
    
    return 2.0 * (a_oi - patchMat[:,i]) - alpha*d*(patchMatLowRank @ H)

def getSubProbALoss(denoised, original, CtC):
    return np.linalg.norm(denoised - original, ord = 'fro') + ((alpha/2.0)*np.linalg.norm(CtC - getKernelMat(denoised, c, d), ord = 'fro'))

def getSubProbALoss(kernMatProd, kernMat):
    np.linalg.norm(kernMatProd, ord = 'nuc')
    (rho/2.0)*np.linalg.norm()        
    return np.linalg.norm(denoised - original, ord = 'fro') + ((alpha/2.0)*np.linalg.norm(CtC - getKernelMat(denoised, c, d), ord = 'fro'))

##Optimizing the matrices (step A and B from the paper)
#Solving low-rank problem (one step starts here)
denoisedNormals = np.copy(patchMatrix)
for j in range(100):
    #Optimizing C (closed-form solution)
    kernelMatrix = getKernelMat(denoisedNormals, c, d)
    u, singVals, vh = np.linalg.svd(kernelMatrix)

    arr = (ctypes.c_float*3)()

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
    CtC = C.T @ C

    #Conducting BGD to optimize A
    prevLoss = getSubProbALoss(denoisedNormals, patchMatrix, CtC)
    idxList = list(range(clusterSize))
    lossDiff = float('inf')
    while lossDiff > 1e-3:
        np.random.shuffle(idxList)
        for i in idxList:
            x0 = denoisedNormals[:,i]
            res = minimize(getCost, x0, 
                    args = (i,  denoisedNormals, patchMatrix, CtC, alpha), 
                    jac = getGrad,
                    method = "L-BFGS-B")
            denoisedNormals[:,i] = np.copy(res.x)
        
        newLoss = getSubProbALoss(denoisedNormals, patchMatrix, CtC)
        lossDiff = prevLoss - newLoss
        prevLoss = newLoss
        print("Yeah {}".format(lossDiff))

    print(np.linalg.norm(denoisedNormals, ord = 'nuc') + lambd * np.linalg.norm(denoisedNormals - patchMatrix))

