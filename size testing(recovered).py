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



def buildBasicERs(erSize1,erSize2,nodePool,quantity):
    baseERs1 = []
    baseERs2 = []
    for i in range(0,quantity):
        baseERs1.append(random.sample(range(0,nodePool),erSize1))
        # print("baseERs[",i,"]: ",baseERs1[i])
        saveQty = max(2,int(erSize1/4))
        savePlace = random.randrange(erSize1-saveQty)
        saveNodes = baseERs1[i][savePlace:savePlace+saveQty]
        # print("saveQty/Place/Nodes: ",saveQty,savePlace,saveNodes)
        baseERs2.append(saveNodes + random.sample(range(0,nodePool),erSize2-saveQty))
        # print("baseERs[",i,"]: ",baseERs2[i])
    return baseERs1,baseERs2

def buildSetizedERs(listERs1,listERs2):
    overallStartTime = time.time_ns()
    setERs1 = []
    setERs2 = []
    for i in range(0,len(listERs1)):
        setERs1.append(set(listERs1[i]))
    for i in range(0,len(listERs2)):
        setERs2.append(set(listERs2[i]))
    overallFinishTime = time.time_ns()
    overallDuration = (overallFinishTime - overallStartTime)   # naonseconds
    return setERs1,setERs2, overallDuration


def convertSetizedERs(setERs1,setERs2):    # convert sets to lists--just for evaluation purposes
    overallStartTime = time.time_ns()
    listERs1 = []
    listERs2 = []
    for i in range(0,len(setERs1)):
        listERs1.append(list(setERs1[i]))
    for i in range(0,len(listERs2)):
        listERs2.append(list(setERs2[i]))
    overallFinishTime = time.time_ns()
    overallDuration = (overallFinishTime - overallStartTime)   # naonseconds
    return overallDuration

def buildSortedListERs(baseERs1,baseERs2):
    sortedERs1 = []
    sortedERs2 = []
    for i in range(0,len(baseERs1)):
        sortedERs1.append(sorted(baseERs1[i]))
    for i in range(0,len(baseERs2)):
        sortedERs2.append(sorted(baseERs2[i]))
    return sortedERs1,sortedERs2

def buildBitArrayERs(baseERs1,baseERs2,nodePool):
    bitArrayERs1 = []
    bitArrayERs2 = []
    for i in range(0,len(baseERs1)):
        bitArray = nodePool * bitarray('0')
        for item in baseERs1[i]:
            bitArray[item] = True
        bitArrayERs1.append(bitArray)
    for i in range(0,len(baseERs2)):
        bitArray = nodePool * bitarray('0')
        for item in baseERs2[i]:
            bitArray[item] = True
        bitArrayERs2.append(bitArray)
    return bitArrayERs1,bitArrayERs2


def compareListERs(listERs1,listERs2):
    # this routine uses unsorted lists, and 'if short list item in longList'
    counts = [0 for _ in range(0,len(listERs1))]
    durations = []
    overallStartTime = time.time_ns()
    for i in range(0,len(listERs1)):
        startTime = time.time_ns()
        # print("startTime: ",startTime)
        if len(listERs1[i]) < len(listERs2[i]):
            shortER = listERs1[i]
            longER = listERs2[i]
        else:
            shortER = listERs2[i]
            longER = listERs1[i]
        for item in shortER:
            if item in longER:
                counts[i] += 1
        finishTime = time.time_ns()
        # print("finishTime: ",finishTime)
        duration = (finishTime - startTime)    # naonseconds
        durations.append(duration)
    overallFinishTime = time.time_ns()
    overallDuration = (overallFinishTime - overallStartTime)   # naonseconds 
    return counts,durations,overallDuration

def compareSetERs(setERs1,setERs2):
    # this routine uses unsorted set, and 'if short set item in longSet'
    counts = [0 for _ in range(0,len(setERs1))]
    durations = []
    overallStartTime = time.time_ns()
    for i in range(0,len(setERs1)):
        startTime = time.time_ns()
        if len(setERs1[i]) < len(setERs2[i]):
            shortER = setERs1[i]
            longER = setERs2[i]
        else:
            shortER = setERs2[i]
            longER = setERs1[i]
        for item in shortER:
            if item in longER:
                counts[i] += 1
        finishTime = time.time_ns()
        durations.append(finishTime - startTime)     # naonseconds
    overallFinishTime = time.time_ns()
    overallDuration = (overallFinishTime - overallStartTime)   # naonseconds            
    return counts,durations,overallDuration
    
def compareBitArrayERs(bitArrayERs1,bitArrayERs2):
    counts = []
    durations = []
    overallStartTime = time.time_ns()
    for i in range(0,len(bitArrayERs1)):
        startTime = time.time_ns()
        result = bitArrayERs1[i] & bitArrayERs2[i]
        counts.append(result.count())
        finishTime = time.time_ns()
        durations.append(finishTime - startTime)    # naonseconds
    overallFinishTime = time.time_ns()
    overallDuration = (overallFinishTime - overallStartTime)   # naonseconds
    return counts,durations,overallDuration

def binary_search(arr, x,startAt=0):
    low = startAt
    high = len(arr) - 1
    mid = 0
    steps=0
    while low <= high:
        steps += 1
        mid = (high + low) // 2
        # If x is greater, ignore left half
        if arr[mid] < x:
            low = mid + 1
        # If x is smaller, ignore right half
        elif arr[mid] > x:
            high = mid - 1
        # means x is present at mid
        else:
            # print("steps: ",steps)
            return mid, mid+1
    # If we reach here, then the element was not present
    # print("steps: ",steps)
    return -1, low

def test_binary_search():
    # testing binary search algorithms
    a = [1,2,3,7,8]
    b = [1,2,5,6,7,9]
    
    for item in a:
        x,newLow = binary_search(b,item,startAt=0)
        print("item: ",item," x/newLow: ",x,newLow)
    
    print("")
    newLow = 0
    for item in a:
        x,newLow = binary_search(b,item,startAt=newLow)
        print("item: ",item," x/newLow: ",x,newLow)
        
        
def comparePartiallySortedList(baseERs1,sortedERs2):
    counts = [0 for _ in range(0,len(baseERs1))]
    durations = []
    overallStartTime = time.time_ns()
    for i in range(0,len(baseERs1)): 
        startTime = time.time_ns()
        a = baseERs1[i]
        b = sortedERs2[i]
        for item in a:
            x,newLow = binary_search(b,item,startAt=0)
            if x != -1:
                counts[i] += 1
        finishTime = time.time_ns()
        durations.append(finishTime - startTime)      # naonseconds 
    overallFinishTime = time.time_ns()
    overallDuration = (overallFinishTime - overallStartTime)   # naonseconds
    return counts,durations,overallDuration
 

def compareSortedList(sortedERs1,sortedERs2):
    counts = [0 for _ in range(0,len(sortedERs1))]
    durations = []
    overallStartTime = time.time_ns()
    for i in range(0,len(sortedERs1)): 
        startTime = time.time_ns()
        a = sortedERs1[i]
        b = sortedERs2[i]
        newLow = 0
        for item in a:
            x,newLow = binary_search(b,item,startAt=newLow)
            if x != -1:
                counts[i] += 1
        finishTime = time.time_ns()
        durations.append(finishTime - startTime)      # naonseconds 
    overallFinishTime = time.time_ns()
    overallDuration = (overallFinishTime - overallStartTime)   # naonseconds
    return counts,durations,overallDuration 


     
#########################################################################################


def main():
    
    # test_binary_search()
    start = datetime.datetime.now()
    print("start: ",start)
    print("")
    
    erSizesList = [8,16,32,64,128,256,512,1024,2048,4096,8192,16384]
    nodePoolSizesList = [2**x for x in range(6,21)]
    
    initQuantity =  2**16 
    
    
    for i in range(0,1):    #  len(nodePoolSizesList)):
        for j in range(0,8):
            quantity = 100

            erSize = erSizesList[i]
            nodePool = nodePoolSizesList[j]
            
            
            # generate base ERs
            baseERs, _ = buildBasicERs(erSize1,erSize,nodePool,quantity)

            

             
            startComps = datetime.datetime.now()
            print("")
            print("startComparisons at: ",startComps)
            print("  ersizes: ",erSize1,erSize2)
            print("  nodePool: ",nodePool)
            print("  quantity: ",quantity)
        
            # normal list compare
            # counts,durations,overallDuration = compareListERs(baseERs1,baseERs2)
            lenBaseERs1 = len(baseERs1)
            totalSize = sys.getsizeof(baseERs1)
            summedSize = 0
            meanSize = totalSize/quantity
            individualSize = sys.getsizeof(baseERs1[0])
            individualNodeSize = sys.getsizeof(baseERs1[0][0])
            oneNode = baseERs1[0][0]
            oneNodeSize = sys.getsizeof(oneNode)
            totalNodeSize = 0
            for k in range(0,len(baseERs1[0])):
                totalNodeSize += sys.getsizeof(baseERs1[0][k])
            totalShouldBe = individualSize * quantity
            effectiveERsize = 
            # averageDuration = overallDuration/quantity/1000000
            # stdevDuration = stdev(durations)/1000000
            print("")
            print("list ER sizes")
            print("  quantity: ",quantity)
            print("  lenBaseERs1: ",lenBaseERs1)
            print("  totalSize: ",totalSize)
            print("  meanSize: ",meanSize)
            print("  individualSize: ",individualSize)
            print("  erSize (nodes): ",erSize1)
            print("  len(baseERs1[0]:",len(baseERs1[0]))
            print("  individualNodeSize: ",individualNodeSize)
            print("  totalNodeSize: ",totalNodeSize)
            print("  individualNodeType: ",type(baseERs1[0][0]))
            print("  totalShouldBe: ",totalShouldBe)
            print("  oneNodeSize: ",oneNodeSize)
            print("")
            sizes = []
            for k in range(0,quantity):
                itemSize = sys.getsizeof(baseERs1[k])
                sizes.append(itemSize)
                summedSize += itemSize
                # if itemSize != 128:
                #     print("list sizse that are not 128 bytes: ",k,sys.getsizeof(sys.getsizeof(baseERs1[i])))
            # print("sizes: ",sizes[0:1000])
            print("summedSize/quantity: ",summedSize,quantity)
            print("averageSize: ",summedSize/quantity)
            meanSizes = mean(sizes)
            stdevSizes = stdev(sizes)
            print("  meanSizes: ",meanSizes)
            print("  stdevSizes: ",stdevSizes)
            # print("  averageDuration(ms): ",averageDuration)
            
            
            
            continue

    
######################################

if __name__ == "__main__":
    main()