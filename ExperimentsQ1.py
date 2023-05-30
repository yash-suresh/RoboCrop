from RoboCrop import *

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def SetOfExperimentsWithNumberOnly(numberOfRuns,numberOfBots):
    
    
    listOfMeansOfAllAlgorithms = []

    movementAlgorithms = ['lw', 'rw', 'b', 'q', 'r']

    for i in range(1, numberOfBots + 1):

    
        for code in movementAlgorithms:  
            
            listOfMeansOfAllRuns = []     
        
            grassPercentCollectedList = []

            for _ in range(numberOfRuns):
                grassPercentCollectedList.append(runOneExperiment(i, code))

            averageGrassPercent = sum(grassPercentCollectedList) / len(grassPercentCollectedList)

            listOfMeansOfAllRuns.append(averageGrassPercent)

        listOfMeansOfAllAlgorithms.append(sum(listOfMeansOfAllRuns) / len(listOfMeansOfAllRuns))



    
    LinReg(listOfMeansOfAllAlgorithms)


def LinearRegression():
    pass

def Plot(l):
    
    plt.plot(l, marker = 'o')
    plt.xlabel('Number of bots')
    plt.ylabel('Percentage of grass cut (%)')
    plt.xlim(left=1)
    plt.show()

def LinReg(l):
    
    x = range(1, len(l)+1)
    slope, intercept, r_value, p_value, std_err = linregress(x, l)

    plt.plot(x, l, 'o', label='original data')
    plt.plot(x, intercept + slope*x, 'r', label='fitted line')
    plt.xlabel('Number of bots')
    plt.ylabel('Percentage of grass cut (%)')
    plt.legend()


    plt.show()

    print("Slope:", slope)
    print("Intercept:", intercept)
    print("R-value:", r_value)
    print("P-value:", p_value)
    print("Standard Error:", std_err)
    print(np.corrcoef(l))



numberOfRuns = 1
numberOfBots = 2

SetOfExperimentsWithNumberOnly(numberOfRuns,numberOfBots)