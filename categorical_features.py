#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 19:04:09 2017

@author: hugo
"""

import numpy as np
import pandas as pd
import plotly as ply
import collections

class Categorical:
    def __init__(self,fileCSV=None):
        
        self.name = 'Categorical'
        if fileCSV is None:
            self.pathBank = './Data/DataSet/bank/bank.csv'
            self.pathBankFull = './Data/DataSet/bank/bank-full.csv'
            self.fileCSV = pd.read_csv(filepath_or_buffer=self.pathBankFull, delimiter = ';', header=0, index_col=0)
        else:
            self.fileCSV = fileCSV
        self.categorical_features_table = []
        self.categoricals = self.fileCSV.select_dtypes(exclude=[np.number])
        self.pathFileTableCategorical = './Data/Results/group7-DQR-Categorical.csv'
        self.pathFileResultsCategorical = './Data/Results/group7-DQR-Categorical-Results.csv'
        
    def get_csv_file(self):
        return self.fileCSV
    
    def get_categoricals(self):
        return self.categoricals
      
    def write_results(self):
        pd.DataFrame(self.categoricals).to_csv(path_or_buf=self.pathFileTableCategorical)
        print("Results writed in :" + self.pathFileTableCategorical)
        pd.DataFrame(self.categorical_features_table).to_csv(path_or_buf=self.pathFileResultsCategorical)
        print("Results writed in :" + self.pathFileResultsCategorical)
       
    def get_categorical_features_table(self):
        return self.categorical_features_table
        
    def draw_graphics(self):
        
        tableCategoricals = self.get_categoricals()
#        for feature,value in tableCategoricals.items():                
#            print(value)
      
    def launch_test(self):
        
        self.treatment();
        self.write_results()
        self.draw_graphics()
        
    
    def treatment(self):
 
        print("Treatment "+ self.name +" in progress...")
        
        categorical_columns = self.fileCSV.select_dtypes(exclude=[np.number])                     

        for categorie_name in categorical_columns:
            
            dataFeature = self.fileCSV[categorie_name]
            
            feature =  collections.OrderedDict()
            feature['nameFeature'] = categorie_name
            feature['countTotal'] = dataFeature.size
            feature['% Miss'] = dataFeature.isnull().sum()/ dataFeature.size * 100
            feature['cardTotal'] = np.unique(dataFeature).size

            feature['First Mode'] = dataFeature.value_counts().keys()[0]
            feature['First Mode Freq'] = dataFeature.value_counts()[0]
            feature['First Mode %'] = round(dataFeature.value_counts()[0] / dataFeature.size * 100,2)
            
            feature['Second Mode'] = dataFeature.value_counts().keys()[1]
            feature['Second Mode Freq'] = dataFeature.value_counts()[1]
            feature['Second Mode %'] = round(dataFeature.value_counts()[1] / dataFeature.size * 100,2)
            
            self.categorical_features_table.append(feature)   
            
        print("Treatment "+ self.name +" finished")
        
Categorical().launch_test()
