#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 19:04:09 2017

@author: Hugo Jové
"""

import numpy as np
import pandas as pd
import plotly as ply
import collections

class Categorical:
    
    def __init__(self,fileCSV=None):
        
        self.__name = 'Categorical'
        if fileCSV is None:
            self.pathBank = 'Data/DataSet/bank/bank.csv'
            self.pathBankFull = 'Data/DataSet/bank/bank-full.csv'
            self.pathBankAdditional = 'Data/DataSet/bank-additional/bank-additional.csv'
            self.pathBankAdditionalFull = 'Data/DataSet/bank-additional/bank-additional-full.csv'
            self.fileCSV = pd.read_csv(filepath_or_buffer= self.pathBankFull, delimiter = ';', header=0, index_col=0)
        else:
            self.fileCSV = fileCSV
        self.__categorical_features_table = []
        self.__categoricals = self.fileCSV.select_dtypes(exclude=[np.number])
        self.pathFileTableCategorical = './Data/Results/group7-Categorical.csv'
        self.pathFileResultsCategorical = './Data/Results/group7-DQR-Categorical.csv'
        
    def get_csv_file(self):
        return self.fileCSV
    
    def get_categoricals(self):
        return self.__categoricals
     
    def get_categorical_features_table(self):
        return self.__categorical_features_table
        
    def write_results(self):
        pd.DataFrame(self.__categoricals).to_csv(path_or_buf=self.pathFileTableCategorical)
        print("Results writed in :" + self.pathFileTableCategorical)
        pd.DataFrame(self.__categorical_features_table).to_csv(path_or_buf=self.pathFileResultsCategorical)
        print("Results writed in :" + self.pathFileResultsCategorical)
       

    def draw_graphics(self):
        
        print("Drawing graphics in progress...")
        csvFile = self.get_csv_file()
        
        for feature in csvFile.columns:
            
            dataFeature = csvFile[feature]
         
            if np.unique(dataFeature).size >= 10:
                        
                ply.offline.plot({
                    "data": [
                        ply.graph_objs.Histogram(
                            x=csvFile[feature]
                        )
                    ],
                    "layout": ply.graph_objs.Layout(
                        title="Histogram of feature \"" + feature + "\" - cardinality >=10"
                    )
                }, filename="./Data/HTML/Categorical/%s.html" % feature)
            else:
                ply.offline.plot({
                    "data": [
                        ply.graph_objs.Bar(
                            x=csvFile[feature].value_counts().keys(),
                            y=csvFile[feature].value_counts().values
                        )
                    ],
                    "layout": ply.graph_objs.Layout(
                        title="Bar plot for feature \"" + feature + "\" - cardinality <10"
                    )
                }, filename="./Data/HTML/Categorical/%s.html" % feature)
        print("Drawing graphics done")
    
    def save_data(self):
 
        print("Saving data in progress...")
        
        categorical_columns = self.get_categoricals()                    

        for cat_name in categorical_columns:
            
            # We get all the column of the category in the CSV file
            dataFeature = self.fileCSV[cat_name]
            
            # We make a dictionnary to be granted to put string keys
            feature =  collections.OrderedDict()
            
            # Put in the table feature the name of the feature
            feature['nameFeature'] = cat_name
            # Put in the table feature the total count of lines
            feature['countTotal'] = dataFeature.size
                   
            feature['% Miss'] = dataFeature.isnull().sum()/ dataFeature.size * 100
            feature['cardTotal'] = np.unique(dataFeature).size

            feature['First Mode'] = dataFeature.value_counts().keys()[0]
            feature['First Mode Freq'] = dataFeature.value_counts()[0]
            feature['First Mode %'] = round(dataFeature.value_counts()[0] / dataFeature.size * 100,2)
            
            feature['Second Mode'] = dataFeature.value_counts().keys()[1]
            feature['Second Mode Freq'] = dataFeature.value_counts()[1]
            feature['Second Mode %'] = round(dataFeature.value_counts()[1] / dataFeature.size * 100,2)
            
            self.__categorical_features_table.append(feature)   
            
        print("Saving data finished")

    def treatment(self):
        self.save_data();
        self.write_results()
        self.draw_graphics()
 
Categorical().treatment()
