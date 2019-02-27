# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 17:01:13 2019


This file's purpose is for the team class. This will hold the information for a single team. 

For now we are only concerned with the offense, so no pitcher will be included

This is for a personal project where I develop a fantasy baseball draft toolkit for my custom league. 
The winner of my league gets $600+ and as of developing this, my team has finished 7th place four years in a row.
The cutoff of winning any money back is 6th place so my co-owner/brother and I are a little annoyed. I hope that this
toolkit will provide us with an advantage for evaluating players and forming a draft strategy. Even though you don't necessarily 
win your league on draft day, you can have a massive head start and it is possible to lose the league at the draft. 

any questions or comments please email me at: kryan225.gomets@gmail.com

@author: kryan
"""
import Batter as bat
import pandas as pd
import numpy as np
from random import randint

class Team:
    def __init__(self, Name, c1=None, c2=None, first=None, second=None, third=None, short=None, mid=None, cornr=None,
                 of1=None, of2=None, of3=None, of4=None, of5=None, util=None):
        self.Name = Name
        self.Catcher1 = c1
        self.Catcher2 = c2
        self.First = first
        self.Second = second
        self.Third = third
        self.Shortstop = short
        self.MiddleINF = mid
        self.CornerINF = cornr
        self.OF1 = of1
        self.OF2 = of2
        self.OF3 = of3
        self.OF4 = of4
        self.OF5 = of5
        self.Utility = util
        
'''
I wonder if it will be easier to just use a pandas dataframe to represent a team instead of making a new object.


I will begin to test creating a team in a dataframe and then decide which method to go with

'''
        


players = pd.read_csv('predictions.csv')
budget = 200
team = pd.DataFrame()#columns = ['Player', 'AB', 'H', 'R', 'HR', 'RBI', 'SB', 'Sal'])
team = team.append(players.loc[players['Player'] == 'Mike Trout CF | LAA '])


while budget > 0:
    rand = randint(0,len(players.index - 1))
    team = team.append(players.iloc[rand])
    players = players.drop(players.index[rand])
    budget = 200 - team['Sal'].sum()



def main():
    print()
    '''
    b1 = bat.Batter('Arenado', [5], 499, 140, 100, 40, 100, 3, 41)
    b1.printPlayer()
    
    team1 = Team('Team1', b1)
    team1.Catcher1.printPlayer()
    '''
        
if __name__ == "__main__":
    main()