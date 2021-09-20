# -*- coding: utf-8 -*-
"""
Spyder Editor

Program to setup various ER formats to analyze performance of comparing ERs 
(dot products)

v1 - Initial cut
        erDict['name'] = dictionary of various ER formats
                'descriptione' : deswcription of format
                'er1'  : first_ER
                'er2'  : second_ER
        formatTypes = [ list of above 'name' keys to use in the anlysis]

            
        Note:  thanks to shippo author Wissam Jarjoui for method to recursively calculate the total 
                space used for a Python object  (get_size)
                
-------------------

v1 - This is a variant of the buildCompareERs that calculates the (average) storage
     requirement for each type of data structure.
        
"""

import time, datetime, random, sys, pickle
from statistics import mean, stdev
from bitarray import bitarray
# sys.path.append('c:/users/talan/documents/krune_git/ganDemo')
# from extAssocMemV13 import AssocMem, AssocMemItem
# from fileDialogs import App


def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

def buildBasicERs(erSize,nodePool,quantity):
    baseERs = []
    for i in range(0,quantity):
        baseERs.append(random.sample(range(0,nodePool),erSize))
    return baseERs

def buildSetizedERs(listERs):
    setERs = []
    for i in range(0,len(listERs)):
        setERs.append(set(listERs[i]))
    return setERs

def buildSortedListERs(baseERs):
    sortedERs = []
    for i in range(0,len(baseERs)):
        sortedERs.append(sorted(baseERs[i]))
    return sortedERs

def buildBitArrayERs(baseERs,nodePool):
    bitArrayERs = []
    for i in range(0,len(baseERs)):
        bitArray = nodePool * bitarray('0')
        for item in baseERs[i]:
            bitArray[item] = True
        bitArrayERs.append(bitArray)
    return bitArrayERs
    

#########################################################################################

def main():
    
    # test_binary_search()
    start = datetime.datetime.now()
    print("start: ",start)
    print("")
    
    erSizesList = [64,256,1024,4096,16384]   #8,16,
    nodePoolSizesList = [2**10,2**16]    #[2**6,2**14,2**20 ]
    quantityList = [4,64,1024]   #[1,4,16,64,256,1024,4096]

    
    resultsList = []
    erDict = {}
    
    # generate file name for results    fileTime= datetime.datetime.now()
    fileTime= datetime.datetime.now()   
    timeId = fileTime.strftime("%y%m%d-%H%M%S")
    sizingResults_fileName = 'data/sizingResults-erFormat-'+timeId+'.srefPkl'
 
    # perform testing for lists, sorted lists, and sets
    for i in range(0,len(erSizesList)):
        erSize = erSizesList[i]
        
        for j in range(0,len(nodePoolSizesList)):
            nodePool = nodePoolSizesList[j]
            
            if erSize > nodePool:
                continue
            
            for k in range(0,len(quantityList)):
                quantity = quantityList[k]
                currentTime = datetime.datetime.now()
                currentTimeId = currentTime.strftime("%y%m%d-%H%M%S")
                print("")
                print("Start new iteration")
                print("  currentTime: ",currentTimeId)

                dictItem = {'erSize1:':erSize,'nodePool':nodePool,'quantity':quantity}            
                print("  ",dictItem)
        
                # generate base ERs
                baseERs = buildBasicERs(erSize,nodePool,quantity)
                dictItem['uoListERs'] = {'description':'unordered lists of nodes', \
                                     'lengths':[erSize],'nodePool':nodePool, \
                                     'quantity':quantity, \
                                     'memorySpace':get_size(baseERs)}                
                # sorted List ERs
                sortedERs = buildSortedListERs(baseERs)
                dictItem['oListERs'] = {'description':'ordered lists of nodes',\
                                     'lengths':[erSize],'nodePool':nodePool,\
                                     'quantity':quantity, \
                                     'memorySpace':get_size(sortedERs)}  
                     
                # setized ERs
                setERs = buildSetizedERs(baseERs)
                dictItem['setERs'] = {'description':'sets of nodes',\
                                     'lengths':[erSize],'nodePool':nodePool,\
                                     'quantity':quantity, \
                                     'memorySpace':get_size(setERs)}      
              
                print("dictItem: ",dictItem)
                resultsList.append(dictItem)
                
                # write results to file
                print("")
                print("Writing sizingResults pickle file: ",sizingResults_fileName)
                       
                afile = open(sizingResults_fileName, 'wb')
                pickle.dump(resultsList, afile)
                
                afile.close()
                print("")
                print("Finished writing a sizingResults pickle file: ",sizingResults_fileName) 
                print("")
                print("")


    erSizesList = [64,256,1024,4096,16384]      #  [64,1024,16384]   #8,16,
    nodePoolSizesList = [2**10,2**16]  #[2**6,2**14,2**20]
    quantityList = [4,64,1024]   #[1,4,16,64,256,1024,4096]
    
    for i in range(0,len(erSizesList)):
        erSize = erSizesList[i]
        
        for j in range(0,len(nodePoolSizesList)):
            nodePool = nodePoolSizesList[j]
            if erSize > nodePool:
                continue
            
            for k in range(0,len(quantityList)):
                quantity = quantityList[k]
                currentTime = datetime.datetime.now()
                currentTimeId = currentTime.strftime("%y%m%d-%H%M%S")
                print("")
                print("Start new iteration")
                print("  currentTime: ",currentTimeId)

                dictItem = {'erSize1:':erSize,'nodePool':nodePool,'quantity':quantity}            
                print("  ",dictItem)
                
                # build the base ERs list for the subequent encoding to bitarray
                baseERs = buildBasicERs(erSize,nodePool,quantity)
                
                # binary array ERs
                bitArrayERs = buildBitArrayERs(baseERs,nodePool)
                dictItem['bArrayERs'] = {'description':'bitArrays',\
                                      'lengths':[erSize],'nodePool':nodePool,\
                                      'quantity':quantity, \
                                      'memorySpace': get_size(bitArrayERs)} 
              
                # print("erDict: ",erDict)
                resultsList.append(dictItem)
        
                print("resultsList: ",resultsList) 
                
                # write results to file
                print("")
                print("Writing sizingResults pickle file: ",sizingResults_fileName)
                       
                afile = open(sizingResults_fileName, 'wb')
                pickle.dump(resultsList, afile)
                
                afile.close()
                print("")
                print("Finished writing a sizingResults pickle file: ",sizingResults_fileName) 
                print("")
                print("")
        
    print("done")
    print("")
    return
    
######################################

if __name__ == "__main__":
    main()