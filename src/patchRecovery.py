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

def createPatchCorrectionChain(startingPatchIdx):
    dataArr = np.array([patch.eigenVals / np.linalg.norm(patch.eigenVals) for patch in meshPatches])
    correctedPatches = []
    uncorrectedPatches = list(range(len(dataArr)))
    refPatchPairs = []

    start = time.time()

    correctedPatches.append(startingPatchIdx)
    uncorrectedPatches.remove(startingPatchIdx)
    closestPoints, closestDists = pairwise_distances_argmin_min(dataArr[correctedPatches], dataArr[uncorrectedPatches])

    bar = Bar('Building patch connectivity map', suffix='%(percent).1f%%', max=len(uncorrectedPatches) - 1)
    while len(uncorrectedPatches) > 1:
        ##Find the closest uncorrected patch and its ref patch
        closestRelationId = np.argmin(closestDists)
        refPatchIdx = correctedPatches[closestRelationId]
        patchToCorrectIdx = closestPoints[closestRelationId]
        refPatchPairs.append((refPatchIdx, patchToCorrectIdx))
        uncorrectedPatches.remove(patchToCorrectIdx)
        ##Creating a new row for the new patch, with empty data
        closestPoints = np.append(closestPoints, -1)
        closestDists = np.append(closestDists, 0.0)
        correctedPatches.append(patchToCorrectIdx)
        #print("Closest ref : {}, closest uncorrected patch : {} (remaining uncorrected patches : {})".format(refPatchIdx, patchToCorrectIdx, len(uncorrectedPatches)))
        ##Finding nearest neighbours for the corrected points that used to have the new point as their nearest neighbour
        #Locating the patches with refPatchIdx as their nearest neighbour
        patchesObsNearstNeighbPos = np.where(closestPoints == patchToCorrectIdx)[0]
        patchesObsNearstNeighbPos = np.append(patchesObsNearstNeighbPos, len(correctedPatches)-1)
        patchesObsNearstNeighbIdx = np.array(correctedPatches)[patchesObsNearstNeighbPos]
        #Finding new nearest neighbours of those patches, registering the relevant statistics
        newPatchClosestPoints, newPatchClosestDists = pairwise_distances_argmin_min(dataArr[patchesObsNearstNeighbIdx], dataArr[uncorrectedPatches])
        for i in range(len(patchesObsNearstNeighbPos)):
            closestPoints[patchesObsNearstNeighbPos[i]] = uncorrectedPatches[newPatchClosestPoints[i]]
            closestDists[patchesObsNearstNeighbPos[i]] = newPatchClosestDists[i]
        bar.next()

    refPatchPairs.append((correctedPatches[np.argmin(closestDists)], uncorrectedPatches[0]))

    end = time.time()

    print("Total time : ", end - start)
    
    return refPatchPairs

def patchesAxisSignMatching(patchRef, patchToCorrect, bmeshObj):
    vertices1Pos = patchRef.getVerticesPos(bmeshObj)
    patch1RefPos = patchRef.getCentralPos(bmeshObj)
    #Transforming the vertices position for patchRef
    vertices1Pos = (patchRef.rotMatInv @ (vertices1Pos - patch1RefPos).T).T
    
    vertices2Pos = patchToCorrect.getVerticesPos(bmeshObj)
    patch2RefPos = patchToCorrect.getCentralPos(bmeshObj)
    #Centering the vertices of patch to correct
    vertices2Pos = vertices2Pos - patch2RefPos
    
    matchingResults = []
    for i in range(NUMBER_OF_SIGN_COMBINATION):
        signsList = intToSignedBitList(i, COLUMNS_SIGN_MODIFIED) #Signs of the columns that we will switch
        mat = np.copy(patchToCorrect.eigenVecs)
        #Applying the sign changes
        for colId in range(COLUMNS_SIGN_MODIFIED):
            mat[:,colId] = signsList[colId] * mat[:,colId]
        #Transforming the vertices
        rotMatInv = np.linalg.inv(mat)
        vertices2PosTransformed = (rotMatInv @ vertices2Pos.T).T
        
        #Measuring the difference between the transformed patches
        closestPoints, closestDists = pairwise_distances_argmin_min(vertices2PosTransformed, vertices1Pos, metric = 'sqeuclidean')
        matchingResults.append(closestDists.sum())
    
    bestCombinationIdx = 3#np.argmin(matchingResults)
    signsList = intToSignedBitList(bestCombinationIdx, COLUMNS_SIGN_MODIFIED)
    
    for colId in range(COLUMNS_SIGN_MODIFIED):
        patchToCorrect.eigenVecs[:,colId] = signsList[colId] * patchToCorrect.eigenVecs[:,colId]
    patchToCorrect.rotMatInv = np.linalg.inv(patchToCorrect.eigenVecs)

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
    
    #Launching a procedure to correct the orientation of the patches' eigenvectors
    #refPatchChain = createPatchCorrectionChain(0)
        
    print("Starting to correct the patches' signs...")

    start = time.time()

    #for couple in refPatchChain:
    #    patchesAxisSignMatching(meshPatches[couple[0]], meshPatches[couple[1]], bm)

    end = time.time()
    print("Time taken : {} seconds".format(end - start))
    
    
    print("Dumping into a binary file...")
    with lzma.open(patchesDataPath, 'wb') as f:
        pickle.dump(meshPatches, f)
    print("Done")

#Loading sampled textures
texturesInfos = []
Patch.Patch.setupBakingEnvironment(bm)
patchesTextureFilePath = os.path.join(meshDataPath, 'textures.pkl')

#Trying to load baked data (if it exists)
if os.path.exists(patchesTextureFilePath):
    print("Baked textures file found in {}. Loading...".format(patchesTextureFilePath))
    with lzma.open(patchesTextureFilePath, 'rb') as f:
        texturesInfos = pickle.load(f) 
    
    (meshPatches[0]).bakePatchTexture(bm)
    patchRef = (meshPatches[0]).pixels
    patchBaked = texturesInfos[0]
    
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

#Solving low-rank problem
denoisedNormals = np.copy(patchMatrix)

from sklearn.metrics.pairwise import pairwise_kernels

kernelMatrix = pairwise_kernels(denoisedNormals.T, metric = 'poly', degree = 1, gamma = 1, coef0 = 1)
u, s, vh = np.linalg.svd(kernelMatrix)
