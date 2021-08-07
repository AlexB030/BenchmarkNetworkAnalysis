#!/usr/bin/python3

################################
# This script creates Table V in
# the paper. Sorting of symbols
# CLRI as given in the defenses
# list
################################

import matplotlib.pyplot as plt
import sys
import math
import os
import csv
import pickle
import numpy as np

mrMatrix={}
#load pickle file
file1 = open("boxplot_maxRev_dump.pkl", 'rb')
mrMatrix=pickle.load(file1)
file1.close()

aarrMatrix={}
#load pickle file
file2 = open("boxplot_avgAccRev_dump.pkl", 'rb')
aarrMatrix=pickle.load(file2)
file2.close()

scenarios=[]
for scenario in mrMatrix.keys():
    scenarios.append(scenario)
#print(scenarios)
defenses=[]
for defense in mrMatrix[scenarios[0]].keys():
    defenses.append(defense)
#print(defenses)
# manual override of defense sorting
defenses=["noDefense","coldMigrationWithIpShuffle","liveMigration","resetRCErights","ipShuffling"]

effectDict={}


for scenario in scenarios:
    # here we get the baseline for comparison
    defense="noDefense"
    strAppend=""
    scenarioNumber=scenario.split("_")[1]

    # first for rmax
    vector=mrMatrix[scenario][defense]
    vector.sort()
    b_topV=vector[-1]

    # now for aarr
    vector=aarrMatrix[scenario][defense]
    vector.sort()
    b_median=np.percentile(vector, 50)
    lQuartile=np.percentile(vector, 25)
    uQuartile=np.percentile(vector, 75)
    b_lCI= b_median - (1.574074074 * (uQuartile - lQuartile) / math.sqrt(len(vector)))
    b_uCI= b_median + (1.574074074 * (uQuartile - lQuartile) / math.sqrt(len(vector)))

    # now rmax for all others
    for defense in defenses:
        if(defense != "noDefense"):

            # first for rmax
            vector=mrMatrix[scenario][defense]
            vector.sort()
            topV=vector[-1]
            if (topV > b_topV):
                strAppend=strAppend+"+"

            elif (topV < b_topV):
                strAppend=strAppend+"-"

            else:
                strAppend=strAppend+"="


    # now aarr all others
    for defense in defenses:
        if(defense != "noDefense"):
            vector=aarrMatrix[scenario][defense]
            vector.sort()
            # median
            median=np.percentile(vector, 50)
            lQuartile=np.percentile(vector, 25)
            uQuartile=np.percentile(vector, 75)
            lCI= median - (1.574074074 * (uQuartile - lQuartile) / math.sqrt(len(vector)))
            uCI= median + (1.574074074 * (uQuartile - lQuartile) / math.sqrt(len(vector)))
            if (lCI > b_uCI):
                strAppend=strAppend+"+"

            elif (uCI < b_lCI):
                strAppend=strAppend+"-"

            else:
                strAppend=strAppend+"="


    #print(strAppend)
    if (strAppend in effectDict.keys()):
        effectDict[strAppend]+=1
    else:
        effectDict[strAppend]=1

#print(effectDict)
listofTuples = sorted(effectDict.items() , reverse=True, key=lambda x: x[1])
# Iterate over the sorted sequence
for elem in listofTuples :
    print("\\texttt{"+elem[0][0:4]+"}&"+"\\texttt{"+elem[0][4:9]+"}&"+str(elem[1]))
