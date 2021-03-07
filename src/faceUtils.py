import math
import time
import threading
import sys
import pickle

import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment

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
	return [img.getpixel( (int(pixelCoords[0]), int(pixelCoords[1])) ) for pixelCoords in facePixelsCoords]

def getFacePixelsDistance(face1PixelColors, face2PixelColors):
	"""
	Computes and returns the Earth Mover Distance between the pixels of both faces
	:param face1PixelColors: The pixels of the first face
	:type face1PixelColors: list
	:param face2PixelColors: The pixels of the second face
	:type face2PixelColors: list
	"""

	Cmat = cdist(face1PixelColors, face2PixelColors, basicUtils.colHSVDist)
	assignment = linear_sum_assignment(Cmat)
	return (Cmat[assignment].sum() / len(Cmat[assignment]))

def getFaceCSVstr(bm, face, imagesCache):
    ret = ""
    
    pixels = getFacePixelColors(bm, face, imagesCache[face.material_index])
    for pixel in pixels:
        ret += str(pixel[0]) + "," + str(pixel[1]) + "," + str(face.index) + "\n"
    return ret

def bakePixelsArray(bm, idxArray, bakedPixels, threadIdx, threadsProgressList, cachedMatImages):
    for i in range(len(idxArray)):
        faceIdx = idxArray[i]
        face = bm.faces[faceIdx]
        pixels = getFacePixelColors(bm, face, cachedMatImages[face.material_index])
        bakedPixels[faceIdx] = [pixel[pxId] for pixel in pixels for pxId in range(2)]
        
        threadsProgressList[threadIdx] = i

def giveThreadsState(threadsList, threadsProgressList, threadsWorkSize):
    start = time.time()
    
    while True:

        aliveThreadsCount = 0
        maxTimeRemaining = 0.0
        threadsReportStr = ""

        for i in range(len(threadsList) - 1):

            timeElapsed = time.time() - start
            thread = threadsList[i]
            threadsReportStr += "Thread {} : ".format(i)

            if thread.is_alive():

                aliveThreadsCount += 1
                workProgress = float(threadsProgressList[i] + 1) / float(threadsWorkSize[i])
                threadsReportStr += str( 100.0 * workProgress ) + " %"

                threadTimeRemaing = timeElapsed * ((1.0 / workProgress) - 1.0)
                maxTimeRemaining = max(maxTimeRemaining, threadTimeRemaing)
            else:

                threadsReportStr += "Done."
            
            threadsReportStr += '\n'

        threadsReportStr += 'Remaining time : {} s\n'.format(maxTimeRemaining)
        sys.stdout.write(threadsReportStr)

        if aliveThreadsCount == 0:
            break
        else:
            time.sleep(0.5)
        

def bakeFacePixels(bm, fileName, cachedMatImages, threadsAmount = 4):
    bakedPixels = {}
    facesCount = len(bm.faces)
    
    arrayLimits = list(range(0,facesCount, int(facesCount/threadsAmount)))
    if not ((facesCount - 1) in arrayLimits):
        arrayLimits.append(facesCount)

    threads = []
    threadsProgressList = [0 for i in range(threadsAmount)]
    threadsWorkSize = []
    for i in range(threadsAmount):
        #Creating the new thread
        workedIndex = list(range(arrayLimits[i], arrayLimits[i+1]))
        newThread = threading.Thread(target=bakePixelsArray, args=(bm, workedIndex, bakedPixels, i, threadsProgressList, cachedMatImages,))
        threads.append(newThread)
        newThread.start()
        #Gathering information for the updater
        threadsWorkSize.append(len(workedIndex))
        
    #Creating a thread to follow the thread's progress
    updaterThread = threading.Thread(target=giveThreadsState, args=(threads, threadsProgressList, threadsWorkSize,))
    updaterThread.start()
    threads.append(updaterThread)
    print(len(threads))
    for t in threads:
        t.join()
    
    #Emptying the file before writing
    with open(fileName, 'wb') as f:
        pickle.dump(bakedPixels, f)