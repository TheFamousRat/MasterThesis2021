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
import debugDrawingBlender

import importlib
importlib.reload(Patch)
importlib.reload(debugDrawingBlender)

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
gpencil, gp_layer = debugDrawingBlender.init_grease_pencil()
gp_layer.clear()
gp_frame = gp_layer.frames.new(0)
lineSize = 0.005

#Operation supposed to take place within a patch's class, so we take an arbitraty one
patchConsidered = meshPatches[1160]

centralVecPos = patchConsidered.getFaceBarycenter(bm.faces[patchConsidered.centralFaceIdx])

import scipy.linalg as la

###

#Plane characteristics
for patch in meshPatches:
    planeNormal = patch.eigenVecs[:,2]
    planeOrigin = patch.getFaceBarycenter(bm.faces[patch.centralFaceIdx])
    e1 = patch.eigenVecs[:,0]
    e2 = patch.eigenVecs[:,1]
    bm.faces[patch.centralFaceIdx].select = True

    #Projecting a vert from the patch onto the plane
    X = np.array([0.0, 0.0, 0.0])
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
        X = np.vstack([X, 0.5 * np.array([u*u/2.0, v*v/2.0, u*v])])
        Y = np.vstack([Y, np.array([t])])
        debugDrawingBlender.draw_line(gpencil, gp_frame, initialPos, vertProj,  "ff0000")

    beta, res, rk, s = np.linalg.lstsq(X,Y)
    dir = beta[1] * e1 + beta[2] * e2
    dir = (dir / np.linalg.norm(dir)) * 0.01
    break
    
###

#Calculating the approximate curvature tensor for the patch
def debugDrawTensors():
    for patch in meshPatches:
        centralVecPos = patch.getFaceBarycenter(bm.faces[patch.centralFaceIdx])
        #eigenVals, eigenVecs = la.eigh(patch.computeCurvatureTensor(bm))
        #print(patch.eigenVals)
        
        axisColors = ["ff0000", "00ff00", "0000ff"]
        
        for i in range(3):
            eigenVecDir = lineSize * patch.eigenVecs[:,i]
            debugDrawingBlender.draw_line(gpencil, gp_frame, centralVecPos, centralVecPos + eigenVecDir,  axisColors[i])
#debugDrawTensors()

def prout():
    vertsId = patchConsidered.getVerticesIdx(bm)
    unrotatedVertsPos = {}
    for vertId in vertsId:
        unrotatedVertsPos[vertId] = rotMatInv @ (np.array(bm.verts[vertId].co) - centralVecPos)
        
    for vertId in vertsId:
        bm.verts[vertId].co = unrotatedVertsPos[vertId]
    bmesh.update_edit_mesh(selectedObj.data)

#prout()

##Logic to sample patch normals
def testNormalSampling():
    samplerRes = 8 #Square root of the number of samples to be taken from the normals

    #Getting the BBox of the unrotated patch
    BBoxSize = []
    zipdCoords = zip(*unrotatedVertsPos.values())
    for i in zipdCoords:
        BBoxSize.append((max(i) - min(i)).item(0))
    #Building the plane vectors
    planeVecs = np.diag(BBoxSize)

    #Projecting the faces to the plane
    normalizedFaceCoords = {}
    normalizedNormals = {}
    for faceIdx in patchConsidered.getFacesIdxIterator():
        normalizedFaceCoords[faceIdx] = patchConsidered.normalizePosition(bm, patchConsidered.getFaceBarycenter(bm.faces[faceIdx]), True)
        normalizedNormals[faceIdx] = patchConsidered.normalizePosition(bm, np.array(bm.faces[faceIdx].normal), False)

    def getSampleToFacePlaneDist(sampleCoords, faceIdxNp):
        i = sampleCoords%samplerRes
        j = (sampleCoords-i)/samplerRes
        i = (i*2 - (samplerRes-1))/samplerRes
        j = (j*2 - (samplerRes-1))/samplerRes
        faceIdx = faceIdxNp[0]
        sampleFaceCoords = planeVecs[1] * i + planeVecs[2] * j
        return abs(np.dot(normalizedNormals[faceIdx], sampleFaceCoords - normalizedFaceCoords[faceIdx]))

    #Sampling the unrotated normal values from the patch
    sampledVals = [[np.zeros((3,1)) for j in range(samplerRes)] for i in range(samplerRes)]
    facesIdx = [[faceIdx] for faceIdx in patchConsidered.getFacesIdxIterator()]
    K = 3 #Number of closest faces to take into account
    for i in range(samplerRes):
        for j in range(samplerRes):
            #Finding the K closest faces to the sample, and adding their normals together
            distVec = cdist([[i+j*samplerRes]], facesIdx, metric = getSampleToFacePlaneDist)[0]
            sortedDistIdx = distVec.argsort()
            totalWeights = 0.0
            normApprox = np.array([0.0,0.0,0.0])
            for i in range(K):
                idx = sortedDistIdx[i]
                faceIdx = facesIdx[idx][0]
                dist = distVec[idx]
                weight = math.exp(-dist)
                totalWeights += weight
                normApprox += weight * normalizedNormals[faceIdx]
            normApprox = normApprox / totalWeights