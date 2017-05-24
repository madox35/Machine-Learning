#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 19:04:09 2017

@author: morgan
"""

import numpy as np
import pandas as pd
import plotly as ply

class Continuous:
    def __init__(self,fileCSV=None):            
        print("Reading file")
        if fileCSV is None:
            self.pathBank   = './Data/DataSet/bank/bank-full.csv'
            self.pathFile   = './Data/DataSet/Data.csv'
            self.fileCSV    = pd.read_csv(filepath_or_buffer=self.pathBank,delimiter = ';', header=0, index_col=0)
        else:
            self.fileCSV = fileCSV
            
        self.continuous = self.fileCSV.select_dtypes(include=[np.number])
        self.pathFileResult = './Data/Results/group7-DQR-Continuous.csv'
        
    def get_csv_file(self):
        return self.fileCSV
    
    def get_continuous(self):
        print("continuous : ",self.continuous)
        return self.continuous
        
    
    def write_results(self):
        pd.DataFrame(self.continuous).to_csv(path_or_buf=self.pathFileResult)
        
    def write_results_from_file(self,file,headers):
        print("Writing file")
        pd.DataFrame(file,columns=[headers]).to_csv(self.pathFileResult)
        
    def add_feature(self,feature,value):
        self.continuous[feature].append(value)
       
        
    # Step 1, treatment to get all continuous features
    def treatment(self):
        continuous_columns = self.continuous
        continuous_header = ["Features","Count","% Miss", "Card", "Min", "1st Qrt", "Mean","Median","3rd Qrt","Max", "std" ]
        continuous_features_table = []
        
        print("Beginning of treatment")
        
        for column_name in continuous_columns:
            
            # Column's name
            feature = [column_name] 
            feature.append(continuous_columns[column_name].size)
            feature.append((continuous_columns[column_name].isnull().sum()/continuous_columns[column_name].size) * 100)
            feature.append(continuous_columns[column_name].unique().size)
            feature.append(np.min(continuous_columns[column_name]))
            feature.append(np.percentile(continuous_columns[column_name],25))
            feature.append(np.mean(continuous_columns[column_name]))
            feature.append(np.percentile(continuous_columns[column_name],50))
            feature.append(np.percentile(continuous_columns[column_name],75))
            feature.append(np.max(continuous_columns[column_name]))
            feature.append(np.std(continuous_columns[column_name]))
                
            continuous_features_table.append(feature)
        
#        print(continuous_features_table)
        
        print("End of treatment")
        #self.write_results_from_file(continuous_features_table,continuous_header)
        pd.DataFrame(continuous_features_table,columns=continuous_header).to_csv(self.pathFileResult)
        self.continuous = continuous_features_table
        self.draw_graphics();
        
    def draw_graphics(self):
        #tableContinuous = self.get_continuous()
        tableDataSet    = self.get_csv_file()
        print("Drawing graphics")
        
        for feature in tableDataSet.columns:
            tableDataSet[feature] 
            if len(set(feature)) >= 10:
                ply.offline.plot({
                    "data": [
                        ply.graph_objs.Histogram(
                            x=tableDataSet[feature]
                        )
                    ],
                    "layout": ply.graph_objs.Layout(
                        title="Histogram of feature \"" + feature + "\" - cardinality >=10"
                    )
                }, filename="./Data/HTML/Continuous/%s.html" % feature)
            else:
                ply.offline.plot({
                    "data": [
                        ply.graph_objs.Bar(
                            x=tableDataSet[feature].value_counts().keys(),
                            y=tableDataSet[feature].value_counts().values
                        )
                    ],
                    "layout": ply.graph_objs.Layout(
                        title="Bar plot for feature \"" + feature + "\" - cardinality <10"
                    )
                }, filename="./Data/HTML/Continuous/%s.html" % feature)

        print("End of drawing graphics")   
        
#Continuous().treatment()