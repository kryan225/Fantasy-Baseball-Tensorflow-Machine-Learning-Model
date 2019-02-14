# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 15:55:07 2019

This file's purpose is to call a trained NN and call predictions on the model

This is for a personal project where I develop a fantasy baseball draft toolkit for my custom league. 
The winner of my league gets $600+ and as of developing this, my team has finished 7th place four years in a row.
The cutoff of winning any money back is 6th place so my co-owner/brother and I are a little annoyed. I hope that this
toolkit will provide us with an advantage for evaluating players and forming a draft strategy. Even though you don't necessarily 
win your league on draft day, you can have a massive head start and it is possible to lose the league at the draft. 

any questions or comments please email me at: kryan225.gomets@gmail.com

@author: kryan
"""
import tensorflow as tf
import numpy as np
import pandas as pd
import DataManipulation as DM
import operator

def buildSinglePredict(ab, h, r, hr, rbi, sb, age=26):
    prediction = {'AB':[ab],
                  'Age':[age],
                  'H':[h],
                  'HR':[hr],
                  'R':[r],
                  'RBI':[rbi],
                  'SB':[sb]
                  }
    return prediction

def modelPredict(predict_x, path='saved', expected=[0]):
    '''This function rebuilds a NN from a directory where it was saved in a training job
    It then runs a predction job based on the given inputs'''
    
    #build the feature columns
    ageCol = tf.feature_column.numeric_column(key='Age')
    atbatCol = tf.feature_column.numeric_column(key='AB')
    hitCol = tf.feature_column.numeric_column(key='H')
    runCol = tf.feature_column.numeric_column(key='R')
    rbiCol = tf.feature_column.numeric_column(key='RBI')
    hrCol = tf.feature_column.numeric_column(key='HR')
    sbCol = tf.feature_column.numeric_column(key='SB')
    
    #define the feature columns in a list
    feature_columns = [
       #ageCol,
       atbatCol, 
       hitCol,
       runCol,
       rbiCol,
       hrCol,
       sbCol,      
       tf.feature_column.indicator_column(tf.feature_column.crossed_column(['H', 'AB'], hash_bucket_size=int(1e4))),
      # tf.feature_column.indicator_column(tf.feature_column.crossed_column(['HR', 'RBI', 'R'], hash_bucket_size=int(1e4))),
      # tf.feature_column.indicator_column(tf.feature_column.crossed_column(['H', 'AB', 'SB'], hash_bucket_size=int(1e4))),                                                                    
      # tf.feature_column.indicator_column(tf.feature_column.crossed_column(['H', 'AB', 'HR', 'RBI', 'R', 'SB'], hash_bucket_size=int(1e4))),
      # tf.feature_column.indicator_column(tf.feature_column.crossed_column(['H', 'AB', 'HR', 'RBI', 'R'], hash_bucket_size=int(1e4))),   
    ]
    
    #configure checkpoints:
    my_checkpointing_config = tf.estimator.RunConfig(
                        save_checkpoints_secs = 20,  # Save checkpoints every 20 secs.
                        keep_checkpoint_max = 10,       # Retain the 10 most recent checkpoints.
    )
   
    # Build the Estimator.
    #model = tf.estimator.LinearRegressor(
    model = tf.estimator.DNNRegressor(
                        hidden_units=[31, 22, 15, 12],
                        feature_columns=feature_columns,
                        config=my_checkpointing_config,
                        model_dir=path
    )
    

    predictions = model.predict(
          input_fn=lambda:DM.eval_input_fn(predict_x,
                                                  labels=None,
                                                  batch_size=100))

    template = ('\nPrediction is "{}" , expected "{}"')
    ret = []
    
    
    
    for pred_dict,expec in zip(predictions, expected):
        #ret.append(pred_dict["predictions"])
        
        print(template.format(pred_dict["predictions"][0], expec))
        ret.append(pred_dict["predictions"][0])

    
    return ret
    
    
    
    
def runBatchPredict(file, modelPath='saved'):
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

    booyah = modelPredict(predictions, path=modelPath, expected=expected)


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