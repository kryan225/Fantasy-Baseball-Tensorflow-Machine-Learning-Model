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

def buildSinglePredict(ab, age, h, hr, r, rbi, sb):
    prediction = {'AB':[ab],
                  'Age':[age],
                  'H':[h],
                  'HR':[hr],
                  'R':[r],
                  'RBI':[rbi],
                  'SB':[sb]
                  }
    return prediction

def modelPredict(predict_x, expected):
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
       ageCol,
       atbatCol, 
       #hitCol,
       runCol,
       #rbiCol,
       #hrCol,
       sbCol,      
       tf.feature_column.indicator_column(tf.feature_column.crossed_column(['H', 'AB'], hash_bucket_size=int(1e4))),
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
                        model_dir='saved'
    )
    

    predictions = model.predict(
          input_fn=lambda:DM.eval_input_fn(predict_x,
                                                  labels=None,
                                                  batch_size=100))

    template = ('\nPrediction is "{}" , expected "{}"')
    ret = []
    realret = []
    
    
    
    for pred_dict,expec in zip(predictions, expected):
        #ret.append(pred_dict["predictions"])
        
        print(template.format(pred_dict["predictions"][0], expec))
        ret.append(pred_dict["predictions"][0])

    
    return ret