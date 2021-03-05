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

### CODE

currentObject = bpy.context.object

if currentObject is None:
    raise(Exception("Please select the mesh on which you want to operate"))

if currentObject.type != 'MESH':
    raise(Exception("Please select a mesh object (selected type : {})".format(currentObject.type)))

print("Loading the mesh info...")
bm = bmesh.from_edit_mesh(currentObject.data)
bm.faces.ensure_lookup_table()

#We load and cache the images for easy access to the pixels
print("Caching face textures...")
cachedImages = {}
cacheTextures(currentObject, bm, cachedImages)

print("Tests")
cluster = []

fileObj = open("facePixels.csv", "w")
fileObj.write("H,S,faceIdx\n")
fileObj.close()

fileObj = open("facePixels.csv", "a")
for i in range(0,100000,100):
    face = bm.faces[i]
    face.select = True
    fileObj.write(getFaceCSVstr(bm, face, cachedImages))
bmesh.update_edit_mesh(currentObject.data, True)

fileObj.close()
#Somehow needed to prevent memory leaks (gc = garbage collector)
import gc
gc.collect()