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
        return 0.0
        #raise(Exception("Error : edge doesn't have 2 neighbouring faces"))

    n0 = getFaceNormal(meshEditorObj, adjFaces[0])
    n1 = getFaceNormal(meshEditorObj, adjFaces[1])
    
    return math.acos(np.dot(n0, n1) / (np.linalg.norm(n0) * np.linalg.norm(n1)))

def getVertexPositionEnergy(meshEditorObj, vertexIdx, alpha, vertexPosition = None):
    if vertexPosition is None:
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
    currentPositionEnergy = getVertexPositionEnergy(meshEditorObj, vertexIdx, alpha)

    #We then get the energy of the proposed position
    proposedPositionEnergy = getVertexPositionEnergy(meshEditorObj, vertexIdx, alpha, proposedPosition)

    return math.exp((currentPositionEnergy - proposedPositionEnergy)/temperature)

def proposeVertexPosition(meshEditorObj, vertexIdx, deviation):
    #We first compute all the dihedral angles for each edge formed with an adjacent vertex
    dihedralAngles = {}
    for neighbourVertexIdx in meshEditorObj.baseMesh.get_vertex_adjacent_vertices(vertexIdx):
        dihedralAngles[neighbourVertexIdx] = getDihedralAngle(meshEditorObj, vertexIdx, neighbourVertexIdx)

    summedFaceAngles = 0.0
    summedWeightedNormals = 0.0
    for faceIdx in meshEditorObj.baseMesh.get_vertex_adjacent_faces(vertexIdx):
        faceVertices = (meshEditorObj.baseMesh.faces[faceIdx]).tolist()
        vertexFaceIdx = faceVertices.index(vertexIdx)
        v1Idx = faceVertices[(vertexFaceIdx+1)%3]
        v2Idx = faceVertices[(vertexFaceIdx+2)%3]

        faceAngle = (dihedralAngles[v1Idx] + dihedralAngles[v2Idx]) / 2.0
        faceNormal = np.array(getFaceNormal(meshEditorObj, faceIdx))

        summedFaceAngles += faceAngle
        summedWeightedNormals += faceAngle * faceNormal * np.random.normal(0.0, deviation)

    return meshEditorObj.proposedVerticesPos[vertexIdx] + (summedWeightedNormals/summedFaceAngles)

filepath = "data/texturedMesh.obj"
print("Mesh loading at path {}...".format(filepath))
meshEditor = MeshEditor(filepath)
print("Done")

iterationsAmount = 1
allVerticesIndices = list(range(0, len(meshEditor.baseMesh.vertices)))
for i in range(0,iterationsAmount): 
    random.shuffle(allVerticesIndices)
    print("Iteration {} out of {}...".format(i+1, iterationsAmount))
    for vIdx in allVerticesIndices:
        proposedPos = proposeVertexPosition(meshEditor, vIdx, 1.0)
        energyRatio = getNewPositionProbabilityRatio(meshEditor, vIdx, proposedPos, 0.1, 1.0)
        u = np.random.uniform(0.0, 1.0)
        if u <= energyRatio:
            meshEditor.setProposedVertexPos(vIdx, proposedPos)

print(meshEditor.baseMesh.vertices[0])
print(proposeVertexPosition(meshEditor, 0, 1.0))