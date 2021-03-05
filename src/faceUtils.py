import bpy
import bmesh
import math
import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment

import basicUtils

def getFaceAdjacentFaces(face):
	"""
	Returns an array of faces representing the indices of faces neighbouring face
	"""
	ret = []
	for edge in face.edges:
		for edgeFace in edge.link_faces:
			if edgeFace != face:
				ret.append(edgeFace)

	return ret

def getMaterialTexture(mat):
	"""
	Returns the texture from an automatically generated material
	"""
	return mat.node_tree.nodes["Image Texture"].image

def getFaceImage(ob, face):
	return ob.material_slots[face.material_index].material.node_tree.nodes["Image Texture"].image

def getFaceImageName(ob, face):
	return getFaceImage(ob, face).name

def getFacePixels(bm, face, img):
	"""Find a face's shader texture, and returns a list of its corresponding pixels coordinates (from UV)

	:param ob: The original object
	:type ob: Mesh
	:param bm: The face's corresponding bmesh
	:type bm: bmesh
	:param face: The face's BMFace object
	:type face: BMFace
	:returns: a list of pixel coordinates
	:rtype: list
	"""
	uvLayer = bm.loops.layers.uv.active
	loopPixelCoords = []
	for loop in face.loops:
		#Transforming the triangle's uv coords into pixel coords
		uvCoords = loop[uvLayer].uv
		uvCoordsNorm = [math.fmod(uvCoords[0], 1.0), math.fmod(uvCoords[1], 1.0)]
		loopPixelCoords.append(np.array([math.floor(uvCoordsNorm[0] * img.size[0]), math.floor(uvCoordsNorm[1] * img.size[1])]))

	#Using a scan-line algorithm to "rasterize" the triangle to a pixel grid, whose coordinates we save and return
	d0 = loopPixelCoords[1] - loopPixelCoords[0]
	d1 = loopPixelCoords[2] - loopPixelCoords[1]
	d0BaseLen = np.linalg.norm(d0)
	d1BaseLen = np.linalg.norm(d1)
	maxLength = max(d0BaseLen, d1BaseLen)
	d0 = d0/maxLength
	d1 = d1/maxLength
	d0NewLen = np.linalg.norm(d0)
	d1NewLen = np.linalg.norm(d1)
	d0SizeRatio = d0NewLen/d0BaseLen
	d1SizeRatio = d1NewLen/d1BaseLen

	stepSize = 0.5 #Smaller yields better results, but is slower (0.5 seems generally reliable)
	alpha = 0.0
	beta = 0.0
	facePixelsCoords = []
	while alpha * d0SizeRatio < 1.0:
		beta = 0.0
		while beta * d1SizeRatio < alpha * d0SizeRatio:
			currentPixelPos = np.floor(loopPixelCoords[0] + alpha * d0 + beta * d1).tolist()
			if not (currentPixelPos in facePixelsCoords):
				facePixelsCoords.append(currentPixelPos)

			beta += stepSize
		alpha += stepSize

	return facePixelsCoords

def getFacePixelColors(bm, face, img):
	"""
	For a given face and its given texture, returns the array of pixels colors it covers
	"""
	facePixelsCoords = getFacePixels(bm, face, img)
	return [np.array(img.getpixel( (int(pixelCoords[0]), int(pixelCoords[1])) )) / 255.0 for pixelCoords in facePixelsCoords]

def getFacePixelsDistance(bm, face1, face2, imagesCache):
	"""
	Computes and returns the Earth Mover Distance between the pixels of both faces
	:param bm: The face's corresponding bmesh
	:type bm: bmesh
	:param face1: Face object for the first face
	:type face1: BMFace
	:param face2: Face object for the second face
	:type face2: BMFace
	"""
	face1PixelColors = getFacePixelColors(bm, face1, imagesCache[face1.material_index])
	face2PixelColors = getFacePixelColors(bm, face2, imagesCache[face2.material_index])

	Cmat = cdist(face1PixelColors, face2PixelColors, basicUtils.colHSVDist)
	assignment = linear_sum_assignment(Cmat)
	return (Cmat[assignment].sum() / len(Cmat[assignment]))