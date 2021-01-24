#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:04:00 2020

I want this tool to be usuable during a draft

TODO:
    *For now I'm abandoning the machine learning aspect and creating a static tool'
    - Be able to hold 1 team with real players x
        - Hold 1 team with players from csv x
        ***Can now form a random team enforcing a given offensive budget
            ***Will get earliest player in csv that it can afford***
        
    - Be able to hold 12 teams with real players from csv x
        + Sep 2020:
            + Should League player pools be DF's or loBatter? 
            + Methods to implement:
                o Add new team xx
                o Add player pool from csv xx
                o Print teams xx
                o Draft player xx
                    ~ Make sure it affects player pool/drafted xx
                    ~ Make sure when querying for index from user, to check proper range of indexes
                        ex: cant give 15 when options are [6,88] xx
                o Print Rosters xx
                o Fill random league
                o Find player
                    ~ If player is drafted return team, else return FA row
                o re-write Team.
        - Want to adjust player pool when a player is drafted
            - will probably need to move League class to Team.py, 
            - so there can be a shared variable for player pool
            - I would love to have the seperate but that might not be worth its
            - Maybe combine all classes into one file to use for actual draft tool. Rename this file to League.py
            - I think we should put the Team class in a subclass of League. They should be connected or else I would
                need to pass the player pool through all the Team functions
                
            RYAN: next step is to move Team class to subclass of League
    
    - Track players who have been drafted and who is still left in the pool
    - Track salaries of players and total $$ left for a given team
    - Calculate the cost of relevant stats based on current draft
        - Use this to calculate players who are deals/expensive
    - DO All of the commands via command line, but send updates to front end/localhost "dashboard"
    - Dynamically adjust for inlfation/deflation for current players based on current draft salaries and stat costs
    

@author: kryan225
"""



from Team import Team
from Batter import Batter
import DataManipulation as DM
import pandas as pd




pp = pd.read_csv('Positions.csv')
pp = DM.stripNames(pp).reset_index(drop=True)

'''

def randomTeam(teamName, budget):
    ''' '''
    Forms a random team that will be beneath a specified budget
    
    
    **currently gets next batter in csv if it can afford it**
    ''' '''
    randTeam = Team(teamName)
    global pp
    
    for index, row in pp.iterrows():
        if randTeam.isComplete():
            return randTeam
        batter = Batter.makeBatter(row)
        maxBid = budget - len(randTeam.getOpen()) + 1
        if batter.Salary <= maxBid:
            if randTeam.addBatter(batter):
                budget = budget - batter.Salary
                pp = pp.drop(index)
                #print('Added ' + batter.Name + 'for: ' + str(batter.Salary) + '   - New Max Bid: ' + str(budget + 1 - len(randTeam.getOpen())))
                #print('$left: ' + str(budget) + '   - spots left: ' + str(randTeam.getOpen()))
        
    return randTeam
'''

print(len(pp.index))
#x = randomTeam('rrrr',200)
print(len(pp.index))








#League class
'''
This will act as the entire fantasy league
Will be a dict_of_team, pd.DataFrame, pd.DataFrame
    - [dict_of_team] teams : list of all teams in the league
    - [pd.DataFrame] fa_pool : list of players not on a team
    - [pd.DataFrame] drafted : list of players drafted
'''
class League:
    def __init__(self, teams=None, fa_pool=None, drafted=None):
        self.Teams = dict()
        self.Fa_pool = pd.DataFrame()
        self.Drafted = pd.DataFrame()
        
    
    '''
    Creates the free agent player pool by taking in a csv and returning a pd.DataFrame
    '''
    def createFaPool(self, csv):
        df = pd.read_csv(csv)
        self.Fa_pool =  DM.stripNames(df).reset_index(drop=True)
        
    
    '''
    Prints all the teams in the league
    '''
    def printTeams(self):
        for key in self.Teams:
            print(key)

    '''
    Returns a list of all the teams in the league
    '''
    def getTeams(self):
        ret = []
        for key in self.Teams:
            ret.append(self.Teams[key])
        return ret
    
    
    '''
    Adds a new team to the League, gives the option of adding a partially completed or already
    completed team
    '''
    def addTeam(self, name, team):
        if type(team) == Team:
            self.Teams[team.Name] = (team)
        else:
            newTeam = Team(name)
            self.Teams[name] = (newTeam)
        
    '''
    Print the data for every team in the league
    '''
    def printLeague(self):
        x = 'nothing'
        for key, value in self.Teams.items():
            x = value.getData()
            print(value.getData())
            print('-------------------------------------------\n')
        return x
            
            
    '''
    Drafts a player from the FA pool and onto a Team, also adds them to drafted pool
    '''
    def draftPlayer(self, playername, teamname):
        print("Drafting player: " + playername + " to team: " + teamname)
        pool = self.Fa_pool
        team = self.Teams[teamname]
        player = pool.loc[pool['Player'] == playername]
        response = -1
        
        #If more than one player is returned by searching the name
        if len(player.index) > 1:
            print(player.to_string())
            
            response = int(input("Which player do you want (Enter Index): "))
            isValidInput = response in player.index 
            while not isValidInput:                
                response = int(input("Not valid index, please put index in range: "))
                isValidInput = response in player.index 
            player = pool.iloc[response]
            print(player)
        elif len(player.index) < 1:
            print("No player found")
            return 
        
        
        bat = Batter.makeBatter(player)
        team.addBatter(bat)
        
        #Now remove the batter from the player pool and add them to drafted
        drafted = self.Drafted
        if(response >= 0):
            pool = pool.drop(response)
        else:
            pool = pool.drop(player.index[0])
        self.Drafted = drafted.append(player).reset_index(drop=True)
        self.Fa_pool = pool.reset_index(drop=True)
        
        
        return team
    
        


ll = League()
ll.createFaPool('Positions.csv')
print(len(ll.Fa_pool.index))
ll.addTeam('mtTeam',None)
#ll.draftPlayer('Trout, Mike', 'mtTeam')
print(ll.Teams['mtTeam'].getData())
print(len(ll.Fa_pool.index))













