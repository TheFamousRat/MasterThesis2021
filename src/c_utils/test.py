import os
import pickle, lzma

from scipy.sparse import data

def retrieveBakedData(bakedDataPath, integrityCheckFunction, sourceDataIdx, dataBakingFunction):
    """
    
    
    """
    if os.path.exists(bakedDataPath):
        retrievedData = []
        print("Baked textures file found in {}. Loading...".format(bakedDataPath))
        with lzma.open(bakedDataPath, 'rb') as f:
            retrievedData = pickle.load(f) 
        
        print("Checking integrity...")
        refIdx = 0
        integrityCheckSuccess = integrityCheckFunction(refIdx, retrievedData[refIdx])
        
        if integrityCheckSuccess:
            print("Patch integrity test successful")
            return retrievedData
        else:
            print("Outdaded or invalid baked textures found, rebaking all textures")
            bakedData = [None] * len(sourceDataIdx)
            print("Baking patch textures...")

            bar = Bar('Extracting patch textures', max=len(sourceDataIdx))
            for dataIdx in sourceDataIdx:
                bakedData[dataIdx] = dataBakingFunction(dataIdx)
                bar.next()
            
            print("Dumping into a binary file...")
            with lzma.open(bakedDataPath, 'wb') as f:
                pickle.dump(bakedData, f)
            print("Done")
