###Loading libraries
##Pip/standard libraries loading
#Python standard libraries
import os
import sys
import time
import math
#To compress mesh data files efficiently
import pickle
import gzip
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

import json

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

import gc
gc.collect()

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

def retrieveBakedData(bakedDataPath, integrityCheckFunction, sourceDataIdx, dataBakingFunction, receiverArray, dumpToFile = True):
    """
    
    
    """
    if os.path.exists(bakedDataPath):
        retrievedData = []
        print("Baked data file found in {}. Loading...".format(bakedDataPath))
        with gzip.open(bakedDataPath, 'rb') as f:
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
        
        print("\nDumping into a binary file...")
        with gzip.open(bakedDataPath, 'wb') as f:
            pickle.dump(bakedData, f)
        print("Done")
        
        receiverArray.append(np.array(bakedData))

def createBMesh(msh):
    bmsh = bmesh.from_edit_mesh(msh)
    bmsh.verts.ensure_lookup_table()
    bmsh.edges.ensure_lookup_table()
    bmsh.faces.ensure_lookup_table()
    return bmsh

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
       
bm = createBMesh(selectedObj.data)

#Storage for mesh data
basedir = bpy.path.abspath("//")
meshDataPath = os.path.join(basedir, 'meshesData/{}/'.format(getMeshHash(selectedObj)))
if not os.path.exists(meshDataPath):
    os.makedirs(meshDataPath)

#Storage for test data
testDataFolderPath = os.path.join(basedir, 'testing')
if not os.path.exists(testDataFolderPath):
    os.makedirs(testDataFolderPath)

testDataJsonPath = os.path.join(testDataFolderPath, 'testsResults.json')

testsData = None
if os.path.exists(testDataJsonPath):
    with open(testDataJsonPath, 'r') as f:
        testsData = json.load(f)
else:
    testsData = {}

if not selectedObj.name in testsData:
        testsData[selectedObj.name] = []

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
    
    return pickle.dumps(patchRef.verticesUVs) == pickle.dumps(bakedUVMap)

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

def checkTextureIntegrity(patchIdx, bakedTexturePixels):
    patchRef = meshPatches[patchIdx]
    patchRef.bakePatchTexture(bm)
    
    return DeepDiff(np.array(patchRef.pixels), np.array(bakedTexturePixels)) == {}

def bakePatchTexture(patchIdx):
    patch = meshPatches[patchIdx]
    patch.bakePatchTexture(bm)
    return patch.pixels

prevEngine = bpy.context.scene.render.engine

Patch.Patch.setupBakingEnvironment(bm)

texturesInfos = []
patchesTextureFilePath = os.path.join(meshDataPath, 'textures.pkl')
retrieveBakedData(patchesTextureFilePath, checkTextureIntegrity, [i for i in range(len(meshPatches))], bakePatchTexture, texturesInfos)
texturesInfos = texturesInfos[0]

bpy.context.scene.render.engine = prevEngine

print("Setting texture data...")
for i in range(len(meshPatches)):
    patch = meshPatches[i]
    patch.pixels = texturesInfos[i]
print("Done")

#Rest of the logic
print("===LOGIC START===")

##Extracting the image features (needs to be done only once)
print("Extracting patch texture features")
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
#with tf.device('/gpu:0'):
imageFeatures = model.predict(allPixels)

imageFeatures = KernelPCA(n_components = 20, kernel = 'rbf').fit_transform(imageFeatures)
imageFeatures = imageFeatures * (1.0 / np.amax(np.linalg.norm(imageFeatures, axis = 1)))

#Function to estimate face normal based on vertex normals
def getFaceNormal(face, vertNormals):
    faceBarycenter = Patch.Patch.getFaceBarycenter(face)
    ret = np.average([vertNormals[vert.index] * math.exp(-10.0 * np.linalg.norm(faceBarycenter - np.array(vert.co))**2) for vert in face.verts], axis = 0)
    return ret / np.linalg.norm(ret)

#Utility to export a mesh to a gltf file (to get back on track easily in case of crash)
def exportToGltf(object, filepath_):
    for obj in bpy.data.objects:
        obj.select_set(False)
    object.select_set(True)

    bpy.ops.export_scene.gltf(
        filepath=filepath_,
        export_selected=True,
        use_selection=True
    )

#Starting the denoising iterations
ITERS_COUNT = 5
CLUSTER_SIZE = 30
IMAGE_FEATURES_WEIGHT = 0.0
USE_GNF = True

for iterNum in range(ITERS_COUNT):
    print("Iteration number {}".format(iterNum+1))
    ##Topological features
    print("Building the neighborhood system")
    topoFeatures = np.array([patch.eigenVals / np.linalg.norm(patch.eigenVals) for patch in meshPatches])
    allFeatures = np.concatenate((topoFeatures, IMAGE_FEATURES_WEIGHT * imageFeatures), axis = 1)

    #Building the KD-tree
    rankRecoverer = LowRankRecovery.LowRankRecovery()
    kdt = KDTree(allFeatures,  leaf_size = CLUSTER_SIZE, metric = 'euclidean')
    
    ##Performing recovery on each patch
    recoveredNormals = {}
    bar = Bar('Performing low-rank recovery', max=len(meshPatches))
    for patchIdx in range(len(meshPatches)):
        patch = meshPatches[patchIdx]
        #Building the patch matrix
        dists, neighIdx = kdt.query([allFeatures[patchIdx]], k = CLUSTER_SIZE)
        neighIdx = neighIdx[0]
        patchMatrix = np.zeros((3 * Patch.Patch.samplesCount, CLUSTER_SIZE))
        for i in range(CLUSTER_SIZE):
            neighbourPatch = meshPatches[neighIdx[i]]
            patchMatrix[:,i] = neighbourPatch.sampledNormals.reshape((Patch.Patch.samplesCount*3))
        
        #Performing low-rank recovery
        E = rankRecoverer.recoverLowRank(patchMatrix)
        recoveredMat = patchMatrix - E
        
        origNormal = np.array(bm.verts[patch.centerVertexIdx].normal)
        patchNormals = np.array([np.average((recoveredMat[:,i]).reshape(Patch.Patch.samplesCount,3), axis = 0) for i in range(CLUSTER_SIZE)])
        newNormal = patch.eigenVecs @ patchNormals[np.argsort(np.arccos(np.dot(patchNormals, origNormal)))[CLUSTER_SIZE // 2]]
        
        #avg = np.average((recoveredMat[:,0]).reshape(Patch.Patch.samplesCount,3), axis = 0)
        #newNormal = patch.eigenVecs @ (avg / np.linalg.norm(avg))
        
        recoveredNormals[patch.centerVertexIdx] = newNormal 
        bar.next()
    print("\n")
    
    #Applying bilateral normal filtering on the recovered normals
    print("Performing normal filtering...")
    filteredNormals = {}
    
    if not USE_GNF:
        filteredNormals = recoveredNormals
    else:
        for patch in meshPatches:
            centerVert = bm.verts[patch.centerVertexIdx]
            centerVertNormal = recoveredNormals[centerVert.index]
            centerVertPos = np.array(centerVert.co)
            filteredNormal = np.zeros((3))
            
            for neighFace in centerVert.link_faces:
                faceBary = Patch.Patch.getFaceBarycenter(neighFace)
                faceNormal = getFaceNormal(neighFace, recoveredNormals)
                filteredNormal += neighFace.calc_area() * math.exp(-np.linalg.norm(faceBary - centerVertPos)) * math.exp(-np.linalg.norm(faceNormal - centerVertNormal)) * faceNormal
                
            filteredNormals[centerVert.index] = filteredNormal / np.linalg.norm(filteredNormal)
    
    #Debug drawing
    #for patch in meshPatches:
    #    centerVert = bm.verts[patch.centerVertexIdx]
    #    centerVertPos = np.array(centerVert.co)
    #    dir = filteredNormals[centerVert.index]
    #    debugDrawing.draw_line(gpencil, gp_frame, (centerVertPos, centerVertPos + 0.02 * dir), (0.5, 3.0), "00ffff")
    
    #raise Exception("Test")
    
    #Correcting vertex positions
    newPos = {}

    print("Updating vertex positions")
    for patch in meshPatches:
        centerVert = bm.verts[patch.centerVertexIdx]
        centerVertexPos = np.array(centerVert.co)
        
        disp = np.array([0.0, 0.0, 0.0])
        
        #Finding every neighbouring vertex by using linked edge
        for neighEdge in centerVert.link_edges:
            #Finding the neighboring vertex
            otherVert = neighEdge.verts[0 if list(neighEdge.verts)[0] != centerVert else 1]
            
            #Parsing the faces linked to that edge (and thus also neighboring the central vertex)
            for linkedFace in neighEdge.link_faces:
                faceBarycenter = np.array(linkedFace.calc_center_median())
                faceNormal = getFaceNormal(linkedFace, filteredNormals)
                
                disp += faceNormal * np.dot(faceNormal, np.array(otherVert.co) - centerVertexPos)
        
        disp = (1.0/(3.0 * len(centerVert.link_faces))) * disp
        
        newPos[patch.centerVertexIdx] = centerVertexPos + disp 

    #Applying new positions
    totChange = 0.0
    for patch in meshPatches:
        vIdx = patch.centerVertexIdx
        totChange += np.linalg.norm(np.array(bm.verts[vIdx].co) - newPos[vIdx]) / patch.totalArea
        bm.verts[vIdx].co = newPos[vIdx]
    changeRel = totChange / len(bm.verts)
    print("Change per vertex : {}".format(changeRel))
    
    #Saving the change this iteration for this mesh
    testsData[selectedObj.name].append(changeRel)
    
    print("Updating mesh representation in Blender...")
    bmesh.update_edit_mesh(bpy.context.active_object.data)
    
    print("Export mesh at this step")
    exportName = "{}_backup.glb".format(selectedObj.name, iterNum)
    exportPath = os.path.join(testDataFolderPath, exportName)
    exportToGltf(selectedObj, exportPath)
    
    print("Checking convergence")
    converged = ((iterNum + 1) == ITERS_COUNT)
    
    if converged:
        print("Convergence reached")
        break
    else:
        #The process is not done or converged yet, we thus update the patches info with the new mesh
        bpy.ops.object.mode_set(mode='EDIT')
        bm = createBMesh(selectedObj.data)
        
        bar = Bar('Updating the patches', max=len(meshPatches))
        for patch in meshPatches:
            patch.computeProperties(bm)
            bar.next()
        print("\n")
    
print("Saving test data...")
with open(testDataJsonPath, 'w') as f:
    json.dump(testsData, f, indent = 4)
    
print("End of script reached")