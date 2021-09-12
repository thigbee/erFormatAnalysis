# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 20:24:57 2021

Program to read multiple er Comparison timingResults pickles and create a plot

"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os, sys, pickle
import matplotlib.ticker
from fileDialogs import App
from PyQt5.QtWidgets import QApplication
import xlsxwriter
import math


# def convVal(value):
#     if value > 0.1 and value < 1.0:
#         return round(value,1)
#     elif value <= 0.1:
#         return round(value,0)
#     else:
#        return int(value)


def load_timingResults():
    fileDialogUi = App()       
    timingResults_fileName = fileDialogUi.openFileNamesDialog("Timing ER Compare Results Pickle","trecPkl")
    if timingResults_fileName == '':
        return
    return timingResults_fileName 
    
         
def read_timingResults(timingResults_fileName):
    file_w_ext = os.path.basename(timingResults_fileName)
    file_ext = os.path.splitext(file_w_ext)  
    if file_ext[1] != '.trecPkl':
        print("Invalid Timing Results pickle file")
        return 
    else:
        objFile = open(timingResults_fileName, 'rb')
        timeStats = pickle.load(objFile)
        objFile.close()
    return timeStats


def main():

    # get trec Pickle file names to import 
    fileNames = load_timingResults()
    if fileNames == []:
        print("  no files selected.")
        return
             
    print("  ",len(fileNames)," selected files: ",fileNames)
    
    timeStatsList = []
    # read each file and combine the list of dictionaries from each
    for i in range(0,len(fileNames)):
        timeStats = read_timingResults(fileNames[i])
        timeStatsList.extend(timeStats)
    
    lenTimeStatsList = len(timeStatsList)
    print("length of timeStatsList: ",lenTimeStatsList)
    print("first time stats: ",timeStatsList[0])
    print("last time stats: ",timeStatsList[lenTimeStatsList-1])

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook('data/erTimingData.xlsx')
    worksheet = workbook.add_worksheet()
    
    # Widen the first column to make the text clearer.
    # worksheet.set_column('A:A', 20)
    
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})
    
    # write column headings
    columnHeaders = ['testNum','erSize1','erSize2','nodePool','test quantity','log2erSize1','log2erSize2','log2NodePool',\
                     'setizing','listizing','unsorted lists','partially sorted lists','sorted lists','sets','bitarry']
    exponent = [2**x for x in range(21)] 
    
    for i in range(0,len(columnHeaders)):
        worksheet.write(0,i,columnHeaders[i],bold)
    
    # add data--one row per list item
    for i in range(0,lenTimeStatsList):
        item = timeStatsList[i]
        # print("item: ",item)
        testNum = i
        worksheet.write(i+1,0,testNum)
        worksheet.write(i+1,1,item['erSize1:'])
        worksheet.write(i+1,2,item['erSize2'])
        worksheet.write(i+1,3,item['nodePool'])
        worksheet.write(i+1,4,item['quantity'])
        worksheet.write(i+1,5,exponent.index(item['erSize1:']))
        worksheet.write(i+1,6,exponent.index(item['erSize2']))
        worksheet.write(i+1,7,exponent.index(item['nodePool']))        
        worksheet.write(i+1,8,item['setizingResults'][0])
        worksheet.write(i+1,9,item['listizingResults'][0])
        worksheet.write(i+1,10,item['partiallySortedListResults'][2])
        worksheet.write(i+1,11,item['sortedListResults'][2])
        worksheet.write(i+1,12,item['listResults'][2])
        worksheet.write(i+1,13,item['setResults'][2])
        worksheet.write(i+1,14,item['bitArrayResults'][2])
    workbook.close()
    
    # create 'data' list for Plotly pivottable (data.py file)
    data = []
    data.append(columnHeaders)
    for i in range(0,lenTimeStatsList):
        item = timeStatsList[i]
        newItem = [i,item['erSize1:'],item['erSize2'],item['nodePool'],item['quantity'],\
                    exponent.index(item['erSize1:']),exponent.index(item['erSize2']),exponent.index(item['nodePool']),\
                    item['setizingResults'][0],item['listizingResults'][0],item['listResults'][0],\
                    item['partiallySortedListResults'][2],item['sortedListResults'][2],\
                    item['listResults'][2],item['setResults'][2],item['bitArrayResults'][2]]
        data.append(newItem)

    # write data list to file        
    textfile = open("data/erTimingData.py", "w")
    textfile.write("data = [\n")
    for i in range(0,len(data)):
        if i != len(data)-1:
            textfile.write(str(data[i])+',\n')
        else:
            textfile.write(str(data[i])+'\n') 
    textfile.write("]")
    textfile.close()
 
    # create second 'data' list for Plotly pivottable (data.py file) -- one timing value per line
    columnHeaders2 = ['log2erSize','log2NodePool','method','log10 execution time']
    measurements = ['setizingResults','listizingResults','listResults','partiallySortedListResults',\
                    'sortedListResults','setResults','bitArrayResults']
    offset = [0,0,2,2,2,2,2]
    data = []
    data.append(columnHeaders2)
    for i in range(0,lenTimeStatsList):
        item = timeStatsList[i]
        for j in range(0,len(measurements)):
            measuredValue = item[measurements[j]][offset[j]]
            if measuredValue == 0:
                logMV = None
            else:
                logMV = math.log10(measuredValue)
            newItem = [exponent.index(item['erSize1:']),exponent.index(item['nodePool']),\
                        measurements[j],logMV]
            data.append(newItem)

    # write data list to file        
    textfile = open("data/erTimingData2.py", "w")
    textfile.write("data = [\n")
    for i in range(0,len(data)):
        if i != len(data)-1:
            textfile.write(str(data[i])+',\n')
        else:
            textfile.write(str(data[i])+'\n') 
    textfile.write("]")
    textfile.close()
    
    return

   

######################################

if __name__ == "__main__":

    app = QApplication(sys.argv)
    main()
    
    sys.exit()