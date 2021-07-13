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
#Blender libs
import bpy
import bmesh
#Hashing utilities for mesh unique identification
import hashlib
#C communication
import ctypes
#Scikit suite
import numpy as np
from sklearn.neighbors import KDTree
from sklearn.decomposition import KernelPCA
#Show progress bar utility
from progress.bar import Bar
#Deep difference for object instance matching
from deepdiff import DeepDiff
#Multithreading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

##Local libraries (re-)loading
#Loading user-defined modules (subject to frequent changes and needed reloading)
pathsToAdd = ["/home/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/src"]

for pathToAdd in pathsToAdd:
    sys.path.append(pathToAdd)

import Patch
import debugDrawing
import LowRankRecovery

import importlib
importlib.reload(Patch)
importlib.reload(debugDrawing)
importlib.reload(LowRankRecovery)

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

def intToSignedBitList(val, bitsAmount):
    """
    Takes an int as parameter and converts it to a signed bit list (True = -1, False = 1) of size bitsAmount
    """
    return [1-2*bool(val & (1<<j)) for j in range(bitsAmount)]

def retrieveBakedData(bakedDataPath, integrityCheckFunction, sourceDataIdx, dataBakingFunction, receiverArray):
    """
    
    
    """
    if os.path.exists(bakedDataPath):
        retrievedData = []
        print("Baked data file found in {}. Loading...".format(bakedDataPath))
        with lzma.open(bakedDataPath, 'rb') as f:
            retrievedData = pickle.load(f) 
        
        print("Checking integrity...")
        refIdx = 0
        integrityCheckSuccess = integrityCheckFunction(refIdx, retrievedData[refIdx])
        
        if integrityCheckSuccess:
            print("Baked data integrity test successful")
            receiverArray.append(np.array(retrievedData))
        else:
            print("Outdaded or invalid baked data found, rebaking for all data")
    
    if len(receiverArray) == 0:
        bakedData = [None] * len(sourceDataIdx)
        
        bar = Bar('Baking...', max=len(sourceDataIdx))
        for dataIdx in sourceDataIdx:
            bakedData[dataIdx] = dataBakingFunction(dataIdx)
            bar.next()
        
        print("Dumping into a binary file...")
        with lzma.open(bakedDataPath, 'wb') as f:
            pickle.dump(bakedData, f)
        print("Done")
        
        receiverArray.append(np.array(bakedData))

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
usedBmesh = bm

#Storage for mesh data
meshDataPath = os.path.join(bpy.path.abspath("//"), 'meshesData/{}/'.format(getMeshHash(selectedObj)))
if not os.path.exists(meshDataPath):
    os.makedirs(meshDataPath)

##Covering the mesh with patches
print("===BAKING START===")
print("---Patches creation---")
def checkPatchIntegrity(patchIdx, bakedPatch):
    patchRef = createVertexPatch(bakedPatch.centerVertexIdx)
    
    return DeepDiff(patchRef, bakedPatch) == {}

def createVertexPatch(vertIdx):
    return Patch.Patch(bm, bm.verts[vertIdx].index, RINGS_NUM)

meshPatches = []
patchesDataPath = os.path.join(meshDataPath, 'patches.pkl')
retrieveBakedData(patchesDataPath, checkPatchIntegrity, [v.index for v in bm.verts], createVertexPatch, meshPatches)
meshPatches = meshPatches[0]

#UV map
print("---UV map---")
def checkUVMapIntegrity(patchIdx, bakedUVMap):
    patchRef = meshPatches[patchIdx]
    patchRef.createCenteredUVMap(bm)
    
    return DeepDiff(patchRef.verticesUVs, bakedUVMap) == {}

def bakeUVMap(patchIdx):
    patch = meshPatches[patchIdx]
    patch.createCenteredUVMap(bm)
    return patch.verticesUVs

UVMaps = []
patchesUVMapsPath = os.path.join(meshDataPath, 'UVMaps.pkl')
retrieveBakedData(patchesUVMapsPath, checkUVMapIntegrity, [v.index for v in bm.verts], bakeUVMap, UVMaps)
UVMaps = UVMaps[0]

print("Applying loaded maps")
for i in range(len(meshPatches)):
    patch = meshPatches[i]
    patch.verticesUVs = UVMaps[i]
print("Done")

#Textures
print("---Textures sampling---")
Patch.Patch.setupBakingEnvironment(bm)

def checkTextureIntegrity(patchIdx, bakedTexturePixels):
    patchRef = meshPatches[patchIdx]
    patchRef.bakePatchTexture(bm)
    
    return DeepDiff(np.array(patchRef.pixels), np.array(bakedTexturePixels)) == {}

def bakePatchTexture(patchIdx):
    patch = meshPatches[patchIdx]
    patch.bakePatchTexture(bm)
    return patch.pixels

texturesInfos = []
patchesTextureFilePath = os.path.join(meshDataPath, 'textures.pkl')
retrieveBakedData(patchesTextureFilePath, checkTextureIntegrity, [i for i in range(len(meshPatches))], bakePatchTexture, texturesInfos)
texturesInfos = texturesInfos[0]

print("Setting texture data...")
for i in range(len(meshPatches)):
    patch = meshPatches[i]
    patch.pixels = texturesInfos[i]
print("Done")

#Rest of the logic
print("===LOGIC START===")

##Low rank recovery
testlib = ctypes.CDLL('/home/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/src/c_utils/libutils.so')
testlib.getDepressedCubicRoots.argtypes = (ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_float))

#Building a KD-tree to find the k nearest neighbours of any point
def getPatchNormalColumnVector(patch):
    return np.concatenate(np.array([patch.sampledNormals[i] for i in range(Patch.Patch.sampleRes**2)]), axis = 0)

###Building the feature vectors
##Topological features
topoFeatures = np.array([patch.eigenVals / np.linalg.norm(patch.eigenVals) for patch in meshPatches])

##Extracting the image features
if False:
    import tensorflow as tf
    from tensorflow.keras.applications import VGG16
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context
    model = VGG16(weights='imagenet', include_top=False, input_shape=(64, 64, 3), pooling="max")

    formattedPatchPixels = [np.delete(patch.pixels.reshape([1, 64, 64, 4]), 3, 3) for patch in meshPatches]

    allPixels = np.concatenate(formattedPatchPixels)
    allPixels = tf.convert_to_tensor(allPixels, dtype = tf.float32)
    allPixels = ((allPixels / 255.0) * 2.0) - 1.0

    imageFeatures = []
    with tf.device('/gpu:0'):
        imageFeatures = model.predict(allPixels)

    imageFeatures = KernelPCA(n_components = 10, kernel = 'rbf').fit_transform(imageFeatures)


##Building the KDtree
kdt = KDTree(topoFeatures, leaf_size = 80, metric = 'euclidean')
clusterSize = 80

patchIdx = 0
dists, neighIdx = kdt.query([topoFeatures[patchIdx]], k=clusterSize)
print(neighIdx)

raise Exception("prout")



##Performing recovery on each patch
kdt = KDTree(topoFeatures,  leaf_size = 40, metric = 'euclidean')
rankRecoverer = LowRankRecovery.LowRankRecovery()
clusterSize = 40

newNormals = {}

bar = Bar('Performing low-rank recovery', max=len(meshPatches))
for patchIdx in range(len(meshPatches)):
    patch = meshPatches[patchIdx]
    #Building the patch matrix
    dists, neighIdx = kdt.query([topoFeatures[patchIdx]], k=clusterSize)
    neighIdx = neighIdx[0]
    patchMatrix = np.zeros((3 * Patch.Patch.sampleRes**2, clusterSize))
    for i in range(clusterSize):
        neighbourPatch = meshPatches[neighIdx[i]]
        patchMatrix[:,i] = getPatchNormalColumnVector(neighbourPatch)
    
    #Performing low-rank recovery
    E = rankRecoverer.recoverLowRank(patchMatrix)
    patchRecCol = (patchMatrix - E)[:,0]
    
    #Recovering a normal for the central vertex
    patchRecNormals = np.array([[patchRecCol[x*3 + i] for i in range(3)] for x in range(len(patchRecCol) // 3)])
    patchRecNormals = (1.0 / np.linalg.norm(patchRecNormals, axis = 1))[:, np.newaxis] * patchRecNormals #Normalizing the normals
    
    #Current normal of the central patch vertex
    patchCenterPos = np.array(bm.verts[patch.centerVertexIdx].co)
    centralNormal = patch.eigenVecs[:,2]
    centralNormal = centralNormal / np.linalg.norm(centralNormal)
    
    #Averaging normals to get new normals
    angles = [math.acos(np.dot(centralNormal, normal)) for normal in patchRecNormals]
    avg = np.average(patchRecNormals, axis = 0) 
    newNormal = patch.eigenVecs @ (avg / np.linalg.norm(avg))
    
    newNormals[patch.centerVertexIdx] = newNormal 
    bar.next()
    
raise Exception("Prout")

#Correcting vertex positions
newPos = {}

print("Updating vertex positions")
for patch in meshPatches:
    centerVert = bm.verts[patch.centerVertexIdx]
    centerVertexPos = np.array(centerVert.co)
    
    disp = np.array([0.0, 0.0, 0.0])
    
    for neighFace in centerVert.link_faces:
        faceBarycenter = np.array(neighFace.calc_center_median())
        faceNormal = np.array([0.0, 0.0, 0.0])
        for faceVertNum in range(3):
            faceVertIdx = neighFace.verts[faceVertNum].index
            faceNormal += newNormals[faceVertIdx] * math.exp(-np.linalg.norm(faceBarycenter - np.array(bm.verts[faceVertIdx].co)))
        faceNormal = faceNormal / np.linalg.norm(faceNormal)
        
        sharedEdges = [edge for edge in neighFace.edges if (centerVert in list(edge.verts))]
        
        for edge in sharedEdges:
            otherVert = edge.verts[0 if list(neighFace.edges[1].verts)[0] != centerVert else 1]
            disp += faceNormal * np.dot(faceNormal, np.array(otherVert.co) - centerVertexPos)
    
    disp = (1.0/(3.0 * len(centerVert.link_faces))) * disp
    
    newPos[patch.centerVertexIdx] = centerVertexPos + disp 

#Applying new positions
for vIdx in newPos:
    bm.verts[vIdx].co = newPos[vIdx]
    
bmesh.update_edit_mesh(bpy.context.active_object.data)