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
        
        
"""

import time, datetime, random, sys, pickle
from statistics import mean, stdev
from bitarray import bitarray
sys.path.append('c:/users/talan/documents/krune_git/ganDemo')
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
    nodePoolSizesList = [2**8,2**10,2**12,2**14,2**16,2**18,2**20]
    
    erDict = {}
    initQuantity =  2**16
    
    resultsList = []
    
    # generate file name for results    fileTime= datetime.datetime.now()
    fileTime= datetime.datetime.now()   
    timeId = fileTime.strftime("%y%m%d-%H%M%S")
    timingResults_fileName = 'data/timingResults-erCompare-'+timeId+'.trecPkl'
    
    for i in range(0,len(erSizesList)):
        for j in range(0,len(nodePoolSizesList)):
    
            erSize1 = erSizesList[i]
            erSize2 = erSizesList[i]
            nodePool = nodePoolSizesList[j]
            

            
            if erSize1 >= nodePool:
                continue
            print("")
            print("Start new iteration")
            print("  erSize1/2,nodePool: ",erSize1,erSize2,nodePool)
            
            # reduce quantity as  the erSize and/or the nodePool increase
            erFactor = max(1,int(erSize1/erSizesList[0]/2))
            print("  erFactor: ",erFactor)
            npFactor = int(nodePool/nodePoolSizesList[0])
            print("  npFactor: ",npFactor)
            quantity = max(1000,int(initQuantity / erFactor / npFactor))
            print("  calculated quantity: ",quantity)

            dictItem = {'erSize1:':erSize1,'erSize2':erSize2,'nodePool':nodePool,'quantity':quantity}            
    
        
            # generate base ERs
            baseERs1, baseERs2 = buildBasicERs(erSize1,erSize2,nodePool,quantity)
            erDict['uoListERs'] = {'description':'unordered lists of nodes', \
                                 'lengths':[erSize1,erSize2],'nodePool':nodePool, \
                                 'ers':[baseERs1,baseERs2]}
            
            # sorted List ERs
            sortedERs1,sortedERs2 = buildSortedListERs(baseERs1,baseERs2)
            erDict['oListERs'] = {'description':'ordered lists of nodes',\
                                 'lengths':[erSize1,erSize2],'nodePool':nodePool,\
                                 'ers': [sortedERs1,sortedERs2]}  
                   
            # setized ERs
            setERs1, setERs2, overallDuration = buildSetizedERs(baseERs1,baseERs2)
            erDict['setERs'] = {'description':'sets of nodes',\
                                 'lengths':[erSize1,erSize2],'nodePool':nodePool,\
                                 'ers': [setERs1,setERs2]}    
            averageDuration = (overallDuration/quantity/1000000)/2     # divide by two because there are two sets lists being converted
            print("")
            print("Convert Lists to Sets")
            print("  overallDuration/quantity(ms): ",overallDuration/1000000/2, quantity)
            print("  averageDuration(ms): ",averageDuration)
            dictItem['setizingResults'] = [averageDuration]
        
        
            # convert sets to list (for analysis purposes--the lists are not used)
            overallDuration = convertSetizedERs(setERs1,setERs2)
            averageDuration = (overallDuration/quantity/1000000)/2     # divide by two because there are two sets lists being converted
            print("")
            print("Convert Sets to Lists")
            print("  overallDuratio(ms)n/quantity: ",overallDuration/1000000/2, quantity)
            print("  averageDuration(ms): ",averageDuration)        
            dictItem['listizingResults'] = [averageDuration]    
                
        
            # binary array ERs
            bitArrayERs1, bitArrayERs2 = buildBitArrayERs(baseERs1,baseERs2,nodePool)
            erDict['bArrayERs'] = {'description':'bitArrays',\
                                 'lengths':[erSize1,erSize2],'nodePool':nodePool,\
                                 'ers': [bitArrayERs1,bitArrayERs2]} 
              
            # print("erDict: ",erDict)
             
            startComps = datetime.datetime.now()
            print("")
            print("startComparisons at: ",startComps)
            print("  ersizes: ",erSize1,erSize2)
            print("  nodePool: ",nodePool)
            print("  quantity: ",quantity)
        
            # normal list compare
            counts,durations,overallDuration = compareListERs(baseERs1,baseERs2)
            meanDuration =mean(durations)/1000000
            averageDuration = overallDuration/quantity/1000000
            stdevDuration = stdev(durations)/1000000
            print("")
            print("list ER dot-product")
            # print("counts/durations(ns): ",counts,durations)
            print("  overallDuration(ms)/quantity: ",overallDuration/1000000, quantity)
            print("  meanDuration(ms): ",meanDuration)
            print("  stdevDuration(ms): ",stdevDuration)
            print("  averageDuration(ms): ",averageDuration)
            dictItem['listResults'] = [meanDuration,stdevDuration,averageDuration]
            
            
            # set compare
            counts,durations,overallDuration = compareSetERs(setERs1,setERs2)
            meanDuration =mean(durations)/1000000
            averageDuration = overallDuration/quantity/1000000
            stdevDuration = stdev(durations)/1000000
            print("")
            print("Set ER dot-product")
            # print("counts/durations(ns): ",counts,durations)
            print("  overallDuration(ms)/quantity: ",overallDuration/1000000, quantity)
            print("  meanDuration(ms): ",meanDuration)
            print("  stdevDuration(ms): ",stdevDuration)
            print("  averageDuration(ms): ",averageDuration)   
            dictItem['setResults'] = [meanDuration,stdevDuration,averageDuration]
            
            
            # partially sorted list compare - er1 non-sorted, er2 sorted; binary search
            counts,durations,overallDuration = comparePartiallySortedList(baseERs1,sortedERs2)
            meanDuration =mean(durations)/1000000
            averageDuration = overallDuration/quantity/1000000
            stdevDuration = stdev(durations)/1000000
            print("")
            print("Partially Sorted ER dot-product")
            # print("counts/durations(ns): ",counts,durations)
            print("  overallDuration(ms)/quantity: ",overallDuration/1000000, quantity)
            print("  meanDuration(ms): ",meanDuration)
            print("  stdevDuration(ms): ",stdevDuration)
            print("  averageDuration(ms): ",averageDuration)      
            dictItem['partiallySortedListResults'] = [meanDuration,stdevDuration,averageDuration] 
            
            
            # sorted list compare - er1 sorted, er2 sorted; modified binary search
            counts,durations,overallDuration = compareSortedList(sortedERs1,sortedERs2)
            meanDuration =mean(durations)/1000000
            averageDuration = overallDuration/quantity/1000000
            stdevDuration = stdev(durations)/1000000
            print("")
            print("Sorted ER dot-product")
            # print("counts/durations(ns): ",counts,durations)
            print("  overallDuration(ms)/quantity: ",overallDuration/1000000, quantity)
            print("  meanDuration(ms): ",meanDuration)
            print("  stdevDuration(ms): ",stdevDuration)
            print("  averageDuration(ms): ",averageDuration)  
            dictItem['sortedListResults'] = [meanDuration,stdevDuration,averageDuration]    
            
            # bitarray compare  -- these are very very quick--so if less than 1,000, repeat loops
            totalOverallDuration = 0
            iterations = 0
            allCounts = []
            allDurations = []
            while iterations < 100000:
                iterations += quantity
                counts,durations,overallDuration = compareBitArrayERs(bitArrayERs1,bitArrayERs2)
                allCounts.extend(counts)
                allDurations.extend(durations)
                totalOverallDuration += overallDuration
                
            meanDuration = mean(allDurations)/1000000
            stdevDuration = stdev(allDurations)/1000000
            averageDuration = totalOverallDuration/iterations/1000000

            print("")
            print("Bitarray ER dot-product")
            # print("counts/durations(ns): ",counts,durations)
            print("  overallDuration(ms)/quantity: ",totalOverallDuration/1000000, iterations)
            print("  meanDuration(ms): ",meanDuration)
            print("  stdevDuration(ms): ",stdevDuration)
            print("  averageDuration(ms): ",averageDuration)   
            dictItem['bitArrayResults'] = [meanDuration,stdevDuration,averageDuration]
            
            
            
            print("")
            print("startComps: ",startComps)
            finish = datetime.datetime.now()
            print("finish: ",finish)
            duration = finish - startComps
            print("duration: ",duration)
    
            resultsList.append(dictItem)
    
            print("resultsList: ",resultsList)
            
            
            # write results to file
            print("")
            print("Writing timingResults pickle file: ",timingResults_fileName)
                   
            afile = open(timingResults_fileName, 'wb')
            pickle.dump(resultsList, afile)
            
            afile.close()
            print("")
            print("Finished writing a timingResults pickle file: ",timingResults_fileName) 
            print("")
            print("")
    
    print("done")
    print("")
    return
    
######################################

if __name__ == "__main__":
    main()