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

print(faceUtils.getFacePixels(currentObject, bm, bm.faces[0]))