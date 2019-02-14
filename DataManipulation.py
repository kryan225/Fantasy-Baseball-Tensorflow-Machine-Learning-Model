# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 15:56:59 2019

This file's purpose is to load baseball stats from csv files and produce train/test splits
that can be fed into a tensorflow nueral net.

This is for a personal project where I develop a fantasy baseball draft toolkit for my custom league. 
The winner of my league gets $600+ and as of developing this, my team has finished 7th place four years in a row.
The cutoff of winning any money back is 6th place so my co-owner/brother and I are a little annoyed. I hope that this
toolkit will provide us with an advantage for evaluating players and forming a draft strategy. Even though you don't necessarily 
win your league on draft day, you can have a massive head start and it is possible to lose the league at the draft. 

any questions or comments please email me at: kryan225.gomets@gmail.com

@author: kryan
"""


import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split
import tensorflow as tf
import matplotlib

##import 4 csv files with historical data from 2018-2015
#data16a = pd.read_csv("2016_A_B.csv")
#data16n = pd.read_csv("2016_N_B.csv")
#data17a = pd.read_csv("2017_A_B.csv")
#data17n = pd.read_csv("2017_N_B.csv")
#data18a = pd.read_csv("2018_A_B.csv")
#data18n = pd.read_csv("2018_N_B.csv")

##combine above dataframes into one dataframe
allData = pd.read_csv("combinedCSV - edited.csv")#pd.concat([data16a,data16n,data17a, data17n, data18a, data18n])


def clean(df):
    '''Cleans a dataframe from all players with not enough at bats, or if their value is too low'''
    df = df[df.AB > 170]
    df = df[df['R$'] >= 0]
    
    return df

def getOstats(df):
    """Takes a raw dataframe exported from BaseballHQ and produces a condenced dataframe with specific
        Offesensive stats"""

    condence = pd.DataFrame()
    condence = df[['Player', 'Age','AB','H','R','RBI','HR','SB','R$']]
    condence = condence.reset_index()

    return condence.sort_values(by=['R$'], ascending=False)
    


def norm(df):
    normalizedDF = pd.DataFrame()
    for colName in df.columns:
        newCol = []
        if colName == 'Player':
            normalizedDF[colName] = df[colName]
        elif colName == 'R$':
            normalizedDF[colName] = df[colName]
        else:   
            mx = max(df[colName])
            mn = min(df[colName])
            print(colName, " - max: ", mx , ", min: " , mn)
            for i in df[colName]:
                newCol.append( (i-mn)/(mx-mn) )
            normalizedDF[colName] = newCol
            
    return normalizedDF
        
##define a dataframe that has condenced, normalized offensive categories   
offData = getOstats(allData)
normData = norm(offData)

def offLoad(df = clean(offData)):
    """Takes a dataframe and prepares it to be given to a tensorflow model
            Creates 2 dataframes for features and labels and then splits them into training and testing sets
            The default value for this function is the concatenated, condences df created earlier: offData"""    
    
    ##define the dataframes and fill them with given information
    features = pd.DataFrame()
    labels = pd.DataFrame()
    features['Age'] = df['Age']
    features['AB'] = df['AB']
    features['H'] = df['H']
    features['R'] = df['R']
    features['RBI'] = df['RBI']
    features['HR'] = df['HR']
    features['SB'] = df['SB']
    labels = df['R$']
    
    ##divide the data into training and testing splits with 20% to be a testing split
    trainx, testx, trainy, testy = train_test_split(features, labels, test_size=.2)
    return (trainx, trainy), (testx, testy)
    
##set variables for the train test splits
(trainx, trainy), (testx, testy) = offLoad()



def export(dfram, name):
    '''exports a dataframe to local file, names file according to input'''
    dfram.to_csv(name)
    
    

def train_input_fn(features, labels, batch_size):
    """An input function for tensorflow for training"""
    # Convert the inputs to a Dataset.
    
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    # Shuffle, repeat, and batch the examples.
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)

    # Return the dataset.
    return dataset


def eval_input_fn(features, labels, batch_size):
    """An input function for tensorflow for evaluation or prediction"""
    
    features=dict(features)
    if labels is None:
        # No labels, use only features.
        inputs = features
    else:
        inputs = (features, labels)

    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices(inputs)

    # Batch the examples
    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)
    # Return the dataset.
    return dataset