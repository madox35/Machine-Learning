#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 23:07:09 2017

@author: morgan
"""

import handle_files as hf
import continuous_features as cont

def main():
    
    path = './Data/DataSet/bank/bank.csv'
    file = hf.Handle_files.get_file(path)
    c = cont.Continuous(file)
    
    continuous = c.get_continuous()
    
    #print(type(continuous))
    #print(continuous)
    
    for item in continuous.items():
        print(item)
    
main()