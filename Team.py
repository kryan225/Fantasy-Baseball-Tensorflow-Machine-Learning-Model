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
import DataManipulation as DM
import Batter as bat
import pandas as pd
import numpy as np
#import DraftTool2020 as DT

from tabulate import tabulate
from random import randint
from functools import reduce

class TeamError(Exception):
    '''base class for Team Errors'''
    pass

class NoPositionError(TeamError):
    '''raised when attempting to access a non-existent attribute on Team'''
    pass

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
        
    def attrs(self):
        return [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self,a)) and a is not 'Name']
    
    def isAttr(self,a):
        if(a in self.attrs()):
            return True
        else:
            raise NoPositionError
    
    def get(self, atr):
        if(self.isAttr(atr)):
            return getattr(self, atr)
    
    def set(self, atr, val):
        if(self.isAttr(atr)):
            return setattr(self, atr, val)
    
    def printTeam(self, atr = 'Player'):
        tm = ''
        for a in self.attrs():
            if getattr(self, a) is not None:
                player = getattr(self,a)
               # print(a, ' - ', getattr(self,a)[atr])
                tm += a + ' - ' + player.Name +  '  -- ' + str(player.Salary) +'\n'
        print(tm)
        
    '''
    formats a team to be printed as data in tabulate function
    team data should be formatted: 
        [(playerName, position, salary, stats?)]
        just turn this thing into a tabulate
    '''
    def getData(self):
        header = ['Position', 'Player', 'Salary']
        data = []
        for position in self.attrs():
            if getattr(self, position) is not None:
                player = getattr(self,position)
                data.append([position, player.Name, str(player.Salary)])
            else:
                data.append([position, 'Empty', 0])
            
        return(tabulate(data, headers=header))
            
        '''
        MRCHEATSHEET - JOHNATHANS TOOL **********************************************************************************
        
        
        *****************************************************************************************************************
        
        '''
    
    def isComplete(self):
        '''
        Checks to see if all postions are filled on the team - returns true is team has all positions filled
        '''
        emtAttrs = [self.Catcher1 is None, self.Catcher2 is None, self.First is None, self.Second is None, self.Third is None,
                    self.Shortstop is None, self.MiddleINF is None, self.CornerINF is None, self.OF1 is None, self.OF2 is None,
                    self.OF3 is None, self.OF4 is None, self.OF5 is None, self.Utility is None]
        ret = True
        for a in emtAttrs:
            ret = ret and (not a)
        return ret
        
    def getOpen(self):
        '''
        Prints all open positions
        '''
        opn = []
        for a in self.attrs():
            if getattr(self, a) is None:
                opn.append(a)
        return opn
            
    '''
    prints how much money is being spent on offense
    '''
    def getOffensiveSalary(self):
        b = 0
        for a in self.attrs():
            player = getattr(self,a)
            if player is not None:
                b += player.Salary
        return b
        
    '''
    Not too sure what this function is doing
    '''
    def buildPD(self):
        df = pd.DataFrame()
        opn = self.getOpen()
        for a in self.attrs():
            if a not in opn:
                df = df.append(getattr(self, a))
        return df
    
    
    '''
    Moves a batter to a new specified position
    '''
    def moveBatter(self, batterName, newPosition):
        wasSuccessfull = False
        for a in self.attrs():
            if self.get(a) is not None and self.get(a).Name == batterName and not wasSuccessfull:                
                self.set(newPosition, self.get(a))
                self.set(a, None)
                print('Moving ' + batterName + ' to ' + newPosition)
                wasSuccessfull = True
        if not wasSuccessfull:
            print('Unable to find ' + batterName)
                
        
    '''
    Adds a batter to the proper position 
    '''
    def addBatter(self, batter):
        
        pos = batter.Pos
        ret = True
        if '2' in pos:
            if self.Catcher1 is None:
                self.Catcher1 = batter
            elif self.Catcher2 is None:
                self.Catcher2 = batter
            elif self.Utility is None:
                self.Utility = batter
            else:
                ret = False
        elif '3' in pos:
            if self.First is None:
                self.First = batter
            elif self.CornerINF is None:
                self.CornerINF = batter
            elif self.Utility is None:
                self.Utility = batter
            else:
                ret = False
        elif '4' in pos:
            if self.Second is None:
                self.Second = batter
            elif self.MiddleINF is None:
                self.MiddleINF = batter
            elif self.Utility is None:
                self.Utility = batter
            else:
                ret = False
        elif '5' in pos:
            if self.Third is None:
                self.Third = batter
            elif self.CornerINF is None:
                self.CornerINF = batter
            elif self.Utility is None:
                self.Utility = batter
            else:
                ret = False
        elif '6' in pos:
            if self.Shortstop is None:
                self.Shortstop = batter
            elif self.MiddleINF is None:
                self.MiddleINF = batter
            elif self.Utility is None:
                self.Utility = batter
            else:
                ret = False
        elif '7' in pos or '8' in pos or '9' in pos:
            if self.OF1 is None:
                self.OF1 = batter
            elif self.OF2 is None:
                self.OF2 = batter
            elif self.OF3 is None:
                self.OF3 = batter
            elif self.OF4 is None:
                self.OF4 = batter
            elif self.OF4 is None:
                self.OF4 = batter
            elif self.OF5 is None:
                self.OF5 = batter
            elif self.Utility is None:
                self.Utility = batter
            else:
                ret = False
        else:
            if self.Utility is None:
                self.Utility = batter
            else:
                ret = False
        return ret
    
    
    '''
    Drops the current player in the given position from the team
        the position is now None    
    '''
    def dropBatter(self, position):
        try:
            self.set(position, None)
        except:
            print( 'No attribute (position): ' + position)             
            
        



        
        
        



'''
team = pd.DataFrame()#columns = ['Player', 'AB', 'H', 'R', 'HR', 'RBI', 'SB', 'Sal'])
team = team.append(players.loc[players['Player'] == 'Mike Trout CF | LAA '])
'''


    

def randomTeam(teamName, budget, playerPool):
    ''' 
    Forms a random team that will be beneath a specified budget
    
    
    **currently gets next batter in csv if it can afford it**
    ''' 
    randTeam = Team(teamName)
    
    for index, row in playerPool.iterrows():
        if randTeam.isComplete():
            return randTeam
        batter = Batter.makeBatter(row)
        maxBid = budget - len(randTeam.getOpen()) + 1
        if batter.Salary <= maxBid:
            if randTeam.addBatter(batter):
                budget = budget - batter.Salary
                playerPool = playerPool.drop(index)
                #print('Added ' + batter.Name + 'for: ' + str(batter.Salary) + '   - New Max Bid: ' + str(budget + 1 - len(randTeam.getOpen())))
                #print('$left: ' + str(budget) + '   - spots left: ' + str(randTeam.getOpen()))
    return randTeam
    
    

'''
def optimalTeam(budget, team = Team('Name'), csv = DM.predictions):  
    budget -= team.getOffensiveBudget()
    stats = DM.parsePredictions(csv)
    players = DM.ready(stats)
    players['VAL'] = (players['H'] + players['HR'] + players['RBI'] + players['R'] + players['SB'])
    players = players.sort_values('VAL', ascending=False)
    for index, row in players.iterrows():
        if budget - row['Sal'] > len(team.getOpen()):
            budget = budget - row['Sal'] 
            name =  row['Player']
            bttr = stats.loc[stats['Player'] == name].squeeze()
            
            team.addBatter(bttr)
    #team.printTeam()
    return team, players

team, players = optimalTeam(200)

'''
    
b1 = bat.Batter('Arenado', ['5'], 499, 140, 100, 40, 100, 3, 41)
#b1.printPlayer()
b2 = bat.Batter('Arenado', ['4'], 499, 140, 100, 40, 100, 3, 41)
b3 = bat.Batter('Arenado', ['3'], 499, 140, 100, 40, 100, 3, 41)
b4 = bat.Batter('Arenado', ['2'], 499, 140, 100, 40, 100, 3, 41)
b5 = bat.Batter('Arenado', ['1'], 499, 140, 100, 40, 100, 3, 41)

team1 = Team('Team1')
team1.addBatter(b1)
team1.addBatter(b2)
team1.addBatter(b3)
team1.addBatter(b4)
team1.addBatter(b5)
#print(team1.printTeam())

'''
def main():
    
    #comment for main lol
    
    
        
if __name__ == "__main__":
    main()
'''