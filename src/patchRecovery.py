import os
import bpy
import bmesh
import sys
import time
import math
#To compress mesh data files efficiently
import pickle
import lzma

from PIL import Image

import hashlib
import numpy as np
from scipy.spatial.distance import cdist

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
bm.verts.ensure_lookup_table()
bm.edges.ensure_lookup_table()
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
    with lzma.open(patchesDataPath, 'rb') as f:
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
    with lzma.open(patchesDataPath, 'wb') as f:
        pickle.dump(meshPatches, f)
    print("Done")

##Test to invert a patch position
gpencil, gp_layer = debugDrawing.init_grease_pencil()
gp_layer.clear() #Removing the previous GPencils
gp_frame = gp_layer.frames.new(0)
lineSize = 0.015
axisColors = ["ff0000", "00ff00", "0000ff"] #Colors of the XYZ axis

#Operation supposed to take place within a patch's class, so we take an arbitraty one

from sklearn.metrics import pairwise_distances_argmin_min

dataArr = np.array([patch.eigenVals / np.linalg.norm(patch.eigenVals) for patch in meshPatches])
correctedPatches = []
uncorrectedPatches = list(range(len(dataArr)))

for patch in meshPatches:
    patchCentralPos = patch.getFaceBarycenter(bm.faces[patch.centralFaceIdx])
    dir = lineSize * patch.eigenVecs[:,2]
    debugDrawing.draw_line(gpencil, gp_frame, (patchCentralPos, patchCentralPos + dir), (0.5, 3.0), "0000ff")

def patchesAxisSignMatching(patchRef, patchToMatch):
    vertices1Pos = patchRef.getVerticesPos(bm)
    vertices2Pos = patchToMatch.getVerticesPos(bm)

    from scipy.spatial.distance import cdist
    from scipy.optimize import linear_sum_assignment

    start = time.time()

    for i in range(8):
        signsList = [1-2*bool(i & (1<<j)) for j in range(3)] #Signs of the columns that we will switch
        

    d = cdist(vertices1Pos, vertices2Pos)
    assignment = linear_sum_assignment(d)
    d[assignment].sum() / len(d[assignment])

    end = time.time()
    print("Time taken : {} seconds".format(end - start))

#Plane characteristics
def principalCurvatureCalc():
    for patch in meshPatches:
        planeNormal = patch.eigenVecs[:,2]
        planeOrigin = patch.getFaceBarycenter(bm.faces[patch.centralFaceIdx])
        e1 = patch.eigenVecs[:,0]
        e2 = patch.eigenVecs[:,1]
        bm.faces[patch.centralFaceIdx].select = True

        #Projecting a vert from the patch onto the plane
        X = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        Y = np.array([0.0])
        for vertIdx in patch.getVerticesIdx(bm):
            #Projecting the vertex
            vert = bm.verts[vertIdx]
            vert.select = True
            initialPos = np.array(vert.co)
            t = np.dot(planeNormal, initialPos - planeOrigin)
            vertProj = initialPos - planeNormal * t
            #Getting its UV coordinates
            u = np.dot(e1, vertProj - planeOrigin)
            v = np.dot(e2, vertProj - planeOrigin)
            #And registering it into a matrix for regression afterwards
            X = np.vstack([X, np.array([1.0, u, v, u*u, u*v, v*v])])
            Y = np.vstack([Y, np.array([t])])

        beta, res, rk, s = np.linalg.lstsq(X,Y)
        v1 = np.array([1.0, 1.0, 0.0, 0.0, 0.0, 0.0])
        v2 = np.array([1.0, -1.0, 0.0, 0.0, 0.0, 0.0])
        if np.dot(v1, beta) < np.dot(v2, beta):
            e1 = -e1
        dir = lineSize * e1
        debugDrawing.draw_line(gpencil, gp_frame, (planeOrigin, planeOrigin + dir), (1.0, 5.0),  "ff0000")          
#principalCurvatureCalc()


def unrotateMeshPatch(patch_):
    vertsId = patch_.getVerticesIdx(bm)
    centralFacePos_ = patch_.getFaceBarycenter(bm.faces[patch_.centralFaceIdx])
    unrotatedVertsPos = {}
    for vertId in vertsId:
        unrotatedVertsPos[vertId] = patch_.rotMatInv @ (np.array(bm.verts[vertId].co) - centralFacePos_)
        
    for vertId in vertsId:
        bm.verts[vertId].co = unrotatedVertsPos[vertId]
    bmesh.update_edit_mesh(selectedObj.data)

#unrotateMeshPatch(patchConsidered)