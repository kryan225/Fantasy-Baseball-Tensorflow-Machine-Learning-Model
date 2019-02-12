# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 16:25:08 2019

This file's purpose is to be able to run a large prediction job on a trained NN model

This is for a personal project where I develop a fantasy baseball draft toolkit for my custom league. 
The winner of my league gets $600+ and as of developing this, my team has finished 7th place four years in a row.
The cutoff of winning any money back is 6th place so my co-owner/brother and I are a little annoyed. I hope that this
toolkit will provide us with an advantage for evaluating players and forming a draft strategy. Even though you don't necessarily 
win your league on draft day, you can have a massive head start and it is possible to lose the league at the draft. 

any questions or comments please email me at: kryan225.gomets@gmail.com



@author: kryan
"""
import tensorflow as tf
import pandas as pd
import numpy as np
import SalaryPredictor as SP
import DataManipulation as DM
import operator

#data = DM.offData.reset_index()
def runBatchPredict(file):
    '''
    This function will take the name of a csv and run a prediction job on it, calling a trained NN. 
    It will return a dictionary with each player's name corresponding to their salary.
    
    Maybe I can have it display the stats too
    '''
    data = pd.read_csv(file)
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
    return sorted_d