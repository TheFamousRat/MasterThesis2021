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
#Show progress bar utility
from progress.bar import Bar
#Deep difference for object instance matching
from deepdiff import DeepDiff
#Multithreading
from concurrent.futures import ThreadPoolExecutor

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

###Classes (for multithreading mostly)
class PatchBuilder:
    def __init__(self, bmeshObj_):
        self.bmeshObj = bmeshObj_
        
    def createVertexPatch(self, vertIdx):
        return Patch.Patch(self.bmeshObj, self.bmeshObj.verts[vertIdx].index, RINGS_NUM)

### Functions
def getMeshHash(obj):
    return hashlib.sha224( str(obj.data.vertices).strip('[]').encode('utf-8') ).hexdigest()

def intToSignedBitList(val, bitsAmount):
    """
    Takes an int as parameter and converts it to a signed bit list (True = -1, False = 1) of size bitsAmount
    """
    return [1-2*bool(val & (1<<j)) for j in range(bitsAmount)]

def buildMeshPatches(patchBuilder):
    #Preparing the building
    meshPatches_ = [None] * len(patchBuilder.bmeshObj.verts)
    poolData = [vert.index for vert in patchBuilder.bmeshObj.verts]
    
    #Multithreaded building
    bar = Bar('Creating patches around vertices', max=len(poolData))
    with ThreadPoolExecutor(max_workers = 4) as executor:
        for res in executor.map(patchBuilder.createVertexPatch, poolData):
            meshPatches_[res.centerVertexIdx] = res
            bar.next()
            
    return meshPatches_

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
patchBuilder = PatchBuilder(bm)

#Checking in patches were baked/are still up to date
patchesDataPath = os.path.join(meshDataPath, 'patches.pkl')
if os.path.exists(patchesDataPath):
    #Loading binary baked patches file
    print("Baked patches file found in {}. Loading...".format(patchesDataPath))
    with lzma.open(patchesDataPath, 'rb') as f:
        meshPatches = pickle.load(f)  
    
    #Checking equality between two patches for the same mesh
    print("Checking integrity...")
    patchBaked = meshPatches[0]
    patchRef = patchBuilder.createVertexPatch(patchBaked.centerVertexIdx)
    
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
    
    #Building the patches
    meshPatches = buildMeshPatches(patchBuilder)
    
    end = time.time()
    print("\nTime taken : {} seconds".format(end - start))
    
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


#Loading image features


#Rest of the logic
print("===LOGIC START===")
#print("Drawing the patches' eigenvectors")
#for patch in meshPatches:
#    patch.drawLRF(gpencil, gp_frame, bm, 0.03, 2.0, 15.0, drawAxis = (True, True, True))

#bpy.ops.mesh.select_all(action='DESELECT')
#patchIdx = 518
#patch = meshPatches[patchIdx]
#for vertIdx in patch.verticesIdxList:
#    bm.verts[vertIdx].select = True
#bpy.data.images['bakedImage'].pixels = list(patch.pixels[:])

##Low rank recovery
testlib = ctypes.CDLL('/home/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/src/c_utils/libutils.so')
testlib.getDepressedCubicRoots.argtypes = (ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_float))

#Building a KD-tree to find the k nearest neighbours of any point
def getPatchNormalColumnVector(patch):
    return np.concatenate(np.array([patch.sampledNormals[i] for i in range(Patch.Patch.sampleRes**2)]), axis = 0)

#Building the feature vectors
#Topological features
topoFeatures = [patch.eigenVals / np.linalg.norm(patch.eigenVals) for patch in meshPatches]

start = time.time()

for patch in meshPatches:
    patch.createCenteredUVMap(bm)

end = time.time()
print(end - start)

Patch.Patch.setupBakingEnvironment(bm)
meshPatches[0].bakePatchTexture(bm)

#Extracting the image features
if False:
    import tensorflow as tf
    from keras.applications import vgg16
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context
    model = vgg16.VGG16(weights='imagenet', include_top=False, input_shape=(64, 64, 3), pooling="max")

    formattedPatchPixels = [np.delete(patch.pixels.reshape([1, 64, 64, 4]), 3, 3) for patch in meshPatches]

    allPixels = np.concatenate(formattedPatchPixels)
    allPixels = tf.convert_to_tensor(allPixels, dtype = tf.float32)
    allPixels = ((allPixels / 255.0) * 2.0) - 1.0

    imageFeatures = []
    with tf.device('/gpu:0'):
        imageFeatures = model.predict(allPixels)

    kdt = KDTree(imageFeatures,  leaf_size = 40, metric = 'euclidean')
    patchIdx = 1637
    dists, neighsIdx = kdt.query([imageFeatures[patchIdx]], k=20)

    for neighIdx in neighsIdx[0]:
        bm.verts[meshPatches[neighIdx].centerVertexIdx].select = True

    #Building the KDtree
    kdt = KDTree(topoFeatures,  leaf_size = 40, metric = 'euclidean')
    rankRecoverer = LowRankRecovery.LowRankRecovery()
    clusterSize = 20

raise Exception("Prout")

#Performing recovery on each patch
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
            faceNormal += newNormals[faceVertIdx] * np.linalg.norm(faceBarycenter - np.array(bm.verts[faceVertIdx].co))
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