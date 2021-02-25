import math
import numpy as np
import pymesh
import random

from meshEditor import MeshEditor

def getFaceNormal(meshEditorObj, faceIdx):
    faceVertices = meshEditorObj.baseMesh.faces[faceIdx]

    v0 = np.array(meshEditorObj.getProposedVertexPos(faceVertices[0]))
    v1 = np.array(meshEditorObj.getProposedVertexPos(faceVertices[1]))
    v2 = np.array(meshEditorObj.getProposedVertexPos(faceVertices[2]))

    d0 = v1 - v0
    d1 = v2 - v0

    crossProd = np.cross(d0, d1)

    return crossProd / np.linalg.norm(crossProd)

def getDihedralAngle(meshEditorObj, v0, v1):
    #We first the two faces adjacent to the edge formed by v0;v1
    faces_v0 = meshEditorObj.baseMesh.get_vertex_adjacent_faces(v0)
    faces_v1 = meshEditorObj.baseMesh.get_vertex_adjacent_faces(v1)

    adjFaces = [faceIdx for faceIdx in faces_v0 if faceIdx in faces_v1]

    #Sanity check
    if len(adjFaces) != 2:
        raise(Exception("Error : edge doesn't have 2 neighbouring faces"))

    n0 = getFaceNormal(meshEditorObj, adjFaces[0])
    n1 = getFaceNormal(meshEditorObj, adjFaces[1])
    
    return math.acos(np.dot(n0, n1) / (np.linalg.norm(n0) * np.linalg.norm(n1)))

def getVertexEnergy(meshEditorObj, vertexIdx, alpha, vertexPosition = None):
    if vertexPosition == None:
        vertexPosition = meshEditorObj.proposedVerticesPos[vertexIdx]

    #Computing the neighbourhood energy, by adding the energy of all cliques
    priorEnergy = 0.0
    for neighbourVertexIdx in meshEditorObj.baseMesh.get_vertex_adjacent_vertices(vertexIdx):
        edgeDihedralAngle = getDihedralAngle(meshEditorObj, vertexIdx, neighbourVertexIdx)
        priorEnergy += meshEditorObj.getProposedEdgeLength(vertexIdx, neighbourVertexIdx) * edgeDihedralAngle

    #Computing the likelihood energy, by penalizing large deviation from the input data
    v0 = np.array(meshEditorObj.getOriginalVertexPos(vertexIdx))#Vertex position in the base mesh
    v = np.array(vertexPosition)#Current vertex position
    likelihoodEnergy = alpha * np.linalg.norm(v0 - v)

    return likelihoodEnergy + priorEnergy

def getNewPositionProbabilityRatio(meshEditorObj, vertexIdx, proposedPosition, alpha, temperature):
    #We first get the energy of the current proposed position
    currentPositionEnergy = getVertexEnergy(meshEditorObj, vertexIdx, alpha)

    #We then get the energy of the proposed position
    proposedPositionEnergy = getVertexEnergy(meshEditorObj, vertexIdx, alpha, proposedPosition)

    return math.exp((currentPositionEnergy - proposedPositionEnergy)/temperature)

def proposeVertexPosition(meshEditorObj, vertexIdx):
    pass

meshEditor = MeshEditor("data/texturedMesh.obj")
print(getNewPositionProbabilityRatio(meshEditor, 0, [0,0,0], 1.0, 1.0))