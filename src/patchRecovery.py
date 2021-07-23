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
#Deepcopying
import copy
#Storing test data
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

def retrieveBakedData(bakedDataPath, integrityCheckFunction, sourceDataIdx, dataBakingFunction, receiverArray):
    """
    Handles the loading and, if necessary, sequential rebaking of data with a high computation cost
    """
    rebuiltData = False
    
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
        rebuiltData = True
    
    return rebuiltData


def createBMesh(msh):
    bmsh = bmesh.from_edit_mesh(msh)
    bmsh.verts.ensure_lookup_table()
    bmsh.edges.ensure_lookup_table()
    bmsh.faces.ensure_lookup_table()
    avgEdgeLen = np.average([edge.calc_length() for edge in bmsh.edges])
    return bmsh, avgEdgeLen

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
       
bm, avgEdgeLen = createBMesh(selectedObj.data)

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
    patchRef = createVertexPatch(bakedPatch.centerFaceIdx)
    
    return DeepDiff(patchRef, bakedPatch) == {}

def createVertexPatch(faceIdx):
    return Patch.Patch(bm, bm.faces[faceIdx].index, RINGS_NUM)

meshPatches = []
patchesDataPath = os.path.join(meshDataPath, 'patches.pkl')
retrieveBakedData(patchesDataPath, checkPatchIntegrity, [f.index for f in bm.faces], createVertexPatch, meshPatches)
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
retrieveBakedData(patchesUVMapsPath, checkUVMapIntegrity, list(range(len(meshPatches))), bakeUVMap, UVMaps)
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
rebuiltData = retrieveBakedData(patchesTextureFilePath, checkTextureIntegrity, [i for i in range(len(meshPatches))], bakePatchTexture, texturesInfos)
texturesInfos = texturesInfos[0]

bpy.context.scene.render.engine = prevEngine

print("Setting texture data...")
for i in range(len(meshPatches)):
    patch = meshPatches[i]
    patch.pixels = texturesInfos[i]
print("Done")

print("---Image features---")
imageFeatures = []
imageFeaturesPath = os.path.join(meshDataPath, 'imageFeatures.pkl')

if (not rebuiltData) and os.path.exists(imageFeaturesPath):
    print("Loading baked image features...")
    with gzip.open(imageFeaturesPath, 'rb') as f:
        imageFeatures = pickle.load(f)

if len(imageFeatures) == 0:
    ##Extracting the image features (needs to be done only once)
    print("Extracting patch texture features")
    import tensorflow as tf
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    
    #from tensorflow.keras.applications import VGG16
    #model = VGG16(weights='imagenet', include_top=False, input_shape=(64, 64, 3), pooling="max")
    
    from tensorflow.keras.applications import ResNet50
    model = ResNet50(weights='imagenet', include_top=False, input_shape=(Patch.Patch.bakedImgSize, Patch.Patch.bakedImgSize, 3), pooling="max")
    
    formattedPatchPixels = np.array([np.delete(patch.pixels.reshape([64, 64, 4]), 2, 2) for patch in meshPatches])
    formattedPatchPixels = tf.keras.applications.resnet50.preprocess_input(formattedPatchPixels)

    imageFeatures = []
    #with tf.device('/gpu:0'):
    imageFeatures = model.predict(formattedPatchPixels)
    
    print("Dumping texture features to file...")
    with gzip.open(imageFeaturesPath, 'wb') as f:
        pickle.dump(imageFeatures, f)
    print("Done")


from sklearn.decomposition import PCA

#imageFeatures = KernelPCA(n_components = 20, kernel = 'rbf').fit_transform(imageFeatures)
imageFeatures = PCA(n_components=50).fit_transform(imageFeatures)
imageFeatures = imageFeatures * (1.0 / np.amax(np.linalg.norm(imageFeatures, axis = 1)))

#Rest of the logic
print("===LOGIC START===")

#Utility to export a mesh to a gltf file (to get back on track easily in case of crash)
def exportToObj(objToExp, filepath_):
    for obj in bpy.data.objects:
        obj.select_set(False)
    objToExp.select_set(True)

    matBefore = objToExp.matrix_world.copy()
    objToExp.matrix_world.identity()
    
    bpy.ops.export_scene.obj(
        filepath=filepath_,
        use_selection=True,
        axis_forward='Y', axis_up='Z'
    )
    
    objToExp.matrix_world = matBefore


#Creating/setting folder for mesh outputs
startTimeStamp = int(time.time())
meshName = selectedObj.name + "_" + str(startTimeStamp) + "_{}.obj"
meshFolder = os.path.join(testDataFolderPath, selectedObj.name)
if not os.path.exists(meshFolder):
    os.makedirs(meshFolder)

meshPath = os.path.join(meshFolder, meshName)

#Starting the denoising iterations
ITERS_COUNT = 1
CLUSTER_SIZE = 30
IMAGE_FEATURES_WEIGHT = 10.0
USE_GNF = True

isDone = False
iterNum = -1
while not isDone:
    iterData = {}
    iterNum += 1
    
    startTot = time.time()
    
    print("Iteration number {}".format(iterNum+1))
    ##Topological features
    print("Building the neighborhood system")
    topoFeatures = np.array([patch.eigenVals / np.linalg.norm(patch.eigenVals) for patch in meshPatches])
    allFeatures = np.concatenate((topoFeatures, IMAGE_FEATURES_WEIGHT * imageFeatures), axis = 1)

    #Building the KD-tree
    rankRecoverer = LowRankRecovery.LowRankRecovery()
    kdt = KDTree(allFeatures,  leaf_size = CLUSTER_SIZE, metric = 'euclidean')
    
    ##Performing recovery on each patch
    startLRR = time.time()
    
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
        
        origNormal = np.array(bm.faces[patch.centerFaceIdx].normal)
        patchNormals = np.array([np.average((recoveredMat[:,i]).reshape(Patch.Patch.samplesCount,3), axis = 0) for i in range(CLUSTER_SIZE)])
        patchNormals = patchNormals / np.linalg.norm(patchNormals, axis=1)[:,np.newaxis]
        
        clampedDotProds = np.maximum(-1.0, np.minimum(1.0, np.dot(patchNormals, origNormal)))
        newNormal = patch.eigenVecs @ patchNormals[np.argsort(np.arccos(clampedDotProds))[CLUSTER_SIZE // 2]]
        
        #avg = np.average((recoveredMat[:,0]).reshape(Patch.Patch.samplesCount,3), axis = 0)
        #newNormal = patch.eigenVecs @ (avg / np.linalg.norm(avg))
        
        recoveredNormals[patch.centerFaceIdx] = newNormal 
        bar.next()
    print("\n")
    
    endLRR = time.time()
    iterData['timeLRR'] = endLRR - startLRR
    
    #Applying bilateral normal filtering on the recovered normals
    filteredNormals = {}
    
    if not USE_GNF:
        filteredNormals = recoveredNormals
    else:
        
        startGNF = time.time()
        
        tempNormals = {patch.centerFaceIdx : recoveredNormals[patch.centerFaceIdx] for patch in meshPatches}
        maxItersGNF = 3
        epsGNF = 1e-2
        sigmaS = 2.0 * (0.2)
        sigmaR = 2.0 * (avgEdgeLen)
        
        bar = Bar('Performing normal filtering', max=maxItersGNF)
        iterNumGNF = 0
        while True:
            iterNumGNF += 1
            
            for patch in meshPatches:
                patchCenter = patch.getOrigin(bm)
                patchNormal = tempNormals[patch.centerFaceIdx]
                
                weightedNormals = [bm.faces[neighFaceIdx].calc_area() * math.exp(-(np.linalg.norm(Patch.Patch.getFaceBarycenter(bm.faces[neighFaceIdx]) - patchCenter)**2.0)/sigmaS) * math.exp(-(np.linalg.norm(tempNormals[neighFaceIdx] - patchNormal)**2.0)/sigmaR) * tempNormals[neighFaceIdx] for neighFaceIdx in patch.rings[1]] 
                filteredNormal = np.real(np.sum(weightedNormals, axis = 0))
                
                filteredNormals[patch.centerFaceIdx] = filteredNormal / np.linalg.norm(filteredNormal)
            
            tot = 0.0
            for faceIdx in tempNormals:
                tot += np.linalg.norm(tempNormals[faceIdx] - filteredNormals[faceIdx])
            avgTot = tot / len(meshPatches)
                
            tempNormals = copy.deepcopy(filteredNormals)
            
            print(avgTot)
            
            if avgTot < epsGNF:
                print("Normal filtering converged, stopping")
                break
            elif iterNumGNF == maxItersGNF:
                print("Maximum number of normal filtering iterations reached")
                break
            
            bar.next()
        
        print("\n")
        
        endGNF = time.time()
        iterData['timeGNF'] = endGNF - startGNF
    
    if False:
        #Debug drawing
        for patch in meshPatches:
            centerPosIdx = patch.centerFaceIdx
            centerPos = Patch.Patch.getFaceBarycenter(bm.faces[centerPosIdx])
            dir = filteredNormals[centerPosIdx]
            debugDrawing.draw_line(gpencil, gp_frame, (centerPos, centerPos + 0.02 * dir), (0.5, 3.0), "00ffff")
    
    #Correcting vertex positions
    startPosUpdt = time.time()
    
    newPos = {}

    print("Updating vertex positions")
    for vert in bm.verts:
        vertexPos = np.array(vert.co)
        
        disp = np.array([0.0, 0.0, 0.0])
        
        #Finding every neighbouring vertex by using linked edge
        for neighEdge in vert.link_edges:
            #Finding the neighboring vertex
            otherVert = neighEdge.verts[0 if list(neighEdge.verts)[0] != vert else 1]
            
            #Parsing the faces linked to that edge (and thus also neighboring the central vertex)
            for linkedFace in neighEdge.link_faces:
                faceNormal = filteredNormals[linkedFace.index]
                
                print(recoveredNormals[linkedFace.index])
                print(filteredNormals[linkedFace.index])
                
                disp += faceNormal * np.dot(faceNormal, np.array(otherVert.co) - vertexPos)
        
        disp = (1.0/(3.0 * len(vert.link_faces))) * disp
        
        newPos[vert.index] = vertexPos + disp 

    endPosUpdt = time.time()
    iterData['timePosUdpt'] = endPosUpdt - startPosUpdt

    #Applying new positions
    totChange = 0.0
    vertMoveWeight = {vert.index : 1.0 / sum([face.calc_area() for face in vert.link_faces]) for vert in bm.verts}
    for vert in bm.verts:
        totChange += np.linalg.norm(np.array(vert.co) - newPos[vert.index]) * vertMoveWeight[vert.index]
        vert.co = newPos[vert.index]
    changeRel = (totChange / sum(vertMoveWeight.values())) / len(bm.verts)
    
    iterData['changeRel'] = changeRel
    
    print("Updating mesh representation in Blender...")
    bmesh.update_edit_mesh(bpy.context.active_object.data)
    
    print("Export mesh at this step")
    exportToObj(selectedObj, meshPath.format(iterNum))
    
    if ((iterNum + 1) == ITERS_COUNT):
        print("Maximum number of iterations reached")
        isDone = True
    else:
        #The process is not done or converged yet, we thus update the patches info with the new mesh
        bpy.ops.object.mode_set(mode='EDIT')
        bm, avgEdgeLen = createBMesh(selectedObj.data)
        
        bar = Bar('Updating the patches', max=len(meshPatches))
        for patch in meshPatches:
            patch.computeProperties(bm)
            bar.next()
        print("\n")
        
    endTot = time.time()
    iterData['timeTot'] = endTot - startTot
    
    #Saving the change this iteration for this mesh
    testsData[selectedObj.name].append(iterData)
    
    print("Data this iteration : {}".format(iterData))
    
print("Saving test data...")
with open(testDataJsonPath, 'w') as f:
    json.dump(testsData, f, indent = 4)
    
print("End of script reached")