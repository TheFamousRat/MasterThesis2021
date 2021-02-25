import math
import numpy as np
import pymesh

class MeshEditor:
    # A helper class to interact with the structure of the pymesh objects
    # The goal now is to simply add logic to edit the vertices positions (and not the rest of the mesh structure)
    def __init__(self, filepath):
        self.baseMesh = pymesh.load_mesh(filepath)
        self.baseMesh.enable_connectivity()
        self.proposedVerticesPos = self.baseMesh.vertices.copy()

    def getProposedEdgeLength(self, v0Idx, v1Idx):
        return np.linalg.norm(np.array(self.proposedVerticesPos[v0Idx]) - np.array(self.proposedVerticesPos[v1Idx]))

    def setProposedVertexPos(self, vIdx, value):
        self.proposedVerticesPos[vIdx] = value

    def getProposedVertexPos(self, vIdx):
        return self.proposedVerticesPos[vIdx]
    
    def getOriginalVertexPos(self, vIdx):
        return self.baseMesh.vertices[vIdx]