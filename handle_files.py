#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 19:38:25 2017

@author: morgan
"""

import pandas as pd

class Handle_files:
    @staticmethod
    def get_file(path=None):
        try:
            file = pd.read_csv(filepath_or_buffer=path)
            return file
        except Exception as e:
            print(e)
            
    
    @staticmethod
    def write_file(file,path=None):
        pd.DataFrame(file).to_csv(path_or_buf=path)
