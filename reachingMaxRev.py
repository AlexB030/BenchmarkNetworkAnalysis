#!/usr/bin/python3

###################################################
# This script calculates over all 200 independent
# simulations for all combinations of defense and
# network, what share reached the respective net-
# works individual rmax. It was reached at least
# once for all network-defense combinations so
# that the highest value in each of the 200 is the
# baseline to compare with.
###################################################


import matplotlib.pyplot as plt
import sys
import math
import os
import csv
import pickle
import numpy as np

resultMatrix={}
#load pickle file
file = open("boxplot_maxRev_dump.pkl", 'rb')
resultMatrix=pickle.load(file)
file.close()

scenarios=[]
for scenario in resultMatrix.keys():
    scenarios.append(scenario)
#print(scenarios)
defenses=[]
for defense in resultMatrix[scenarios[0]].keys():
    defenses.append(defense)
#print(defenses)
#defenses=["coldMigrationWithIpShuffle","ipShuffling","liveMigration","resetRCErights","noDefense"]

achievalRate=[]

for scenario in scenarios:
    belowMax=0
    scenarioNumber=scenario.split("_")[1]
    # create base line with no defense
    defense="noDefense"
    vector=resultMatrix[scenario][defense]
    vector.sort()

    # median
    maxRev=vector[-1]
    for revVal in vector:
        if revVal < maxRev:
            belowMax+=1
    achievalRate.append((200-belowMax)/2)

meanRev=sum(achievalRate)/len(achievalRate)
print(achievalRate)
print(meanRev)
