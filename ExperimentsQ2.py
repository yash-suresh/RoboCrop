from RoboCrop import *

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.stats import f_oneway

def runSetOfExperiments(numberOfRuns,numberOfBots, code):
    #runs a set of experiments for each number of robots a certain number of times.
    # so 1 robot: 1 set,  2 robots: 1 set ....and so on

    

    listOfMeans = []
    #contains the mean of the result for 'each number of bots'
    #should look like [x1,x2, ....xn] where n = number of bots, and 'x' is the average
    #each algorithm should produce one list.

    for i in range(1, numberOfBots+1):

        grassPercentCollectedList = []

        for _ in range(numberOfRuns):
            grassPercentCollectedList.append(runOneExperiment(i, code))

        averageGrassPercent = sum(grassPercentCollectedList) / len(grassPercentCollectedList)

        listOfMeans.append(averageGrassPercent)

    return listOfMeans
    


def runExperimentsWithDifferentParameters():
    
    resultsDict = {}

    movementAlgorithms = ['lw', 'rw', 'b', 'q', 'r']
    
    algoName = ["Linear Wander", "Random Wander", "Bisector Search", "Quadrant Search",
    "Repel"]

    numOfBots = 8
    numOfRuns = 10

    for i, code in enumerate(movementAlgorithms):

        resultsDict[algoName[i]] = runSetOfExperiments(numOfRuns, numOfBots, code)

    #print(resultsDict)
    Anova(resultsDict)
    plot_results(resultsDict)


def Anova(resultsDict):
    lw_results = resultsDict['Linear Wander']
    rw_results = resultsDict['Random Wander']
    bs_results = resultsDict['Bisector Search']
    qs_results = resultsDict['Quadrant Search']
    r_results = resultsDict['Repel']

    # Perform ANOVA test
    f_statistic, p_value = f_oneway(lw_results, rw_results, bs_results, qs_results, r_results)

    # Print results
    print('F-statistic:', f_statistic)
    print('p-value:', p_value)

def plot_results(resultsDict):
    
    # Create a new figure
    fig, ax = plt.subplots()

    # we need to plot each line separately
    for algorithm, results in resultsDict.items():
        ax.plot(range(1, len(results) + 1), results, label=algorithm)

    # Setting the x-axis label and tick marks
    ax.set_xlabel('Number of bots')
    ax.set_xticks(range(1, len(resultsDict["Linear Wander"]) + 1))

    # Setting the y-axis label and limits
    ax.set_ylabel('Grass percent collected')
    ax.set_ylim([0, 100])

    
    ax.legend()
    plt.show()

runExperimentsWithDifferentParameters()






