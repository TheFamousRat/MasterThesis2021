import threading
import time
import sys

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
        self.candidateFaces = {} #Faces that neighboured a candidate face for the current cluster. Format is candidateFaceIdx : [possible neighbourIdx]
        self.incompatibleFaces = [] #For the current cluster, the index of faces that can't be added to the current cluster
        self.updaterThread = None
        self.giveUpdates = False

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
            if face.index in self.candidateFaces:
                self.candidateFaces.pop(face.index)

            for neighbourFace in faceUtils.getFaceAdjacentFaces(face):
                self.addFaceAsCandidate(face, neighbourFace)
        else:
            raise(Exception("Couldn't add face of index {} : Already in the cluster".format(face.index)))
                
    def addFaceAsCandidate(self, baseFace, candidateFace):
        if (not (candidateFace.index in self.clusters[-1])) and (not (candidateFace.index in self.incompatibleFaces)):

            if not (candidateFace.index in self.candidateFaces):
                self.candidateFaces[candidateFace.index] = []

            if not (baseFace.index in self.candidateFaces[candidateFace.index]):
                self.candidateFaces[candidateFace.index].append(baseFace.index)

    def setFaceAsIncompatible(self, face):
        if face.index in self.candidateFaces:
            self.candidateFaces.pop(face.index)

        self.incompatibleFaces.append(face.index)

    def areFacesCandidateForLastCluster(self):
        return (len(self.candidateFaces) > 0)

    def getACandidateFace(self, removePairOnReturn = False):
        candidateIdx = list(self.candidateFaces.keys())[-1]
        neighbourIdx = self.candidateFaces[candidateIdx][0]

        if removePairOnReturn:
            self.candidateFaces[candidateIdx].remove(neighbourIdx)
            if len(self.candidateFaces[candidateIdx]) == 0:
                self.candidateFaces.pop(candidateIdx)

        return candidateIdx, neighbourIdx

    def activateProgressFeedback(self):
        self.giveUpdates = True
        self.updaterThread = threading.Thread(target=self.clusteringProgressInfo)
        self.updaterThread.start()

    def deactivateProgressFeedback(self):
        self.giveUpdates = False
        if not (self.updaterThread is None):
            self.updaterThread.join()
        self.updaterThread = None

    def clusteringProgressInfo(self):
        while self.giveUpdates:
            #To be called from a thread
            infoStr = ""
            infoStr += "Current amount of clusters : {}\n".format(len(self.clusters))
            infoStr += "Amount of free faces : {}\n".format(len(self.availableFaces))
            infoStr += "Candidates for current cluster : {}\n".format(len(self.candidateFaces))
            infoStr += "Discarded for current cluster : {}\n".format(len(self.incompatibleFaces))
            print(infoStr)
            time.sleep(0.5)