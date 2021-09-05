occd Doc# -*- coding: utf-8 -*-
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
# sys.path.append('c:/users/talan/documents/krune_git/gandemo')
# from extAssocMemV13 import AssocMem, AssocMemItem
from fileDialogs import App
from operator import itemgetting,attrgetter


def buildBasicERs(erSize,nodePool):
    baseER1 = random.sample(range(0,nodePool),erSize)
    baseER2 = random.sample(range(0,nodePool),erSize)
    return baseER1,baseER2

def buildSetizedERs(erList1,erList2):
    setER1 = set(erList1)
    setER2 = set(erList2)
    return setER1,seter2

def buildSortedListERs(baseER1,baseER2):
    sortedER1 = sorted(baseER1)
    sortedER2 = sorted(baseER2)
    return sortedER1,sortedER2

def binaryERs(baseER1,baseER2,nodePool):
    numWords = nodePool/64
    



def main():
    erSizesList = [4,16,64,256,1024,4096,16384]
    nodePoolSizesList = [256,1024,4096,16384,65536,262144]
    
    erDict = {}
        
    # base ERs
    baseER1, baseER2 = buildBasicERs()
    erDict{'baseERs'} = {'description':'unordered list of nodes',\
                         'erSize':erSize,'nodePool':nodePool,\
                         'er1': baseER1,'er2':baseER2}
    
    # ordered base ERs
    sortedER1, sortedER2 = buildSortedListERs(baseER1,baseER2)
    erDict['sortedBaseERs'] = {'description':'ordered list of nodes',\
                         'erSize':erSize,'nodePool':nodePool,\
                         'er1': sortedBaseER1,'er2':sortedBaseR2}
    
    # setized base ERs
    setER1, setER2 = buildSetizedERs(baseER1,baseER2)
    erDict{'setBaseERs'} = {'description':'unordered set of nodes',\
                         'erSize':erSize,'nodePool':nodePool,\
                         'er1': setBaseER1,'er2':setBaseER2}    
    
    # setized sorted base ERs
    setSortedBaseER1, setSortedBaseER2 = buildSortedListERs(baseER1,baseER2)
    erDict{'bsetSortedBaseERs'} = {'description':'ordered set of nodes',\
                         'erSize':erSize,'nodePool':nodePool,\
                         'er1': setSortedBaseER1,'er2':setSortedBaseER2}      
    
   # binary ERs
    binaryER1, binaryER2 = buildBinaryERs(baseER1,baseER2,nodePool)
    erDict{'binaryERs'} = {'description':'binaryERs',\
                         'erSize':erSize,'nodePool':nodePool,\
                         'er1': binaryER1,'er2':binaryER2}
        
    
        
