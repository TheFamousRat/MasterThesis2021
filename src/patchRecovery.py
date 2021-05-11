import os
import bpy
import bmesh
import sys
import time
import pickle
import hashlib

#Loading user-defined modules (subject to frequent changes and needed reloading)
pathsToAdd = ["/home/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/src"]

for pathToAdd in pathsToAdd:
    sys.path.append(pathToAdd)

import patch

import importlib
importlib.reload(patch)

for pathToAdd in pathsToAdd:
    sys.path.remove(pathToAdd)

###Constants
RINGS_NUM = 2 #Number of rings around the central face to take into the patch

### Functions
def getMeshHash(obj):
    return hashlib.sha224( str(obj.data.vertices).strip('[]').encode('utf-8') ).hexdigest()
    
def createFacePatch(bmeshObj, face):
    return patch.Patch(bmeshObj, face.index, RINGS_NUM)
    
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
        