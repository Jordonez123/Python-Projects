#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 16:01:28 2019

@author: jordonez
"""
import random
import math
from matplotlib import pyplot as plt
import numpy as np

def image_example():
    '''should produce red,purple,green squares
    on the diagonal, over a black background'''
    # RGB indexes
    red,green,blue = range(3)
    # img array 
    # all zeros = black pixels
    # shape: (150 rows, 150 cols, 3 colors)
    img = np.zeros((150,150,3))
    for x in range(50):
        for y in range(50):
            # red pixels
            img[x,y,red] = 1.0
            # purple pixels
            # set 3 color components 
            img[x+50, y+50,:] = (.5,.0,.5)
            # green pixels
            img[x+100,y+100,:] = (.5,.5,.5)
    plt.imshow(img)

def normpdf(x, mean, sd):
    """
    Return the value of the normal distribution 
    with the specified mean and standard deviation (sd) at
    position x.
    You do not have to understand how this function works exactly. 
    """
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

def pdeath(x, mean, sd):
    start = x-0.5
    end = x+0.5
    step =0.01    
    integral = 0.0
    while start<=end:
        integral += step * (normpdf(start,mean,sd) + normpdf(start+step,mean,sd)) / 2
        start += step            
    return integral    
    

recovery_time = 4 # recovery time in time-steps
virality = 0.2 # probability that a neighbor cell is infected in each time step
class Cell(object):

    def __init__(self,x, y):
        self.x = x
        self.y = y 
        self.state = 'S' # can be "S" (susceptible), "R" (resistant = dead), or 
        self.infect_time = 0
        self.count = 0
    def infect(self):
        self.state = 'I'
        self.infect_time = 0 #keeps track of the number of time_steps
    
    def process(self, adjacent_cells):
        die = pdeath(self.count,4,1) #this value stays the same for all cells
        if self.state == 'I':
            for el in adjacent_cells: #element in the dictionary
                if self.count%recovery_time == 0: #checks for every four time steps
                    el.state = 'S'
                p_recov = random.random() #arbitrary value for recovery probability
                if p_recov < die: #this kills the cell
                    self.state = 'R'
                if el.state == 'S':
                    x = random.random()
                    if x <= virality:
                        el.infect() #this infects the cell
                    else:
                        self.infect_time += 1
            self.count += 1 #increases how many times we infect a cell
            
        
        
        
class Map(object):
    
    
    def __init__(self):
        self.height = 150
        self.width = 150           
        self.cells = {}
        

    def add_cell(self, cell):
        self.cell = cell
        #cells should be the values not the keys
        self.cells[int(self.cell.x),int(self.cell.y)] = self.cell
    
    def display(self):
        red,green,blue = range(3)
        img = np.zeros((150,150,3))
        for key in self.cells:
            j = self.cells[key] #where j is the actual cell
            if self.cells[key].state == 'S':
                img[j.x,j.y,green] = 1.0 #sets green
            if self.cells[key].state == 'R':
                img[j.x,j.y,:] = (.5,.5,.5)#sets gray
            if self.cells[key].state == 'I':
                img[j.x,j.y,red] = 1.0 #sets red
                
        plt.imshow(img)
    
    def adjacent_cells(self,x,y):
        adj_cell_li = [] #list of adjacent cells
        top = x,y+1
        bot = x,y-1
        left = x-1,y
        right = x+1,y
        #checking if each tuple is in the cells dictionary
        if top in self.cells:
            cell = self.cells[top]
            adj_cell_li.append(cell)
        if bot in self.cells:
            cell = self.cells[bot]
            adj_cell_li.append(cell)
        if left in self.cells:
            cell = self.cells[left]
            adj_cell_li.append(cell)
        if right in self.cells:
            cell = self.cells[right]
            adj_cell_li.append(cell)
        return adj_cell_li
    
    def time_step(self):
        self.count = 0 #intializes self.count
        for key in self.cells: #key being the tuple of x and y
            adj = self.adjacent_cells(key[0],key[1])
            self.cells[key].process(adj)
        self.display()
        self.count+=1 #must increase value of self.count by 1
            
def read_map(filename):
    m = Map()
    fname = open(filename,"r")
    for el in fname:
        el.strip()
        for i in range(0,len(el),1):
            if el[i] == ',':
                cell = Cell(int(el[0:i]),int(el[i+1:]))
        m.add_cell(cell)
        
    return m
if __name__ == "__main__":
    print("This program will use the nyc_map.csv saved in Documents.")
    print()
    print('This will be followed by an already designed test for m.cells[(32,89)].infect()')
    print('To use other parameters, please comment out if __name__ == "__main__":')
    print()
    print('Please run multiple times')
    print()
    print('loading...')
    m = read_map("nyc_map.csv")
    m.cells[(32,89)].infect()
    for i in range(15):
        m.time_step()
    