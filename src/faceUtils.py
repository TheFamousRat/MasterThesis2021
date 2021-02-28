import bpy
import bmesh
import math
import numpy as np

def getFaceAdjacentFaces(face):
    """Returns an array of faces representing the indices of faces neighbouring face"""
    ret = []
    for edge in face.edges:
        for edgeFace in edge.link_faces:
            if edgeFace != face:
                ret.append(edgeFace)
    
    return ret

def getFacePixels(ob, bm, face):
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
    faceImageTexture = ob.material_slots[face.material_index].material.node_tree.nodes["Image Texture"].image
    loopPixelCoords = []
    for loop in face.loops:
        #Transforming the triangle's uv coords into pixel coords
        uvCoords = loop[uvLayer].uv
        uvCoordsNorm = [math.fmod(uvCoords[0], 1.0), math.fmod(uvCoords[1], 1.0)]
        loopPixelCoords.append(np.array([math.floor(uvCoordsNorm[0] * faceImageTexture.size[0]), math.floor(uvCoordsNorm[1] * faceImageTexture.size[1])]))

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

    stepSize = 0.5
    alpha = 0.0
    beta = 0.0
    facePixelsCoords = []
    while alpha * d0SizeRatio < 1.0:
        beta = 0.0
        while beta * d1SizeRatio < alpha * d0SizeRatio:
            currentPixelPos = np.floor(loopPixelCoords[0] + alpha * d0 + beta * d1)
            if not (True in [np.array_equal(pixelCoord, currentPixelPos) for pixelCoord in facePixelsCoords]):
                facePixelsCoords.append(currentPixelPos)

            beta += 0.5
        alpha += 0.5

    return facePixelsCoords

    