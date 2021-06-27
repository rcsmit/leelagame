# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 12:04:30 2020

@author: rcxsm
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 23:40:39 2020

@author: rcxsm
"""

import random
import sys
import time

from plotly.graph_objs import Bar, Layout
from plotly import offline
from matplotlib import pyplot as plt
from collections import Counter

numberofgames = 10_000

numberofrounds = 0
currentposition = 0
tempthrown = 0
zesnumber_thrown = False
started = False
route = []
r = 1
printregel=[]
specials= (
            #ladders
            [10,23],
            [17,69],
            [20,32],
            
            [22,60],
            [27,41],
            [28,50],
            
            [45,67],
            [37,66],
            [46,62],
            [54,68],
            #snakes            
            [63,2],
            [55,3],
            [16,4],
            [29,6],
            [24,7],
            [12,8],
            [44,9],
            [52,35],
            [72,51])
results=[]

def throw_dice():
    """ Throw the dice """
    global numberofrounds
    
    number = random.randint(0,5)
    number_thrown = number + 1
    #print (f"{play}/{numberofrounds} - You have thrown { number_thrown}")
    numberofrounds +=1
    
    return number_thrown

def median(v):
    """ find the median """
    n = len (v)
    sorted_v = sorted(v)
    midpoint = n//2
    if n%2 ==1:
        #if  odd, return the middle value
        return sorted_v[midpoint]
    else:
        #if evenm return the average of the middle values
        lo = midpoint -1
        hi = midpoint
        return (sorted_v[lo]+sorted_v[hi]) / 2
    
def quantile (x,p):
    """returns the pth-percentile value in x """
    p_index = int (p * len(x))
    return sorted (x)[p_index]

def printx(a):
    """ Only print when in debuging mode """
    global printregel
    
    debug = False
    if debug == True:
        print (a)
    else:
        printregel.append(a)
        pass
          
def plotresults():
    """ plot the results """
    frequencies = []
    #print (results)
    m = max(results)+1
    for value in range(1,m):
        freq = results.count(value)
        frequencies.append(freq)
    #print (frequencies)
    cumm=[]
    t=0
    
    # calculate cummulative values
    for freq in frequencies:
        t+=freq
        cumm.append(t)
      
    #visualize in the browser
    x_values = list (range(1,m))
    data = [Bar (x=x_values, y = frequencies)]
     
    x_axis_config = {'title':'Result'}
    y_axis_config = {'title':'Frequency'}
    title = "Needed rounds to end the Leela game (" + str(numberofgames) + " games)"
    my_layout = Layout (title=title, 
                        xaxis = x_axis_config, yaxis=y_axis_config)
    offline.plot ({'data':data, 'layout': my_layout})    
    
    
   
    # plot on the console
    plt.xlabel("# of dice thrown ")
    plt.ylabel("frequencies")
    plt.bar(x_values, frequencies) 
    plt.show
    
   

    
    print ("=========== cumm frequency in deciles ==============")
    
    print (f"MEAN = {(sum(results)/len(results))}")
    print (f"    min = {min(results)}")
    
    print (f"    0.1 = {quantile(results,0.10)}")
    print (f"   0.25 = {quantile(results,0.25)}")
    print (f"MEDIAAN = {median(results)}")
    print (f"   0.75 = {quantile(results,0.75)}")
    print (f"   0.95 = {quantile(results,0.95)}")
    print (f"    max = {max(results)}")


def playgame():
    global started
    global currentposition
    global tempthrown
    global zesnumber_thrown
    global route
    global r
    global printregel
    #time.sleep(0.25)
    
    thrown = throw_dice()
    route.append(thrown)
    printx (f"{play} / {numberofrounds}. You have thrown {thrown} - {started}")
        
    # TO DO
    # Exception: if six drops out three times in a row, they are not summed, 
    # but are reset.  If a player rolls four or more 
    # sixes in a row, he continues to roll the dice until a number other than 
    # six falls out, and then he goes forward by the number of steps equal 
    # to the total sum of all points thrown,
    # and then passes the dice.
   
    if (started == False and thrown == 6) or (started == True):   
    
        if (started == False and thrown == 6):
            #route.append(999)
            pass
        started = True
        
        oldposition = currentposition     
        currentposition += thrown
        
        if currentposition > 72:
            currentposition = currentposition - thrown-tempthrown
            printx (f"You stay at {currentposition}")
        else:
            printx (f"             {oldposition} +  {thrown} = {currentposition}\n ")
          
        for value in specials:
                if currentposition == (value[0]):
                    currentposition = value[1]
                    printx(f"You go from {value[0]} to {value[1]} ")
           
        if currentposition == 68:   #COSMIC CONSCIOUSNESS
            #printx (f"{play}. {(route)}")
            #for prg in printregel:
            #    print (prg)
            if numberofrounds <5:
                #for prg in printregel:
                #    print (prg)
            
                #print (printregel)
                #print (f"========= {play} / {r}. {(route)}")
                #r+=1
                pass
                
            if play % 100_000 == 0:
                # print a line to show progress one time per 100k games
                print (f"{play}th game - YOU ARRIVED AT COSMIC CONSCIOUSNESS (#68) in {numberofrounds} ROUNDS")
            results.append(numberofrounds)    
        else:
            playgame()
    else:
        # Player didn't throw a 6 yet to start
        playgame()    
    
    
def main():   
    global numberofrounds
    global currentposition
    global play
    global numberofgames
    global route
    global printregel
    global started
    
    s1 = (int(time.time()))
    
    for play in range(1,(numberofgames+1)):  
        printx (f"------------{play}--------------")
        route=[]
        printregel=[]
        numberofrounds = 0
        currentposition = 0
        started = False
        
        playgame() 
        printx (f"------------/{play}--------------")
    plotresults()
    
    s2 = (int(time.time()))
    s2x = s2-s1
    print(f"Playing these {numberofgames} games took " + str(s2x) + " seconds ....")
main()
    
