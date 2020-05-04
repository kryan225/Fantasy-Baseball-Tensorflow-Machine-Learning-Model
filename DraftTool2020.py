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
    - Dynamically adjust for inlfation/deflation for current players based on current draft salaries and stat costs
    

@author: kryan225
"""



from Team import Team
from Batter import Batter
from League import League
import pandas as pd




playerPool = pd.read_csv('Positions.csv')



def randomTeam(teamName, budget):
    ''' 
    Forms a random team that will be beneath a specified budget
    
    
    **currently gets next batter in csv if it can afford it**
    ''' 
    randTeam = Team(teamName)
    global playerPool
    
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


print(len(playerPool.index))
r = randomTeam('rrrr',200)
print(len(playerPool.index))