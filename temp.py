# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 16:25:08 2019

@author: kryan
"""
import tensorflow as tf
import pandas as pd
import numpy as np
import SalaryPredictor as SP
import DataManipulation as DM
import operator

data = DM.offData.reset_index()
predictions = {'Age': [],
              'AB':[],
              'H': [],
              'R': [],
              'RBI': [],
              'HR': [],
              'SB': []
              }


for index, row in data.iterrows():    
    predictions['Age'].append(row['Age'])
    predictions['AB'].append(row['AB'])
    predictions['H'].append(row['H'])
    predictions['R'].append(row['R'])
    predictions['RBI'].append(row['RBI'])
    predictions['HR'].append(row['HR'])
    predictions['SB'].append(row['SB'])
    
    

expected = [0] * (len(predictions['Age']))

booyah = SP.modelPredict(predictions, expected)
newDict = dict()
x = 0
for item in booyah:
    string = data.loc[x]['Player']
    print(string)
    newDict[string] = int(item)
    x = x + 1
    
sorted_d = sorted(newDict.items(), key=operator.itemgetter(1))