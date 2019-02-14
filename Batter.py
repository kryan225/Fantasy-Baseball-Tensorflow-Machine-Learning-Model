# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 16:32:01 2019

This file's purpose is for the batter class. This is what a fantasy baseball team's offense will compose of

This is for a personal project where I develop a fantasy baseball draft toolkit for my custom league. 
The winner of my league gets $600+ and as of developing this, my team has finished 7th place four years in a row.
The cutoff of winning any money back is 6th place so my co-owner/brother and I are a little annoyed. I hope that this
toolkit will provide us with an advantage for evaluating players and forming a draft strategy. Even though you don't necessarily 
win your league on draft day, you can have a massive head start and it is possible to lose the league at the draft. 

any questions or comments please email me at: kryan225.gomets@gmail.com

@author: kryan
"""

class Batter:
    def __init__(self, Name, Pos, AB, H, R, HR, RBI, SB, Salary):
        self.Name = Name
        self.Pos = Pos
        self.AB = AB
        self.H = H
        self.R = R
        self.HR = HR
        self.RBI = RBI
        self.SB = SB
        self.Salary = Salary
        
        
    def getAVG(self):
        '''
        Returns the batting average of the batter: Hits/At Bats
        '''
        return round(self.H / self.AB, 3)
        
    def printPlayer(self):
        '''
        Prints that batter's name and information
        '''
        print(self.Name,
              " Pos: ", self.Pos,
              " AB: ", self.AB,
              " H: ", self.H, 
              " AVG: ", self.getAVG(), 
              " R: ", self.R, 
              " HR: ", self.HR,
              " RBI: ", self.RBI,
              " SB: ", self.SB,
              " Sal: ", self.Salary)