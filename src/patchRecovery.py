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
#Image processing
from PIL import Image
#Blender libs
import bpy
import bmesh
#Hashing utilies for mesh unique identification
import hashlib
#Scikit suite
import numpy as np
from scipy.spatial.distance import cdist
#Show progress bar utility
from progress.bar import Bar

##Local libraries (re-)loading
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
    
def createFacePatch(bmeshObj, face):
    return Patch.Patch(bmeshObj, face.index, RINGS_NUM)
    
def intToSignedBitList(val, bitsAmount):
    """
    Takes an int as parameter and converts it to a signed bit list (True = -1, False = 1) of size bitsAmount
    """
    return [1-2*bool(val & (1<<j)) for j in range(bitsAmount)]

###Body
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

##Correcting the patches' orthogonal basis signs
#Pairing the patches together as a ref and uncorrected patch couple
def createPatchCorrectionChain():
    from sklearn.metrics import pairwise_distances_argmin_min

    dataArr = np.array([patch.eigenVals / np.linalg.norm(patch.eigenVals) for patch in meshPatches])
    correctedPatches = []
    uncorrectedPatches = list(range(len(dataArr)))
    refPatchPairs = []

    start = time.time()

    #Picking an arbitrary patch : the directions of his orthogonal basis are defined as a correct reference
    startingPatchIdx = 4150

    correctedPatches.append(startingPatchIdx)
    uncorrectedPatches.remove(startingPatchIdx)
    closestPoints, closestDists = pairwise_distances_argmin_min(dataArr[correctedPatches], dataArr[uncorrectedPatches])

    bar = Bar('Building patch connectivity map', suffix='%(percent).1f%%', max=len(uncorrectedPatches) - 1)
    while len(uncorrectedPatches) > 1:
        ##Find the closest uncorrected patch and its ref patch
        closestRelationId = np.argmin(closestDists)
        refPatchIdx = correctedPatches[closestRelationId]
        patchToCorrectIdx = closestPoints[closestRelationId]
        refPatchPairs.append((refPatchIdx, patchToCorrectIdx))
        uncorrectedPatches.remove(patchToCorrectIdx)
        ##Creating a new row for the new patch, with empty data
        closestPoints = np.append(closestPoints, -1)
        closestDists = np.append(closestDists, 0.0)
        correctedPatches.append(patchToCorrectIdx)
        #print("Closest ref : {}, closest uncorrected patch : {} (remaining uncorrected patches : {})".format(refPatchIdx, patchToCorrectIdx, len(uncorrectedPatches)))
        ##Finding nearest neighbours for the corrected points that used to have the new point as their nearest neighbour
        #Locating the patches with refPatchIdx as their nearest neighbour
        patchesObsNearstNeighbPos = np.where(closestPoints == patchToCorrectIdx)[0]
        patchesObsNearstNeighbPos = np.append(patchesObsNearstNeighbPos, len(correctedPatches)-1)
        patchesObsNearstNeighbIdx = np.array(correctedPatches)[patchesObsNearstNeighbPos]
        #Finding new nearest neighbours of those patches, registering the relevant statistics
        newPatchClosestPoints, newPatchClosestDists = pairwise_distances_argmin_min(dataArr[patchesObsNearstNeighbIdx], dataArr[uncorrectedPatches])
        for i in range(len(patchesObsNearstNeighbPos)):
            closestPoints[patchesObsNearstNeighbPos[i]] = uncorrectedPatches[newPatchClosestPoints[i]]
            closestDists[patchesObsNearstNeighbPos[i]] = newPatchClosestDists[i]
        bar.next()

    refPatchPairs.append((correctedPatches[np.argmin(closestDists)], uncorrectedPatches[0]))

    end = time.time()

    print("Total time : ", end - start)
    
    return refPatchPairs

refPatchChain = createPatchCorrectionChain()

from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment

def patchesAxisSignMatching(patchRef, patchToCorrect):
    vertices1Pos = patchRef.getVerticesPos(bm)
    patch1RefPos = patchRef.getFaceBarycenter(bm.faces[patchRef.centralFaceIdx])
    #Transforming the vertices position for patchRef
    vertices1Pos = (patchRef.rotMatInv @ (vertices1Pos - patch1RefPos).T).T
    
    vertices2Pos = patchToCorrect.getVerticesPos(bm)
    patch2RefPos = patchToCorrect.getFaceBarycenter(bm.faces[patchToCorrect.centralFaceIdx])
    #Centering the vertices of patch to correct
    vertices2Pos = vertices2Pos - patch2RefPos
    
    matchingResults = []
    for i in range(NUMBER_OF_SIGN_COMBINATION):
        signsList = intToSignedBitList(i, COLUMNS_SIGN_MODIFIED) #Signs of the columns that we will switch
        mat = np.copy(patchToCorrect.eigenVecs)
        #Applying the sign changes
        for colId in range(COLUMNS_SIGN_MODIFIED):
            mat[:,colId] = signsList[colId] * mat[:,colId]
        
        #Transforming the vertices
        rotMatInv = np.linalg.inv(mat)
        vertices2PosTransformed = (rotMatInv @ vertices2Pos.T).T
        
        #Measuring the difference between the transformed patches
        d = cdist(vertices1Pos, vertices2PosTransformed)
        assignment = linear_sum_assignment(d)
        matchingResults.append(d[assignment].sum() / len(d[assignment]))
    
    bestCombinationIdx = np.argmin(matchingResults)
    signsList = intToSignedBitList(bestCombinationIdx, COLUMNS_SIGN_MODIFIED)
    for colId in range(COLUMNS_SIGN_MODIFIED):
        patchToCorrect.eigenVecs[:,colId] = signsList[colId] * patchToCorrect.eigenVecs[:,colId]
    
print("Starting to correct the patches' signs...")

start = time.time()

for couple in refPatchChain:
    patchesAxisSignMatching(meshPatches[couple[0]], meshPatches[couple[1]])

end = time.time()
print("Time taken : {} seconds".format(end - start))

print("Drawing the patches")
for patch in meshPatches:
    patchCentralPos = patch.getFaceBarycenter(bm.faces[patch.centralFaceIdx])
    for i in range(3):
        dir = patch.eigenVecs[:,i]
        debugDrawing.draw_line(gpencil, gp_frame, (patchCentralPos, patchCentralPos + lineSize * dir), (0.5, 3.0), axisColors[i])


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