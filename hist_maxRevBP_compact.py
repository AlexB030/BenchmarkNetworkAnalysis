#!/usr/bin/python3

###################################################
# This program takes the matrixResult dicationary
# from boxPlotterAvgAccRev.py and calculates the
# upper and lower borders for the confidence inter-
# val of the median for each defense in every
# benchmark network.
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
#print("file loaded")
####################################
#              plot                #
####################################
#print(resultMatrix)
scenarios=[]
for scenario in resultMatrix.keys():
    scenarios.append(scenario)
#print(scenarios)
defenses=[]
for defense in resultMatrix[scenarios[0]].keys():
    defenses.append(defense)

histogrammData={}

headerLine="scenarioNumber;"
for defense in defenses:
    if(defense != "noDefense"):
        headerLine=headerLine+defense+";"
        histogrammData[defense]=[0,0,0]
print(headerLine)
for scenario in scenarios:
    strAppend=""
    scenarioNumber=scenario.split("_")[1]
    # create base line with no defense
    defense="noDefense"
    vector=resultMatrix[scenario][defense]
    vector.sort()

    # median
    b_topV=vector[-1]
    b_median=np.percentile(vector, 50)
    lQuartile=np.percentile(vector, 25)
    uQuartile=np.percentile(vector, 75)
    b_lCI= b_median - (1.574074074 * (uQuartile - lQuartile) / math.sqrt(len(vector)))
    b_uCI= b_median + (1.574074074 * (uQuartile - lQuartile) / math.sqrt(len(vector)))

    # now for all others
    for defense in defenses:
        if(defense != "noDefense"):
            vector=resultMatrix[scenario][defense]
            vector.sort()
            # median
            median=np.percentile(vector, 50)
            lQuartile=np.percentile(vector, 25)
            uQuartile=np.percentile(vector, 75)
            topV=vector[-1]
            lCI= median - (1.574074074 * (uQuartile - lQuartile) / math.sqrt(len(vector)))
            uCI= median + (1.574074074 * (uQuartile - lQuartile) / math.sqrt(len(vector)))
            #strAppend=strAppend+str(uCI).replace(".",",")+";"
            if (topV > b_topV):
                strAppend=strAppend+"+;"
                histogrammData[defense][2]+=1
            elif (topV < b_topV):
                strAppend=strAppend+"-;"
                histogrammData[defense][0]+=1
            else:
                strAppend=strAppend+"=;"
                histogrammData[defense][1]+=1

    print("%s;%s" % (scenarioNumber,strAppend))
print(histogrammData)

sequential=False
if sequential == True:
    for defense in defenses:
        if(defense != "noDefense"):
            categories = ('smaller', 'equal', 'higher')
            y_pos = np.arange(len(categories))
            performance = histogrammData[defense]

            plt.bar(y_pos, performance, align='center', alpha=0.5)
            plt.xticks(y_pos, categories)
            #plt.ylabel('Occurance')
            plt.title(defense)

            plt.show()

else:
    fig, axs = plt.subplots(2, 3,figsize=(12,6))
    categories = ('smaller', 'equal', 'higher')
    y_pos = np.arange(len(categories))

    performance = histogrammData['coldMigrationWithIpShuffle']
    axs[0, 0].bar(y_pos, performance, align='center', alpha=0.5)
    #axs[0, 0].xticks(y_pos, categories)
    axs[0, 0].set_title('Cold Migration')

    performance = histogrammData['ipShuffling']
    axs[0, 1].bar(y_pos, performance, align='center', alpha=0.5)
    #axs[0, 1].xticks(y_pos, categories)
    axs[0, 1].set_title('IP Shuffling')

    performance = histogrammData['noDefenseK1']
    axs[0, 2].bar(y_pos, performance, align='center', alpha=0.5)
    #axs[0, 1].xticks(y_pos, categories)
    axs[0, 2].set_title('Control Group 1')

    performance = histogrammData['liveMigration']
    axs[1, 0].bar(y_pos, performance, align='center', alpha=0.5)
    #axs[1, 0].xticks(y_pos, categories)
    axs[1, 0].set_title('Live Migration')

    performance = histogrammData['resetRCErights']
    axs[1, 1].bar(y_pos, performance, align='center', alpha=0.5)
    #axs[1, 1].xticks(y_pos, categories)
    axs[1, 1].set_title('VM Resetting')

    performance = histogrammData['noDefenseK2']
    axs[1, 2].bar(y_pos, performance, align='center', alpha=0.5)
    #axs[0, 1].xticks(y_pos, categories)
    axs[1, 2].set_title('Control Group 2')

    for ax in axs.flat:
        ax.yaxis.grid()

    fig.subplots_adjust(hspace=0.3)
    plt.setp(axs, xticks=y_pos, xticklabels=categories, yticks=[50,100,150,200,250,300,350,400,450,500])
    plt.savefig("histmaxRev", format="pdf", bbox_inches='tight', pad_inches=0.1)


    plt.close()
