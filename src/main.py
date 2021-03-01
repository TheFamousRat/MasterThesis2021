#First loading user-defined modules (subject to frequent changes)

import sys

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

#Importing static modules
 
import bpy
import bmesh
#import KS2D 

### CODE

currentObject = bpy.context.object

if currentObject is None:
    raise(Exception("Please select the mesh on which you want to operate"))

if currentObject.type != 'MESH':
    raise(Exception("Please select a mesh object (selected type : {})".format(currentObject.type)))

bm = bmesh.new()
bm.from_mesh(currentObject.data)
bm.faces.ensure_lookup_table()

imagesPixels = {}

#Loop will start here...
face = bm.faces[2]
faceImage = faceUtils.getFaceImage(currentObject, face)
if not faceImage in imagesPixels:
    imagesPixels[faceImage] = faceImage.pixels[:]
facePixelCoords = faceUtils.getFacePixels(currentObject, bm, face)
pixelColors = [basicUtils.getImagePixelColor_HS(imagesPixels[faceImage], faceImage.size[0], int(pixelCoords[0]), int(pixelCoords[1])) for pixelCoords in facePixelCoords]

ret = str(pixelColors).replace('[', 'c(').replace(']', ')')

    
print(ret)