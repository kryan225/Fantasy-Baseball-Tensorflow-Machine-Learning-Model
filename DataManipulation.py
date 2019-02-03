# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 15:56:59 2019

@author: kryan
"""


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
import matplotlib

##import 4 csv files with historical data from 2018-2015
data15 = pd.read_csv("2015_N_B.csv")
data16 = pd.read_csv("2016_N_B.csv")
data17 = pd.read_csv("2017_N_B.csv")
data18 = pd.read_csv("2018_N_B.csv")

##combine above dataframes into one dataframe
allData = pd.concat([data15,data16,data17,data18])

def getOstats(df):
    """Takes a raw dataframe exported from BaseballHQ and produces a condenced dataframe with specific
        Offesensive stats"""

    condence = pd.DataFrame()
    condence = df[['Age','AB','H','R','RBI','HR','SB','R$']]
    return condence
    
##define a dataframe that has condenced offensive categories 
offData = getOstats(allData)


def offLoad(df = offData):
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