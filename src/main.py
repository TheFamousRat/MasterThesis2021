#Importing static modules
 
import bpy
import bmesh
from PIL import Image
import sys
import os

#Loading user-defined modules (subject to frequent changes and needed reloading)
pathsToAdd = ["/home/home/thefamousrat/Documents/KU Leuven/Master Thesis/MasterThesis2021/src"]

for pathToAdd in pathsToAdd:
    sys.path.append(pathToAdd)

import basicUtils 
import faceUtils

import importlib
importlib.reload(basicUtils)
importlib.reload(faceUtils)

for pathToAdd in pathsToAdd:
    sys.path.remove(pathToAdd)

### FUNCTIONS

def cacheTextures(bm, cachedImagesDic):
    """
    Caches the automatically generated material textures into a given dict object
    """
    uniqueMats = set([])
    for face in bm.faces:
        uniqueMats.add(face.material_index)
    for matIdx in uniqueMats:
        blenderTexture = faceUtils.getMaterialTexture(currentObject.material_slots[matIdx].material)
        cachedImages[matIdx] = Image.open(bpy.path.abspath(blenderTexture.filepath), 'r').convert('HSV')
        
### CODE

currentObject = bpy.context.object

if currentObject is None:
    raise(Exception("Please select the mesh on which you want to operate"))

if currentObject.type != 'MESH':
    raise(Exception("Please select a mesh object (selected type : {})".format(currentObject.type)))

print("Loading the mesh info...")
bm = bmesh.new()
bm.from_mesh(currentObject.data)
bm.faces.ensure_lookup_table()

#We load and cache the images for easy access to the pixels
print("Caching face textures...")
cachedImages = {}
cacheTextures(bm, cachedImages)

print("Tests")
cluster = []

face1 = bm.faces[0]
face2 = bm.faces[1]
print(faceUtils.getFacePixelsDistance(bm, face1, face2, cachedImages))

#Somehow needed to prevent memory leaks (gc = garbage collector)
import gc
gc.collect()