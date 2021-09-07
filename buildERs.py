# -*- coding: utf-8 -*-
"""
Spyder Editor

Program to setup various ER formats to analyze performance of comparing ERs 
(dot products)

v1 - Initial cut
        erDict = dictionary of various ER formats
                'name' : <name_of_format
                'er1'  : first_ER
                'er2'  : second_ER
        formatTypes = [ list of above 'name' keys to use in the anlysis]
        
        
"""

import requests,time,random,pickle
import sys
from statistics import mean,stdev
sys.path.append('c:/users/talan/documents/krune_git/gandemo')
# from extAssocMemV13 import AssocMem, AssocMemItem
from fileDialogs import App
from operator import itemgetter,attrgetter


def buildBasicERs(erSize1,erSize2,nodePool,iterations):
    baseERs1 = []
    baseERs2 = []
    for i in range(0,iterations):
        baseERs1.append(random.sample(range(0,nodePool),erSize1))
        baseERs2.append(random.sample(range(0,nodePool),erSize2))
    return baseERs1,baseERs2

def buildSetizedERs(listERs1,listERs2):
    setERs1 = []
    setERs2 = []
    for i in range(0,len(listERs1)):
        setERs1.append(set(listERs1))
    for i in range(0,len(listERs2)):
        setERs2.append(set(listERs2))
    return setERs1,setERs2

def buildSortedListERs(baseERs1,baseERs2):
    sortedERs1 = []
    sortedERs2 = []
    for i in range(0,len(baseERs1)):
        sortedERs1.append(sorted(baseERs1))
    for i in range(0,len(baseERs2)):
        sortedERs2.append(sorted(baseERs2))
    return sortedERs1,sortedERs2

def buildBitArrayERs(baseERs1,baseERs2,nodePool):
    bitArrayERs1 = nodePool * bitArray('0')
    bitArrayERs2 = nodePool * bitArray('0')
    for item in baseERs1:
        bitArrayERs1[item] = '1'
    for item in baseERs2:
        bitArrayERs2[item] = '1'
    return bitArrayERs1,bitArrayERs2

def compareListERs(listERs1,listERs2):
    # this routine uses unsorted lists, and 'if short list item in longList'
    count = 0
    startTime = time.time_ns()
    overallStart = time.time_ns()
    for i in range(0,len(listERs1)):
        if len(listERs1[i]) < len(listERs2[i]):
            shortER = listERs1[i]
            longER = listERs2[i]
        else:
            shortER = listERs2[i]
            longER = listERs1[i]
        for item in shortER:
            if item in longER:
                count += 1
        finishTime = time.time_ns()
        duration = (finishTime - startTime).microseconds
    overallFinishTime = time.time_ns()
    overallDuration = (OverallFinishTime - OverallStartTime).microseconds 
    return count,duration,overallDuration

def compareSetERs(setERs1,setER2s):
    # this routine uses unsorted set, and 'if short set item in longSet'
    counts = []
    durations = []
    overallStart = time.time_ns()
    for i in range(0,len(setERs1)):
        startTime = time.time_ns()
        if len(setERs1[i]) < len(setERs2[i]):
            shortER = setER1[i]
            longER = setER2[i]
        else:
            shortER = setERs2[i]
            longER = setERs1[i]
        for item in shortER:
            if item in longER:
                count += 1
        finishTime = time.time_ns()
        duration.append(finishTime - startTime).microseconds
    overallFinishTime = time.time_ns()
    overallDuration = (OverallFinishTime - OverallStartTime).microseconds            
    return counts,durations,overallDuration
    
def compareBitArrayERs(bitArrayER1,bitArrayER2):
    counts = []
    durations = []
    overallStart = time.time_ns()
    for i in range(0,len(bitArrayERs1)):
        startTime = time.time_ns()
        result = bitArrayER1 & bitArrayER2
        finishTime = time.time_ns()
        counts.append(result.count())
        duration.append((finishTime - startTime).microseconds)
    overallFinishTime = time.time_ns()
    overallDuration = (OverallFinishTime - OverallStartTime).microseconds
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
            print("steps: ",steps)
            return mid, mid+1
    # If we reach here, then the element was not present
    print("steps: ",steps)
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
        
        
#########################################################################################


def main():
    
    test_binary_search()
    
    return

    erSizesList = [8,16,32,64,128,256,512,1024,2048,4096,8192,16384]
    nodePoolSizesList = [256,1024,4096,16384,65536]
    
    erDict = {}
    iterations = 100
    
    
    # base ERs
    baseERs1, baseERs2 = buildBasicERs(erSize1,erSize2,nodePool,iterations)
    erDict['baseERs'] = {'description':'unordered lists of nodes', \
                         'lengths':[erSize1,erSize2],'nodePool':nodePool, \
                         'ers':[baseERs1,baseERs2]}
    
    # setized ERs
    setERs1, setERs2 = buildSetizedERs(baseERs1,baseERs2)
    erDict['baseERs'] = {'description':'unordered sets of nodes',\
                         'lengths':[erSize1,erSize2],'nodePool':nodePool,\
                         'ers': [setERs1,setER2]}    
    
    # sorted List ERs
    sortedERs1,sortedERs2 = buildSortedListERs(baseERs1,baseERs2)
    erDict['baseERs'] = {'description':'unordered lists of nodes',\
                         'lengths':[erSize1,erSize2],'nodePool':nodePool,\
                         'ers': [sortedERs1,sortedERs2]}  
        
    # sorted setized ERs
    sortedSetERs1, sortedSetERs2 = buildSetizedERs(baseERs1,baseERs2)
    erDict['baseERs'] = {'description':'ordered sets of nodes',\
                         'lengths':[erSize1,erSize2],'nodePool':nodePool,\
                         'ers': [baseER1,baseER2]}    
 
    # binary array ERs
    bitArrayERs1, bitArrayERs2 = buildBinaryERs(baseERs1,baseERs2)
    erDict['baseERs'] = {'description':'ordered sets of nodes',\
                         'lengths':[erSize1,erSize2],'nodePool':nodePool,\
                         'ers': [bitArrayER1,bitArrayER2]} 
        
        
######################################

if __name__ == "__main__":
    main()