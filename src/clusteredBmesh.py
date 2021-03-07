import bpy
import bmesh
import random

import faceUtils

class ClusteredBMesh:
    """
    Helper class to cluster a mesh in a region-growing based fashion
    """
    def __init__(self, bm):
        self.availableFaces = list(range(len(bm.faces))) #The index of the faces not belonging to any cluster
        self.clusters = [] #A list of list of all faces, grouped by the cluster they belong to
        self.candidateFaces = {} #Faces that neighboured a candidate face for the current cluster. Format is candidateFaceIdx : neighbourIdx
        self.incompatibleFaces = [] #For the current cluster, the index of faces that can't be added to the current cluster

    def createNewCluster(self, resetPreviousSearch = False):
        self.clusters.append([])
        if resetPreviousSearch:
            self.candidateFaces = {}
            self.incompatibleFaces = []

    def addFaceToLastCluster(self, face):
        if not face.index in self.clusters[-1]:
            face.select = True
            self.clusters[-1].append(face.index)
            if face.index in self.availableFaces:
                self.availableFaces.remove(face.index)
            while face.index in self.candidateFaces:
                self.candidateFaces.pop(face.index)

            for neighbourFace in faceUtils.getFaceAdjacentFaces(face):
                self.addFaceAsCandidate(face, neighbourFace)
        else:
            raise(Exception("Couldn't add face of index {} : Already in the cluster".format(face.index)))
                
    def addFaceAsCandidate(self, baseFace, candidateFace):
        if (not (candidateFace.index in self.candidateFaces)) and (not (candidateFace.index in self.clusters[-1])) and (not (candidateFace.index in self.incompatibleFaces)):
            self.candidateFaces[candidateFace.index] = baseFace.index

    def setFaceAsIncompatible(self, face):
        if face.index in self.candidateFaces:
            self.candidateFaces.pop(face.index)
        self.incompatibleFaces.append(face.index)
    
    def areFacesCandidateForLastCluster(self):
        return (len(self.candidateFaces) > 0)

    def getACandidateFace(self):
        candidateIdx = list(self.candidateFaces.keys())[-1]
        return candidateIdx, self.candidateFaces[candidateIdx]