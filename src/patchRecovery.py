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
from sklearn.metrics import pairwise_distances_argmin_min
from scipy.optimize import linear_sum_assignment
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
    
def createVertexPatch(bmeshObj, vertex):
    return Patch.Patch(bmeshObj, vertex.index, RINGS_NUM)
    
def intToSignedBitList(val, bitsAmount):
    """
    Takes an int as parameter and converts it to a signed bit list (True = -1, False = 1) of size bitsAmount
    """
    return [1-2*bool(val & (1<<j)) for j in range(bitsAmount)]

def createPatchCorrectionChain(startingPatchIdx):
    dataArr = np.array([patch.eigenVals / np.linalg.norm(patch.eigenVals) for patch in meshPatches])
    correctedPatches = []
    uncorrectedPatches = list(range(len(dataArr)))
    refPatchPairs = []

    start = time.time()

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

def patchesAxisSignMatching(patchRef, patchToCorrect, bmeshObj):
    vertices1Pos = patchRef.getVerticesPos(bmeshObj)
    patch1RefPos = patchRef.getCentralPos(bmeshObj)
    #Transforming the vertices position for patchRef
    vertices1Pos = (patchRef.rotMatInv @ (vertices1Pos - patch1RefPos).T).T
    
    vertices2Pos = patchToCorrect.getVerticesPos(bmeshObj)
    patch2RefPos = patchToCorrect.getCentralPos(bmeshObj)
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
        closestPoints, closestDists = pairwise_distances_argmin_min(vertices2PosTransformed, vertices1Pos, metric = 'sqeuclidean')
        matchingResults.append(closestDists.sum())
    
    bestCombinationIdx = 3#np.argmin(matchingResults)
    signsList = intToSignedBitList(bestCombinationIdx, COLUMNS_SIGN_MODIFIED)
    
    for colId in range(COLUMNS_SIGN_MODIFIED):
        patchToCorrect.eigenVecs[:,colId] = signsList[colId] * patchToCorrect.eigenVecs[:,colId]
    patchToCorrect.rotMatInv = np.linalg.inv(patchToCorrect.eigenVecs)

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

##Covering the mesh with patches
meshPatches = []

#Checking in patches were baked/are still up to date
patchesDataPath = os.path.join(meshDataPath, 'patches.pkl')
if os.path.exists(patchesDataPath):
    #Loading binary baked patches file
    print("Baked patches file found in {}. Loading...".format(patchesDataPath))
    with lzma.open(patchesDataPath, 'rb') as f:
        meshPatches = pickle.load(f)  
    
    #Checking equality between two patches for the same mesh
    print("Checking integrity...")
    patchRef = createVertexPatch(bm, bm.verts[0])
    patchBaked = meshPatches[0]
    if pickle.dumps(patchRef) != pickle.dumps(patchBaked):
        print("Outdaded or invalid baked patches found, rebuilding all patches")
        meshPatches = []
    else:
        print("Patch integrity test successful")
    
#Checking if the patchs were correctly loaded
if len(meshPatches) == 0:
    #Patches not found, baking them
    print("Building patches for the mesh")
    start = time.time()
    for vert in bm.verts:
        meshPatches.append(createVertexPatch(bm, vert))

    end = time.time()
    print("Time taken : {} seconds".format(end - start))
    
    #Launching a procedure to correct the orientation of the patches' eigenvectors
    refPatchChain = createPatchCorrectionChain(0)
        
    print("Starting to correct the patches' signs...")

    start = time.time()

    for couple in refPatchChain:
        patchesAxisSignMatching(meshPatches[couple[0]], meshPatches[couple[1]], bm)

    end = time.time()
    print("Time taken : {} seconds".format(end - start))
    
    
    print("Dumping into a binary file...")
    with lzma.open(patchesDataPath, 'wb') as f:
        pickle.dump(meshPatches, f)
    print("Done")

print("Drawing the patches' eigenvectors")
for patch in meshPatches:
    patchCentralPos = patch.getCentralPos(bm)
    for i in range(3):
        dir = patch.eigenVecs[:,i]
        debugDrawing.draw_line(gpencil, gp_frame, (patchCentralPos, patchCentralPos + lineSize * dir), (0.5, 3.0), axisColors[i])




##Baking patch texture info
prevRenderEngine = bpy.context.scene.render.engine
bpy.context.scene.render.engine = 'CYCLES'

#Creating a temporary UV layer
uvLayerName = "tempProj"
if not uvLayerName in selectedObj.data.uv_layers:
    selectedObj.data.uv_layers.new(name = uvLayerName)
uvLayer = selectedObj.data.uv_layers[uvLayerName]
    
if not uvLayer.active:
    uvLayer.active = True

#Creating an image to bake to
bakedImgName = "bakedImage"
bakedImgSize = 16
if not bakedImgName in bpy.data.images:
    bpy.data.images.new(bakedImgName, bakedImgSize, bakedImgSize)
bpy.data.images[bakedImgName].scale(bakedImgSize, bakedImgSize)
    
#Preparing the shaders for baking if they aren't already
imageNodeName = "BakedTextureNode"
uvLayerNodeName = "BakedUVLayerNode"
for mat in selectedObj.data.materials:
    nodeTree = mat.node_tree #shorthand
    #Preparing the image node
    if not imageNodeName in mat.node_tree.nodes:
        nodeTree.nodes.new("ShaderNodeTexImage").name = imageNodeName
        
    imageNode = nodeTree.nodes[imageNodeName]
    imageNode.location = np.array([0.0, 0.0])
    imageNode.image = bpy.data.images[bakedImgName]
        
    #Preparing the UV node
    if not uvLayerNodeName in nodeTree.nodes:
        newNode = nodeTree.nodes.new("ShaderNodeUVMap")
        newNode.name = uvLayerNodeName
    
    uvNode = nodeTree.nodes[uvLayerNodeName]
    uvNode.location = np.array(imageNode.location) - np.array([200.0,0.0])
    uvNode.uv_map = uvLayerName
    
    #Connecting the nodes (if necessary)
    if len(imageNode.inputs['Vector'].links) == 0:
        nodeTree.links.new(uvNode.outputs['UV'], imageNode.inputs[0])
        
    #Setting the Image texture one as the active
    nodeTree.nodes.active = imageNode
    
#Unselecting every faces
for face in bm.faces:
    face.select = False

#Selecting a patch
patchesToWorkOn = [meshPatches[1440]]
for patch in patchesToWorkOn:
    #'Resetting' the UV map by putting all UV is a far away corner... Dirty but works !
    for vert in bm.verts:
        for loop in vert.link_loops:
            loop[bm.loops.layers.uv[uvLayerName]].uv = np.array([2.0, 2.0])
    
    patchFacesIt = patch.getFacesIdxIterator()
    
    #Remove the rest of the UVs from the focus
    #!!!!!
    
    #Unwrap using angle-based approach
    for faceIdx in patchFacesIt:
        bm.faces[faceIdx].select = True
    
    bpy.ops.uv.unwrap()
    
    for faceIdx in patchFacesIt:
        bm.faces[faceIdx].select = False
    
    #Center the UVs (so that the central vertex is at pos (0.5,0.5)
    uvMapCenter = np.array([0.5, 0.5])
    posShift = uvMapCenter - np.array(patch.getVertUV(bm, patch.centerVertexIdx, uvLayerName))
    
    for vIdx in patch.verticesIdxList:
        vertUVCoords = patch.getVertUV(bm, vIdx, uvLayerName)
        patch.setVertUV(bm, vIdx, uvLayerName, np.array(vertUVCoords) + posShift)
    
    #Rotate the UVs to match local axis
    #Finding a ref
    linkedEdge = bm.verts[patch.centerVertexIdx].link_edges[0]
    refVertIdx = (linkedEdge.verts[0] if linkedEdge.verts[0].index != patch.centerVertexIdx else linkedEdge.verts[1]).index
    
    #Projecting that ref onto the plane
    planeNormal = patch.eigenVecs[:,2]
    planeOrigin = np.array(bm.verts[patch.centerVertexIdx].co)
    vertWorldPos = np.array(bm.verts[refVertIdx].co)
    vertRelPos = vertWorldPos - planeOrigin
    projCoords = np.array([np.dot(vertRelPos, patch.eigenVecs[:,0]), np.dot(vertRelPos, patch.eigenVecs[:,1])])
    
    #Angle between the projection and the x-axis (in the world plane)
    angleWorld = -math.atan2(projCoords[1], projCoords[0])
    
    #xAxis in the UV map
    refVecUV = np.matrix(patch.getVertUV(bm, refVertIdx, uvLayerName)).T
    centerVec = np.matrix(uvMapCenter).T
    centeredRefUV = refVecUV - centerVec
    angleUV = math.atan2(centeredRefUV[1], centeredRefUV[0])
    
    #Rotation matrix
    rotMatInvUV = np.matrix([[math.cos(-angleUV), -math.sin(-angleUV)],[math.sin(-angleUV), math.cos(-angleUV)]])
    rotMatInvAxis = np.matrix([[math.cos(angleWorld), -math.sin(angleWorld)],[math.sin(angleWorld), math.cos(angleWorld)]])
    rotMat = rotMatInvAxis @ rotMatInvUV
    
    for vIdx in patch.verticesIdxList:
        vertUVCoords = np.matrix(patch.getVertUV(bm, vIdx, uvLayerName)).T
        patch.setVertUV(bm, vIdx, uvLayerName, (rotMat @ (vertUVCoords - centerVec)) + centerVec)
    
    bpy.ops.object.bake(type='EMIT')
        
bpy.context.scene.render.engine = prevRenderEngine