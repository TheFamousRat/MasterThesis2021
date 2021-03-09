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
import math
import numpy as np

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
        cachedImages[matIdx] = Image.open(bpy.path.abspath(blenderTexture.filepath), 'r')#.convert('HSV')

def getMeshHash(obj):
    return hashlib.sha224( str(obj.data.vertices).strip('[]').encode('utf-8') ).hexdigest()

def getCombinedFaceColorsInertia(faceAInfo, faceBInfo):
    nA = float(faceAInfo["n"])
    nB = float(faceBInfo["n"])

    faceACentroid = np.array(faceAInfo["avg"])
    faceBCentroid = np.array(faceBInfo["avg"])

    combinedSize = float(nA + nB)
    combinedCentroid = (nA * faceACentroid + nB * faceBCentroid)/combinedSize

    faceAEnergy = (nA - 1.0) * faceAInfo["inert"] + nA * pow(np.linalg.norm(combinedCentroid - faceACentroid), 2.0)
    faceBEnergy = (nB - 1.0) * faceBInfo["inert"] + nB * pow(np.linalg.norm(combinedCentroid - faceBCentroid), 2.0)

    combinedInertia = (faceAEnergy + faceBEnergy)/(nA + nB - 1.0)

    return combinedSize, combinedCentroid.tolist(), combinedInertia


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

# Creating a folder storing that mesh's baked data
meshDataPath = os.path.join(bpy.path.abspath("//"), 'meshesData/{}/'.format(getMeshHash(currentObject)))
if not os.path.exists(meshDataPath):
    os.makedirs(meshDataPath)
    
# Baking the face pixels for faster clustering
bakedFacePixelsPath = os.path.join(meshDataPath, 'faceColors.pkl')
if not os.path.exists(bakedFacePixelsPath):
    print("Baked mesh pixels not found, starting baking process...")
    faceUtils.bakeFacePixels(bm, bakedFacePixelsPath, 8, cachedImages) #8 threads works well on my machine, might need tuning
    # 4 threads : 812.0091547966003 seconds
    # 8 threads : 515.5761802196503 seconds
    # 16 threads : 513.2351567745209 seconds
else:
    print("Baked pixels file found in {}".format(bakedFacePixelsPath))

print("Loading baked pixels file...")
bakedPixels = {}
with open(bakedFacePixelsPath, 'rb') as f:
    bakedPixels = pickle.load(f)

#We compute a few statistics for each face color set : mean, inertia etc.
bakedFaceColorsStatsPath = os.path.join(meshDataPath, 'faceColorsStats.pkl')
if not os.path.exists(bakedFaceColorsStatsPath):
    print("Baking face color statistics...")
    faceUtils.bakeFacePixelsStatistics(bm, bakedFaceColorsStatsPath, 8, bakedPixels)

print("Loading face color statistics...")
bakedFaceColStats = {}
with open(bakedFaceColorsStatsPath, 'rb') as f:
    bakedFaceColStats = pickle.load(f)

print("Starting faces per-color clustering...")

face1Idx = 0
face2Idx = 1
face1Info = bakedFaceColStats[face1Idx]
face2Info = bakedFaceColStats[face2Idx]
print(face1Info)
print(face2Info)
print(getCombinedFaceColorsInertia(face1Info, face2Info))

if True:
    clusteredMesh = clusteredBmesh.ClusteredBMesh(bm)
    clusteredMesh.createNewCluster(True)
    clusteredMesh.addFaceToLastCluster(bm.faces[10000])
    clusteredMesh.activateProgressFeedback()
    
    try:
        currentClusterInfo = bakedFaceColStats[clusteredMesh.clusters[-1][0]]
        while clusteredMesh.areFacesCandidateForLastCluster():
            candidateIdx, neighbourIdx = clusteredMesh.getACandidateFace()
            candidateFace = bm.faces[candidateIdx]
            
            combinedSize, combinedCentroid, combinedInertia = getCombinedFaceColorsInertia(currentClusterInfo, bakedFaceColStats[candidateIdx])
            if combinedInertia < 0.02:
                clusteredMesh.addFaceToLastCluster(candidateFace)
                currentClusterInfo = faceUtils.getFaceStatsFormated(combinedSize, combinedCentroid, combinedInertia)
            else:
                clusteredMesh.setFaceAsIncompatible(candidateFace)
    except e:
        clusteredMesh.deactivateProgressFeedback()

clusteredMesh.deactivateProgressFeedback()


print("Calling garbage collector")
lastGarbageSize = 0
currentGarbageSize = 1
while lastGarbageSize != currentGarbageSize:
    lastGarbageSize = currentGarbageSize
    currentGarbageSize = gc.collect()
    
print("End of script reached")