import os
import bpy
import bmesh
import sys
import time
import pickle
import hashlib
import numpy as np
from scipy.spatial.distance import cdist

#Loading user-defined modules (subject to frequent changes and needed reloading)
pathsToAdd = ["/home/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/src"]

for pathToAdd in pathsToAdd:
    sys.path.append(pathToAdd)

import Patch

import importlib
importlib.reload(Patch)

for pathToAdd in pathsToAdd:
    sys.path.remove(pathToAdd)

###Constants
RINGS_NUM = 2 #Number of rings around the central face to take into the patch

### Functions
def getMeshHash(obj):
    return hashlib.sha224( str(obj.data.vertices).strip('[]').encode('utf-8') ).hexdigest()
    
def createFacePatch(bmeshObj, face):
    return Patch.Patch(bmeshObj, face.index, RINGS_NUM)

def getPatchesSimilarity(patch1Idx, patch2Idx, patchArr):
    return pow(np.linalg.norm(patch1.eigenVals - patch2.eigenVals), 2.0)
    
### Logic
#Creating the bmesh
selectedObj = bpy.context.active_object

if selectedObj.type != "MESH":
    raise Exception("Please choose a mesh")
    
bm = bmesh.from_edit_mesh(selectedObj.data)
bm.faces.ensure_lookup_table()

#Storage for mesh data
meshDataPath = os.path.join(bpy.path.abspath("//"), 'meshesData/{}/'.format(getMeshHash(selectedObj)))
if not os.path.exists(meshDataPath):
    os.makedirs(meshDataPath)

#Covering the mesh with patches
meshPatches = []

patchesDataPath = os.path.join(meshDataPath, 'patches.pkl')
if os.path.exists(patchesDataPath):
    print("Baked patches file found in {}. Loading...".format(patchesDataPath))
    with open(patchesDataPath, 'rb') as f:
        meshPatches = pickle.load(f)  
    print("Checking integrity...")
    patchRef = createFacePatch(bm, bm.faces[0])
    patchBaked = meshPatches[0]
    if pickle.dumps(patchRef) != pickle.dumps(patchBaked):
        print("Outdaded or invalid baked patches found, rebuilding all patches")
        meshPatches = []
    else:
        print("Patch integrity test successful")
    
if len(meshPatches) == 0:
    #Patches not found, baking them
    print("Building patches for the mesh")
    start = time.time()
    for face in bm.faces:
        meshPatches.append(createFacePatch(bm, face))

    end = time.time()
    print("Time taken : {} seconds".format(end - start))
    print("Dumping into a binary file...")
    with open(patchesDataPath, 'wb') as f:
        pickle.dump(meshPatches, f)
    print("Done")

from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree

dataArr = np.array([patch.eigenVals / np.linalg.norm(patch.eigenVals) for patch in meshPatches])
clustering = KMeans(n_clusters = 5).fit(dataArr)

for i in range(len(dataArr)):
    if clustering.labels_[i] == 2:
        bm.faces[i].select = True

def KNNTest():
    kdt = KDTree(dataArr, leaf_size = 50, metric = 'euclidean')
    K = 50
    centralFaceIdx = 0
    for faceIdx in kdt.query(dataArr, k = K)[1][centralFaceIdx]:
        bm.faces[faceIdx].select = True

#Trying some DBSCAN algorithm
def DBSCANImpl():
    epsilon = 0.1
    minClusterSize = 5
    unclusteredPatches = np.array([[patch] for patch in meshPatches])
    currentClusterNum = -1

    while len(unclusteredPatches) > 0:
        print("Remaining points : {}".format(len(unclusteredPatches)))
        sourcePatch = np.array([unclusteredPatches[0]])
        unclusteredPatches = np.delete(unclusteredPatches, 0, axis = 0)
        
        distVec = cdist(sourcePatch, unclusteredPatches, metric = getPatchesSimilarity)
        neighboursIdx = np.where(distVec < epsilon)[1]
                
        if len(neighboursIdx) < minClusterSize:
            continue #Cluster too small
        
        ##Creating new cluster
        #Labelling the seeds
        currentClusterNum += 1
        print("Building cluster #{}".format(currentClusterNum))
        seeds = np.take(unclusteredPatches, neighboursIdx, axis = 0)
        sourcePatch[0][0].clusterLabel = currentClusterNum
        for seed in seeds:
            seed[0].clusterLabel = currentClusterNum
        
        #Removing the seed elements of the new cluster
        unclusteredPatches = np.delete(unclusteredPatches, neighboursIdx, axis = 0)
            
        #Expanding the cluster
        while len(seeds) > 0:
            currentSeed = np.array([seeds[0]])
            seeds = np.delete(seeds, 0, axis = 0)
            
            distVec = cdist(currentSeed, unclusteredPatches, metric = getPatchesSimilarity)
            neighboursIdx = np.where(distVec < epsilon)[1] #New elements to add to the cluster
            
            seeds = np.concatenate((seeds, np.take(unclusteredPatches, neighboursIdx, axis = 0)))
            
            for newPatchIdx in neighboursIdx:
                unclusteredPatches[newPatchIdx][0].clusterLabel = currentClusterNum
            
            unclusteredPatches = np.delete(unclusteredPatches, neighboursIdx, axis = 0)

            print("Added {} patches to cluster {} (remaining patches : {})".format(len(neighboursIdx), currentClusterNum, len(unclusteredPatches)))
                    
    for patch in meshPatches:
        if patch.clusterLabel == 1:
            bm.faces[patch.centralFaceIdx].select = True