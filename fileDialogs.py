# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 21:23:44 2017

@author: talan_000
"""

import sys
from PyQt5.QtWidgets import QFileDialog, QWidget
 
class App(QWidget):
 
    def __init__(self):
        super().__init__()
 
    def openFileNameDialog(self,fileTypeText,fileExt,filePath="data"): 
        fileSpecParm1 = fileTypeText + " File"
        fileSpecParm2 = fileSpecParm1 + " (*." + fileExt + ")"
        fileName, _ = QFileDialog.getOpenFileName(self,"Open "+fileSpecParm1, \
                                                  filePath,fileSpecParm2)
        return fileName
    
    def openFileNamesDialog(self,fileTypeText,fileExt,filePath='data'):
        fileSpecParm1 = fileTypeText + " File"
        fileSpecParm2 = fileSpecParm1 + " (*." + fileExt + ")"        
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Open "+fileSpecParm1, \
                                                    filePath,fileSpecParm2)
        return fileNames    
     
 
    # def openFileNamesDialog(self):    
    #     files, _ = QFileDialog.getOpenFileNames(self,fileTypeText, \
    #             "","All Files (*);;Python Files (*.py)")
    #     return files
 
    def saveFileDialog(self,fileTypeText,fileExt,filePath="data"):   
        fileSpecParameter = fileTypeText + " File (*." + fileExt + ")"
        fileName, _ = QFileDialog.getSaveFileName(self,fileTypeText, \
                      filePath,fileSpecParameter)
        return fileName