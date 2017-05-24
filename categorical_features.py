#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 19:04:09 2017

@author: hugo
"""

import numpy
import pandas as pd
import plotly as ply

class Categorical:
    def __init__(self,fileCSV=None):
        if fileCSV is None:
            self.pathBank   = './Data/DataSet/bank/bank.csv'
            self.pathFile   = './Data/DataSet/Data.csv'
            self.fileCSV    = pd.read_csv(filepath_or_buffer=self.pathBank,delimiter = ';', header=0, index_col=0)
            del self.fileCSV["age"]
        else:
            self.fileCSV = fileCSV
            
        self.categoricals = self.fileCSV.select_dtypes(exclude=[numpy.number])
        self.pathFileResult = './Data/Results/group7-DQR-Categorical.csv'
        
    def get_csv_file(self):
        return self.fileCSV
    
    def get_categoricals(self):
        return self.categoricals
      
    def write_results(self):
        pd.DataFrame(self.categoricals).to_csv(path_or_buf=self.pathFileResult)
    
    def add_feature(self,feature,value):
        self.categoricals[feature].append(value)
        
    def draw_graphics(self):
        
        tableCategoricals = self.get_categoricals()
#        for feature,value in tableCategoricals.items():                
#            print(value)
      
    def launch_test(self):
        
        self.write_results();
        
        
Categorical().launch_test()
