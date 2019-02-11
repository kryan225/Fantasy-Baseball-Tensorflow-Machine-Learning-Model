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

#data = DM.offData.reset_index()
data = pd.read_csv('projections.csv')
predictions = {
              'AB':[],
              'H': [],
              'R': [],
              'RBI': [],
              'HR': [],
              'SB': []
              }


for index, row in data.iterrows():    
    #predictions['Age'].append(row['Age'])
    predictions['AB'].append(row['AB'])
    predictions['H'].append(row['H'])
    predictions['R'].append(row['R'])
    predictions['RBI'].append(row['RBI'])
    predictions['HR'].append(row['HR'])
    predictions['SB'].append(row['SB'])
    
    

expected = [0] * (len(predictions['AB']))

booyah = SP.modelPredict(predictions, expected)

'''
Current problem is there are 866 unique players, but we have 1921 predictions. When we build the dict that holds every player 
to their prediction, they end up getting paired with their oldest (lowest) salary prediction. 

I think we ready to try with the baseballHQ 2019 predictions now

NORMALIZE THE DATA YOU STUPID MORON 
'''

newDict = dict()
x = 0
for item in booyah[:]:
    string = data.loc[x]['Player']
    
    if(string in newDict):
        if(newDict[string] < item):
            newDict[string] = int(item)
    else:
        newDict[string] = int(item)
    x = x + 1
    
sorted_d = sorted(newDict.items(), key=operator.itemgetter(1), reverse=True)