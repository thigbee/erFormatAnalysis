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


def load_sizingResults():
    fileDialogUi = App()       
    sizingResults_fileName = fileDialogUi.openFileNamesDialog("Sizing ER Compare Results Pickle","srefPkl")
    if sizingResults_fileName == '':
        return
    return sizingResults_fileName 
    
         
def read_sizingResults(sizingResults_fileName):
    file_w_ext = os.path.basename(sizingResults_fileName)
    file_ext = os.path.splitext(file_w_ext)  
    if file_ext[1] != '.srefPkl':
        print("Invalid Sizing Results pickle file")
        return 
    else:
        objFile = open(sizingResults_fileName, 'rb')
        sizeStats= pickle.load(objFile)
        objFile.close()
    return sizeStats


def main():

    # get trec Pickle file names to import 
    fileNames = load_sizingResults()
    if fileNames == []:
        print("  no files selected.")
        return
             
    print("  ",len(fileNames)," selected files: ",fileNames)
    
    sizeStatsList = []
    # read each file and combine the list of dictionaries from each
    for i in range(0,len(fileNames)):
        sizeStats = read_sizingResults(fileNames[i])
        sizeStatsList.extend(sizeStats)
    
    lenSizeStatsList = len(sizeStatsList)
    print("length of sizeStatsList: ",lenSizeStatsList)
    print("first size stats: ",sizeStatsList[0])
    print("last size stats: ",sizeStatsList[lenSizeStatsList-1])

    # Create a new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook('data/erSizingData.xlsx')
    worksheet = workbook.add_worksheet()
    
    # Widen the first column to make the text clearer.
    # worksheet.set_column('A:A', 20)
    
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})


    # write column headings
    columnHeaders = ['testNum','erSize1','nodePool','test quantity','log2erSize1','log2NodePool',\
                     'unordered lists','sorted lists','sets','bitarray']
    exponent = [2**x for x in range(21)] 
    
    for i in range(0,len(columnHeaders)):
        worksheet.write(0,i,columnHeaders[i],bold)
    
    # add data--one row per list item
    for i in range(0,lenSizeStatsList):
        item = sizeStatsList[i]
        # print("item: ",item)
        testNum = i
        worksheet.write(i+1,0,testNum)
        worksheet.write(i+1,1,item['erSize1:'])
        worksheet.write(i+1,2,item['nodePool'])
        worksheet.write(i+1,3,item['quantity'])
        worksheet.write(i+1,4,exponent.index(item['erSize1:']))
        worksheet.write(i+1,5,exponent.index(item['nodePool'])) 
        if 'uoListERs' in item:
            worksheet.write(i+1,6,item['uoListERs']['memorySpace'])
        if 'oListERs' in item:    
            worksheet.write(i+1,7,item['oListERs']['memorySpace'])
        if 'setERs' in item:
            worksheet.write(i+1,8,item['setERs']['memorySpace'])
        if 'bArrayERs' in item:
            worksheet.write(i+1,9,item['bArrayERs']['memorySpace'])
        
    workbook.close()


    # Create a second Excel file and add a worksheet--with a preformatted table.
    workbook = xlsxwriter.Workbook('data/erSizingData-table.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    
    # write column headings
    methods = ['unordered Lists','ordered Lists','Sets','Bit arrays']
    baseRow = 3
    baseCol = 1
    worksheet.write(1,1,"ER Compare Sizing Requirements (bytes)",bold)
    groupSpace = 10
    rowSpace = 12
    colConvert = [6,10,14,16,20]
    rowConvert = [6,8,10,12,14]
    quantityConvert = [4,64,1024]
    
    # print method and nodePool header lines
    for k in range(0,3):
        for i in range(0,len(methods)):
            worksheet.write(baseRow+(k*rowSpace)-1,baseCol+(i*groupSpace)+3,methods[i].upper(),bold)
            worksheet.write(baseRow+(k*rowSpace)+0,baseCol+(i*groupSpace)+1,'Quantity:',bold)
            worksheet.write(baseRow+(k*rowSpace)+0,baseCol+(i*groupSpace)+2,quantityConvert[k])
            worksheet.write(baseRow+(k*rowSpace)+1,baseCol+(i*groupSpace)+1,'NodePool-->',bold)
            worksheet.write(baseRow+(k*rowSpace)+2,baseCol+(i*groupSpace)+1,'ER Size',bold)
            for j in range(0,len(colConvert)):      # column headers
                index = colConvert[j]
                worksheet.write(baseRow+(k*rowSpace)+1,baseCol+(i*groupSpace)+3+j,str(2**index),bold)   # nodePool
                worksheet.write(baseRow+(k*rowSpace)+2,baseCol+(i*groupSpace)+3+j,"2**"+str(index),bold)  # log10 nodePool
            for j in range(0,len(rowConvert)):     # row headers
                index = rowConvert[j]
                worksheet.write(baseRow+(k*rowSpace)+j+3,baseCol+(i*groupSpace)+1,str(2**index),bold)       # erSize
                worksheet.write(baseRow+(k*rowSpace)+j+3,baseCol+(i*groupSpace)+2,"2**"+str(index),bold)      # log10 erSize            

    # fill in table entries
    for i in range(0,lenSizeStatsList):
        item = sizeStatsList[i]
        rowOffset = rowConvert.index(exponent.index(item['erSize1:'])) + 3
        colOffset = colConvert.index(exponent.index(item['nodePool'])) + 3
        multiRowOffset = quantityConvert.index(item['quantity']) * (groupSpace+2)
        if True:
            print("")
            print("row/colOffset: ",rowOffset,colOffset)
            print("row/col: ",baseRow + rowOffset, baseCol + colOffset)
            print("item: ",item)
            print("")
            
        if 'uoListERs' in item:
            worksheet.write(baseRow+rowOffset+multiRowOffset,baseCol+colOffset,item['uoListERs']['memorySpace'])
        if 'oListERs' in item:    
            worksheet.write(baseRow+rowOffset+multiRowOffset,baseCol+groupSpace+colOffset,item['oListERs']['memorySpace'])
        if 'setERs' in item:
            worksheet.write(baseRow+rowOffset+multiRowOffset,baseCol+(2*groupSpace)+colOffset,item['setERs']['memorySpace'])
        if 'bArrayERs' in item:
            worksheet.write(baseRow+rowOffset+multiRowOffset,baseCol+(3*groupSpace)+colOffset,item['bArrayERs']['memorySpace'])            
            
    workbook.close()


    return

    
    # create 'data' list for Plotly pivottable (data.py file)
    data = []
    data.append(columnHeaders)
    for i in range(0,lenSizeStatsList):
        item = sizeStatsList[i]
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
    for i in range(0,lenSizeStatsList):
        item = sizeStatsList[i]
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