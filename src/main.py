#Importing static modules
 
import bpy
import bmesh
from PIL import Image
import sys
import os
import hashlib
import json
import threading
import time

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

def getFaceCSVstr(bm, face, imagesCache):
    ret = ""
    
    pixels = faceUtils.getFacePixelColors(bm, face, imagesCache[face.material_index])
    for pixel in pixels:
        ret += str(pixel[0]) + "," + str(pixel[1]) + "," + str(face.index) + "\n"
    return ret

def bakePixelsArray(bm, idxArray, bakedPixels, threadIdx, threadsProgressList):
    for i in range(len(idxArray)):
        faceIdx = idxArray[i]
        face = bm.faces[faceIdx]
        pixels = faceUtils.getFacePixelColors(bm, face, cachedImages[face.material_index])
        bakedPixels[faceIdx] = ([[pixel[pxId] for pxId in range(2)] for pixel in pixels])
        
        threadsProgressList[threadIdx] = i

def giveThreadsState(threadsList, threadsProgressList, threadsWorkSize):
    start = time.time()
    workerThreadsAmount = len(threadsList) - 1
    while True:

        aliveThreadsCount = 0
        totalTimeRemaining = 0.0
        threadsReportStr = ""

        for i in range(workerThreadsAmount):

            timeElapsed = time.time() - start
            thread = threadsList[i]
            threadsReportStr += "Thread {} : ".format(i)

            if thread.is_alive():

                allThreadsDead += 1
                workProgress = float(threadsProgressList[i] + 1) / float(threadsWorkSize[i])
                threadsReportStr += str( 100.0 * workProgress ) + " %"

                threadTimeRemaing = timeElapsed * ((1.0 / workProgress) - 1.0)
                totalTimeRemaining += threadTimeRemaing
            else:

                threadsReportStr += "Done."
            
            threadsReportStr += '\n'

        threadsReportStr += 'Remaining time : {} s\n'.format(totalTimeRemaining / float(aliveThreadsCount))
        sys.stdout.write(threadsReportStr)

        if allThreadsDead:
            break
        else:
            time.sleep(0.5)
        

def bakeFacePixels(bm, fileName, threadsAmount = 4):
    bakedPixels = {}
    facesCount = len(bm.faces)
    
    arrayLimits = list(range(0,facesCount, int(facesCount/threadsAmount)))
    if not ((facesCount - 1) in arrayLimits):
        arrayLimits.append(facesCount)

    threads = []
    threadsProgressList = [0 for i in range(threadsAmount)]
    threadsWorkSize = []
    for i in range(threadsAmount):
        #Creating the new thread
        workedIndex = list(range(arrayLimits[i], arrayLimits[i+1]))
        newThread = threading.Thread(target=bakePixelsArray, args=(bm, workedIndex, bakedPixels, i, threadsProgressList,))
        threads.append(newThread)
        newThread.start()
        #Gathering information for the updater
        threadsWorkSize.append(len(workedIndex))

    #Creating a thread to follow the thread's progress
    updaterThread = threading.Thread(target=giveThreadsState, args=(threads, threadsProgressList, threadsWorkSize,))
    updaterThread.start()
    threads.append(updaterThread)

    for t in threads:
        t.join()
    
    with open(fileName, 'w') as f:
        json.dump(bakedPixels, f)#, indent = 4)

def getMeshHash(obj):
    return hashlib.sha224( str(obj.data.vertices).strip('[]').encode('utf-8') ).hexdigest()

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

# Baking the pixel clusters for faster clustering
bakedFacePixelsPath = os.path.join(bpy.path.abspath("//"), '{}.json'.format(getMeshHash(currentObject)))

if not os.path.exists(bakedFacePixelsPath):
    print("Baked mesh pixels not found, starting baking process...")
    start = time.time()
    bakeFacePixels(bm, bakedFacePixelsPath, 8) #8 threads works well on my machine, might need tuning
    end = time.time()
    print("Baking done in {} seconds".format(end - start))
    print("File baked to {}".format(bakedFacePixelsPath))
else:
    print("Baked pixels file found in {}".format(bakedFacePixelsPath))
# 4 threads : 812.0091547966003 seconds
# 8 threads : 515.5761802196503 seconds
# 16 threads : 513.2351567745209 seconds
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
    
import gc
gc.collect()