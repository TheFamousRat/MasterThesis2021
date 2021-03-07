#Importing static modules
 
import bpy
import bmesh
from PIL import Image
import sys
import os
import hashlib
import pickle
import threading
import time
import gc

gc.enable()
gc.collect()

#Loading user-defined modules (subject to frequent changes and needed reloading)
pathsToAdd = ["/home/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/src"]

for pathToAdd in pathsToAdd:
    sys.path.append(pathToAdd)

import basicUtils 
import faceUtils
import clusteredBmesh

import importlib
importlib.reload(basicUtils)
importlib.reload(faceUtils)
importlib.reload(clusteredBmesh)

for pathToAdd in pathsToAdd:
    sys.path.remove(pathToAdd)

### FUNCTIONS

def cacheTextures(sourceObj, bm, cachedImagesDic):
    """
    Caches the automatically generated material textures into a given dict object
    """
    uniqueMats = set([])
    for face in bm.faces:
        uniqueMats.add(face.material_index)
    for matIdx in uniqueMats:
        blenderTexture = faceUtils.getMaterialTexture(sourceObj.material_slots[matIdx].material)
        cachedImages[matIdx] = Image.open(bpy.path.abspath(blenderTexture.filepath), 'r').convert('HSV')

def getMeshHash(obj):
    return hashlib.sha224( str(obj.data.vertices).strip('[]').encode('utf-8') ).hexdigest()

def readCompressedPixels(compPixels):
    return [[compPixels[pixelIdxStart+i] for i in range(2)] for pixelIdxStart in range(0, len(compPixels), 2)]

### CODE

currentObject = bpy.context.object

if currentObject is None:
    raise(Exception("Please select the mesh on which you want to operate"))

if currentObject.type != 'MESH':
    raise(Exception("Please select a mesh object (selected type : {})".format(currentObject.type)))

#Loading the mesh in edit mod, so it's easier to interract with the faces (select/deselect them for example)
print("Loading the mesh info...")
bm = bmesh.from_edit_mesh(currentObject.data)
bm.faces.ensure_lookup_table()

#We load and cache the images for easy access to the pixels
print("Caching face textures...")
cachedImages = {}
cacheTextures(currentObject, bm, cachedImages)

print("Tests")
availableFaces = list(range(len(bm.faces))) #The index of the faces not belonging to any cluster
clusters = [] #A list of list of all faces, grouped by the cluster they belong to
candidateFaces = {} #Faces that might 
incompatibleFaces = [] #For the current cluster, the index of faces that can't be added to the current cluster

# Baking the face pixels for faster clustering
bakedFacePixelsPath = os.path.join(bpy.path.abspath("//"), '{}.pkl'.format(getMeshHash(currentObject)))

if not os.path.exists(bakedFacePixelsPath):
    print("Baked mesh pixels not found, starting baking process...")
    start = time.time()
    faceUtils.bakeFacePixels(bm, bakedFacePixelsPath, cachedImages, 8) #8 threads works well on my machine, might need tuning
    end = time.time()
    # 4 threads : 812.0091547966003 seconds
    # 8 threads : 515.5761802196503 seconds
    # 16 threads : 513.2351567745209 seconds
    print("Baking done in {} seconds".format(end - start))
    print("File baked to {}".format(bakedFacePixelsPath))
else:
    print("Baked pixels file found in {}".format(bakedFacePixelsPath))

print("Loading baked pixels file...")
start = time.time()
bakedPixels = {}
with open(bakedFacePixelsPath, 'rb') as f:
    bakedPixels = pickle.load(f)#json.load(f, object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()})
end = time.time()
print("File loaded in {} seconds".format(end - start))

print("Starting faces per-color clustering...")
print(readCompressedPixels(bakedPixels[70000]))
if False:
    clusteredMesh = clusteredBmesh.ClusteredBMesh(bm)
    clusteredMesh.createNewCluster(True)
    clusteredMesh.addFaceToLastCluster(bm.faces[0])

    while clusteredMesh.areFacesCandidateForLastCluster():
        candidateIdx, neighbourIdx = clusteredMesh.getACandidateFace()
        candidateFace = bm.faces[candidateIdx]
        neighbourFace = bm.faces[neighbourIdx]
        
        if faceUtils.getFacePixelsDistance(bm, candidateFace, neighbourFace, cachedImages) < 0.01:
            clusteredMesh.addFaceToLastCluster(candidateFace)
        else:
            clusteredMesh.setFaceAsIncompatible(candidateFace)


print("Calling garbage collector")
lastGarbageSize = 0
currentGarbageSize = 1
while lastGarbageSize != currentGarbageSize:
    lastGarbageSize = currentGarbageSize
    currentGarbageSize = gc.collect()
    
print("End of script reached")