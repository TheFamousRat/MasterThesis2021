import math
import time
import threading
import sys
import pickle

import numpy as np
from scipy.spatial.distance import cdist
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

import bpy
import bmesh

import basicUtils

INV_255 = 1.0/255.0
PI_TIMES_2 = 2.0 * math.pi
 
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

def getFacePixels(bm, face, img, stepSize = 1.0):
	"""Find a face's shader texture, and returns a list of its corresponding pixels coordinates (from UV)

	:param ob: The original object
	:type ob: Mesh
	:param bm: The face's corresponding bmesh
	:type bm: bmesh
	:param face: The face's BMFace object
	:type face: BMFace
	:param stepSize: Step size for the scan line algorithm. Must be between 0 and 1. Smaller values (closer to 0) yield better results, but are slower 
	:type stepSize: float
	:returns: a list of pixel coordinates
	:rtype: list
	"""
	uvLayer = bm.loops.layers.uv.active
	loopPixelCoords = []
	for loop in face.loops:
		#Transforming the triangle's uv coords into pixel coords
		uvCoords = loop[uvLayer].uv
		uvCoordsNorm = [math.fmod(uvCoords[0], 1.0), 1.0 - math.fmod(uvCoords[1], 1.0)] #inverting the y-axis to go from UV space to pixel space
		loopPixelCoords.append(np.array([math.floor(uvCoordsNorm[0] * img.size[0]), math.floor(uvCoordsNorm[1] * img.size[1])]))
	
	#Using a scan-line algorithm to "rasterize" the triangle to a pixel grid, whose coordinates we save and return
	d0 = loopPixelCoords[1] - loopPixelCoords[0]
	d1 = loopPixelCoords[2] - loopPixelCoords[1]
	d0BaseLen = np.linalg.norm(d0)
	d1BaseLen = np.linalg.norm(d1)

	if not ((d0BaseLen > 0.0) and (d1BaseLen > 0.0)):
		return []
	
	maxLength = max(d0BaseLen, d1BaseLen)
	d0 = d0/maxLength
	d1 = d1/maxLength
	d0NewLen = np.linalg.norm(d0)
	d1NewLen = np.linalg.norm(d1)
	d0SizeRatio = d0NewLen/d0BaseLen
	d1SizeRatio = d1NewLen/d1BaseLen

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
	ret = [convert_color( sRGBColor(*img.getpixel( (int(pixelCoords[0]), int(pixelCoords[1])) ), True), LabColor ).get_value_tuple() for pixelCoords in facePixelsCoords]
	return np.array(ret, dtype='float16')

def getFaceCSVstr(bm, face, imagesCache):
    ret = ""
    
    pixels = getFacePixelColors(bm, face, imagesCache[face.material_index])
    for pixel in pixels:
        ret += str(pixel[0]) + "," + str(pixel[1]) + "," + str(face.index) + "\n"
    return ret

def bakeFacesArrayInfo(bm, idxArray, bakedFacesInfo, threadIdx, threadsProgressList, infoFunc, infoFuncParams):
    for i in range(len(idxArray)):
        faceIdx = idxArray[i]
        bakedFacesInfo[faceIdx] = infoFunc(bm, bm.faces[faceIdx], *infoFuncParams)
        
        threadsProgressList[threadIdx] = i

def bakeFacePixelsColors(bm, face, cachedMatImages):
	"""
	Returns the pixels of the a face as serialized list
	"""
	pixels = getFacePixelColors(bm, face, cachedMatImages[face.material_index])
	return [x for pixel in pixels for x in pixel]

def bakeFacePixelsColorsStatistics(bm, face, bakedPixelsColors):
	"""
	Returns the pixels of the a face as serialized list
	"""
	pixels = readCompressedPixels(bakedPixelsColors[face.index], 3)
	return getFaceColorStatistics(pixels)

def giveThreadsState(threadsList, threadsProgressList, threadsWorkSize):
	"""
	Updater function that prints to the console a string giving the progress state of the threads
	"""
	while True:
		aliveThreadsCount = 0
		threadsReportStr = ""
		totalWorkDone = 0
		totalWorkToDo = 0

		for i in range(len(threadsList) - 1):
			totalWorkToDo += threadsWorkSize[i]

			thread = threadsList[i]
			threadsReportStr += "Thread {} : ".format(i)

			if thread.is_alive():

				aliveThreadsCount += 1
				workProgress = float(threadsProgressList[i] + 1) / float(threadsWorkSize[i])
				threadsReportStr += str( 100.0 * workProgress ) + " %"

				totalWorkDone += threadsProgressList[i] + 1
			else:
				threadsReportStr += "Done."
				totalWorkDone += threadsWorkSize[i]
			
			threadsReportStr += '\n'

		workProgress = float(totalWorkDone) / float(totalWorkToDo)
		barSize = 20.0
		threadsReportStr += 'Progress : |{}{}| ({} %)\n'.format('*'*int(workProgress*barSize), ' '*int((1.0 - workProgress)*barSize), 100.0 * workProgress)
		sys.stdout.write(threadsReportStr)

		if aliveThreadsCount == 0:
			break
		else:
			time.sleep(0.5)
        

def bakeFacePixels(bm, fileName, threadsAmount, cachedImages):
	bakeFacesInfo(bm, fileName, threadsAmount, bakeFacePixelsColors, (cachedImages,))

def bakeFacePixelsStatistics(bm, fileName, threadsAmount, bakedPixels):
	bakeFacesInfo(bm, fileName, threadsAmount, bakeFacePixelsColorsStatistics, (bakedPixels,))

def bakeFacesInfo(bm, fileName, threadsAmount, infoFunc, infoFuncParams):
	"""
	Multi-threaded process to bake info relating to a faces of the mesh to a binary file
	:param bm: BMesh of the object
	:type bm: BMesh
	:param fileName: Path of the binary file to dump the pixels to
	:type fileName: str
	:param cachedMatImages: List of images cached from material's textures
	:type cachedMatImages: list
	:param threadsAmount: Number of threads
	:type threadsAmount: int
	"""
	start = time.time()
	
	bakedFacesInfo = {}
	facesCount = len(bm.faces)

	arrayLimits = list(range(0,facesCount, int(facesCount/threadsAmount)))
	if not ((facesCount - 1) in arrayLimits):
		arrayLimits.append(facesCount)
	arrayLimits[-1] = facesCount

	threads = []
	threadsProgressList = [0 for i in range(threadsAmount)]
	threadsWorkSize = []
	for i in range(threadsAmount):
		#Creating the new thread
		workedIndex = list(range(arrayLimits[i], arrayLimits[i+1]))
		newThread = threading.Thread(target=bakeFacesArrayInfo, args=(bm, workedIndex, bakedFacesInfo, i, threadsProgressList, infoFunc, infoFuncParams,))
		threads.append(newThread)
		newThread.start()
		#Gathering information for the updater
		threadsWorkSize.append(len(workedIndex))
		
	#Creating a thread to follow the thread's progress
	updaterThread = threading.Thread(target=giveThreadsState, args=(threads, threadsProgressList, threadsWorkSize,))
	threads.append(updaterThread)
	updaterThread.start()

	for t in threads:
		t.join()

	end = time.time()
	print("Baking done in {} seconds".format(end - start))

	#Emptying the file before writing
	with open(fileName, 'wb') as f:
		pickle.dump(bakedFacesInfo, f)

	print("File baked to {}".format(fileName))

def readCompressedPixels(compPixels, colorDim):
    return np.array([[compPixels[pixelIdxStart+i] for i in range(colorDim)] for pixelIdxStart in range(0, len(compPixels), colorDim)])

def normalizeCompressedPixels(compPixels, colorSpace):
	"""
	From an array of compressed pixels, (so just plain list, not a list of lists), returns the decompressed and normalized form of the colors
	"""
	colorsDims = 3
	normalizer = np.array([1.0,1.0,1.0])
	if colorSpace == "HS":
		colorsDims = 2
		normalizer = np.array([PI_TIMES_2 * INV_255, INV_255])
	elif colorSpace == "HSV":
		colorsDims = 3
		normalizer = np.array([PI_TIMES_2 * INV_255, INV_255, INV_255])
	elif colorSpace == "RGB":
		colorsDims = 3
		normalizer = np.array([INV_255, INV_255, INV_255])
	
	decompressedPixels = readCompressedPixels(compPixels, colorsDims)
	return [np.multiply(np.array(pixel), normalizer).tolist() for pixel in decompressedPixels]

def squaredEuclideanNorm(vA, vB):
	v = vA - vB
	return np.dot(v,v)

def test(col1, col2):
	return pow(delta_e_cie2000(col1[0], col2[0]), 2.0)

def getFaceColorStatistics(pixelColors):
	#1/Project the colors to the color cone, a space where the distance between colors can be the euclidean one
	#projectedFacePixels = []
	#for pixelCol in pixelColors:
	#	projectedFacePixels.append([math.cos(pixelCol[0]) * pixelCol[1], math.sin(pixelCol[0]) * pixelCol[1]])
	#projectedFacePixels = np.array(projectedFacePixels)

	n = len(pixelColors)
	#2/Calculate the centroid of the projected point cloud (meanA = a.mean(0).tolist())
	centroid = pixelColors.mean(0)
	#3/Calculate the sample standard deviation
	labColorObjects = [[LabColor(*(pixelCol))] for pixelCol in pixelColors]
	centroidColor = [[LabColor(*centroid)]]

	inertia = np.sum(cdist(labColorObjects, centroidColor, test)) / float(n - 1)

	return getFaceStatsFormated(n, centroid, inertia)

def getFaceStatsFormated(n, centroid, inertia):
	return {"n" : n, "center" : centroid, "std" : inertia}