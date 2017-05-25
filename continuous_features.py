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
    def __init__(self,initBank=True,initContinuousData=True):            
        print("Reading file")
        
        # Bank file
        self.fileCSV = None
        # Extracting continuous values from bank file
        self.continuous = None
        # Continuous features
        self.continuousFeatures = None
        
        self.pathBank       = './Data/DataSet/bank/bank.csv'
        self.pathBankFull   = './Data/DataSet/bank/bank-full.csv'
        
        self.pathBankAdditional = './Data/DataSet/bank/bank-additional.csv'
        self.pathBankAdditionalFull   = './Data/DataSet/bank/bank-additional-full.csv'
        
        self.pathContinuousFile = './Data/Results/group7-Continuous.csv'
        # Path for features continuous values
        self.pathFileResult = './Data/Results/group7-DQR-Continuous.csv'
           
        if initBank is True:
            self.init_bank_file(self.pathBankFull)
            #self.fileCSV = pd.read_csv(filepath_or_buffer=self.pathBankFull,delimiter = ';', header=0, index_col=0)
            
        if initContinuousData is True:
            self.init_continuous_data()
            #self.continuous = self.fileCSV.select_dtypes(include=[np.number])
            self.write_continuous_file(self.continuous)
            
            
            
    # Reading bank file from path
    def init_bank_file(self,path):
        print("Reading bank file")
        self.fileCSV = pd.read_csv(filepath_or_buffer=path,delimiter = ';', header=0, index_col=0)
        
    # Init continuous data
    def init_continuous_data(self):
        print("Init continuous data from bank file")
        if self.fileCSV is not None:
            self.continuous = self.fileCSV.select_dtypes(include=[np.number])
        else:
            print("Continuous not initiated")
            
    # Init features continuous 
    def init_features_continuous_data(self,featuresData):
        print("Init features continuous from continuous data")
        self.continuousFeatures = featuresData                  
        
    def write_continuous_file(self,file):
        print("Writing continuous data")
        pd.DataFrame(file).to_csv(path_or_buf=self.pathContinuousFile)
        
    def write_results_from_data(self,data,headers):
        self.init_features_continuous_data(data)
        print("Writing results csv file")
        pd.DataFrame(data,columns=headers).to_csv(self.pathFileResult)
        
    def read_continuous_features(self):
        return pd.read_csv(filepath_or_buffer=self.pathFileResult,delimiter = ';', header=0, index_col=0)
    
    def get_csv_file(self):
        return self.fileCSV
    
    def get_continuous(self):
        print("continuous : ",self.continuous)
        return self.continuous
    
    def get_continuous_features(self):
        print("continuous : ",self.continuousFeatures)
        return self.continuousFeatures
        
    
    def treatment(self):
        continuous_columns = self.continuous
        continuous_header = ["Features","Count","% Miss", "Card", "Min", "1st Qrt", "Mean","Median","3rd Qrt","Max", "std" ]
        continuous_features_table = []
         #continuous_features_table = collections.OrderedDict()
        
        print("Beginning of treatment")
        
        for column_name in continuous_columns:
            
            # Column's name
            feature = [column_name] 
            
            # Get all data in csv file for each column
            data_feature = continuous_columns[column_name]

            # Get some informations to evaluate quality of some outliers            
            mini = np.min(data_feature)
            maxi = np.max(data_feature)
            first_q = np.percentile(data_feature,25)
            third_q = np.percentile(data_feature,75)
            median = np.median(data_feature)
            
            # Add number of values in column
            feature.append(data_feature.size)
            # Add missing values in rate
            feature.append((data_feature.isnull().sum()/continuous_columns[column_name].size) * 100)
            # Add number of unique data 
            feature.append(data_feature.unique().size)
            # Add the min of data
            feature.append(mini)
            # Add 1st quartil
            feature.append(first_q)
            # Add mean of data
            feature.append(np.mean(data_feature))
            # Add median
            feature.append(median)
            # Add 3rd quartil
            feature.append(third_q)
            # Add the max of data
            feature.append(maxi)
            # Add std
            feature.append(np.std(data_feature))
                
            # Add this row in continuous file
            continuous_features_table.append(feature)

        print("End of treatment")
        self.write_results_from_data(continuous_features_table,continuous_header)
        
        # Writing new CSV file
        
        pd.DataFrame(continuous_features_table,columns=continuous_header).to_csv(self.pathFileResult)
        self.continuous = continuous_features_table
        #self.draw_graphics();
        
    def draw_graphics(self):
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