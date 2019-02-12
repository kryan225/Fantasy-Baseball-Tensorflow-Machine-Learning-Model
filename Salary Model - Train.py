# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 12:44:10 2019

This file's purpose is to train a nueral net using tensorflow. The NN will be able to make predictions
for a baseabll player's fantasy baseball salary value, based off given projected stats

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


glob = 0
STEPS = 1000
PRICE_NORM_FACTOR = 1
DIRECTORY = 'Users\kryan\Desktop\larry'
#'Users\kryan\Google Drive\Ryan files\College\Senior\FantasyBaseballToolkit\Fantasy-Baseball-Tensorflow-Machine-Learning-Model\saved'



feature_specs_glob = {
                   'Age': tf.VarLenFeature(dtype=tf.int64),
                   'AB': tf.VarLenFeature(dtype=tf.int64),
                   'H': tf.VarLenFeature(dtype=tf.int64),
                   'R': tf.VarLenFeature(dtype=tf.int64),
                   'RBI': tf.VarLenFeature(dtype=tf.int64),
                   'HR': tf.VarLenFeature(dtype=tf.int64),   
                   'SB': tf.VarLenFeature(dtype=tf.int64),
                   }
                   
def main(argv):
    '''builds trains and evaluates the model'''
    
    #get the train/test data
    (train_x, train_y), (test_x, test_y) = DM.offLoad()
    
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
       #tf.feature_column.indicator_column(tf.feature_column.crossed_column(['HR', 'RBI', 'R'], hash_bucket_size=int(1e4))),
       #tf.feature_column.indicator_column(tf.feature_column.crossed_column(['H', 'AB', 'SB'], hash_bucket_size=int(1e4))),                                                                    
       #tf.feature_column.indicator_column(tf.feature_column.crossed_column(['H', 'AB', 'HR', 'RBI', 'R', 'SB'], hash_bucket_size=int(1e4))),
       #tf.feature_column.indicator_column(tf.feature_column.crossed_column(['H', 'AB', 'HR', 'RBI', 'R'], hash_bucket_size=int(1e4))),                                                                    
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
    
    # Train the model.
    # By default, the Estimators log output every 100 steps.
    model.train(input_fn=lambda:DM.train_input_fn(train_x, train_y, 100), steps=STEPS)
    
    # Evaluate how the model performs on data it has not yet seen.
    eval_result = model.evaluate(input_fn=lambda:DM.eval_input_fn(test_x, test_y, 100))

    # The evaluation returns a Python dictionary. The "average_loss" key holds the
    # Mean Squared Error (MSE).
    average_loss = eval_result["average_loss"]
    glob = eval_result
    # Convert MSE to Root Mean Square Error (RMSE).
    print("\n" + 80 * "*")
    print("\nRMS error for the test set: {:.0f} dollars"
          #.format(PRICE_NORM_FACTOR * average_loss**0.5))
        .format(average_loss))
    print("\nSaved at: " + model.model_dir + "\n")
    
    
    expected = [38]
    predict_x = {
          #'Age': [26],
          'AB':[549],
          'H': [173],
          'R': [123],
          'RBI': [100],
          'HR': [29],
          'SB': [30]
                        
      }

    predictions = model.predict(
          input_fn=lambda:DM.eval_input_fn(predict_x,
                                                  labels=None,
                                                  batch_size=100))

    template = ('\nPrediction is "{}" , expected "{}"')

    
  
    for pred_dict, expec in zip(predictions, expected):
        print(template.format(pred_dict["predictions"][0], expec))
    
    
    
    
    
    
    
    
if __name__ == "__main__":
  # The Estimator periodically generates "INFO" logs; make these logs visible.
  tf.logging.set_verbosity(tf.logging.INFO)
  tf.app.run(main=main)

