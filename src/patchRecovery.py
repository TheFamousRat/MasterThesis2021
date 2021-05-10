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
    
### Functions
def getMeshHash(obj):
    return hashlib.sha224( str(obj.data.vertices).strip('[]').encode('utf-8') ).hexdigest()
    
### Logic
#Creating the bmesh
selectedObj = bpy.context.active_object

if selectedObj.type != "MESH":
    raise Exception("Please choose a mesh")
    
bm = bmesh.from_edit_mesh(selectedObj.data)
bm.faces.ensure_lookup_table()

#Storage for mesh data
meshDataPath = os.path.join(bpy.path.abspath("//"), 'meshesData/{}/'.format(getMeshHash(currentObject)))
if not os.path.exists(meshDataPath):
    os.makedirs(meshDataPath)

#Covering the mesh with patches
meshPatches = []

start = time.time()
for face in bm.faces:
    meshPatches.append(patch.Patch(bm, face.index, 2))

end = time.time()
print("Time taken : {} seconds".format(end - start))
