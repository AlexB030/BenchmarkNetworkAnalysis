#!/usr/bin/python3
import matplotlib.pyplot as plt
import sys
import os
import csv
import pickle

####################################
#         configuration            #
####################################
importDir="./10_mixed_716cca_12000rounds/condensed"
outputDir="./plots/"
show=False
freshImport=False

simPrefixes=[]
suffixes=["resetRCErights","noDefense","liveMigration","ipShuffling","coldMigrationWithIpShuffle","noDefenseK1","noDefenseK2"]

############################################################################
## this is to autodetermine all folders and differentiate different prefixes
############################################################################
autoIndex=False

if(autoIndex==True):
    simPrefixes=[]
    preliminarySimPrefixes = [f for f in os.listdir(importDir) if (os.path.isdir(os.path.join(importDir, f)) and "sim.pl" in f)]

    for currPref in preliminarySimPrefixes:
        newPref=currPref.split("sim.pl")[0]+"sim.pl"
        if newPref not in simPrefixes:
            simPrefixes.append(newPref)
    #print(simPrefixes)


############################################################################
## Ende
############################################################################

autoIndex=True

maxRounds=12000
resultMatrix={}
####################################
#             import               #
####################################
if freshImport==True:
    demoRuns=-1
    for run,simPrefix in enumerate(simPrefixes):
        if run==demoRuns:
            break
        resultMatrix[simPrefix]={}
        for suffix in suffixes:
            resultMatrix[simPrefix][suffix]=[]

            # obtain all shortlists from folder
            if (autoIndex==True):
                currPath=os.path.join(importDir,simPrefix+suffix)
                csvFiles = [f for f in os.listdir(currPath) if (os.path.isfile(os.path.join(currPath, f)) and "attacker1shortlist.csv" in f)]

            # go through all shortlists (csv) for given prefix and suffix
            for csvFile in csvFiles:
                anticipatedRow=1
                lastValue=0
                fullPath=os.path.join(importDir,simPrefix+suffix,csvFile)
                with open(fullPath, 'r') as csvDatei:
                    reader = csv.reader(csvDatei, delimiter=';')
                    accumRev=0
                    for row in reader:
                        if(int(row[0])==anticipatedRow):
                            # anticipated row is found, that means we don't need to interpolate
                            accumRev=accumRev+int(row[2])
                            anticipatedRow+=1
                            lastValue=int(row[2])
                        elif(int(row[0])>anticipatedRow):
                            # the found row does not match the anticipated row (that represents x values), which is why we have to fill up our values for x and y up until we reach a value for x that matches the currently found row
                            while(int(row[0])>anticipatedRow):
                                accumRev=accumRev+lastValue
                                anticipatedRow+=1
                            accumRev=accumRev+int(row[2])
                            anticipatedRow+=1
                            lastValue=int(row[2])
                        else:
                            # this should never happen since round numbers within rows increase at least by 1 for every row. still, we catch it
                            print("anticipated Row number is higher than the one from CSV file! rownumber doubled? .... maybe?")
                            break
                    while(anticipatedRow<=maxRounds):
                        accumRev=accumRev+lastValue
                        anticipatedRow+=1
                resultMatrix[simPrefix][suffix].append(float(accumRev/maxRounds))
                csvDatei.close()
            #X1=resultMatrix[simPrefix][suffix]
    # save pickleFile
    file = open("boxplot_avgAccRev_dump.pkl", 'wb')
    pickle.dump(resultMatrix, file)
    file.close()
else:
    #load pickle file
    file = open("boxplot_avgAccRev_dump.pkl", 'rb')
    resultMatrix=pickle.load(file)
    file.close()

####################################
#              plot                #
####################################

suffixes=["resetRCErights","noDefense","liveMigration","ipShuffling","coldMigrationWithIpShuffle","noDefenseK1","noDefenseK2"]
scenarios=resultMatrix.keys()
#filteredScenarios=["157","096"]
for scenario in scenarios:
    #if (scenario.split("_")[1] in filteredScenarios):
        plt.figure(figsize=(7, 6))
        X1=resultMatrix[scenario][suffixes[4]]
        X2=resultMatrix[scenario][suffixes[3]]
        X3=resultMatrix[scenario][suffixes[2]]
        X4=resultMatrix[scenario][suffixes[0]]
        X5=resultMatrix[scenario][suffixes[1]]

        #X6=resultMatrix[scenario][suffixes[5]]
        #X7=resultMatrix[scenario][suffixes[6]]

        line_props=dict(linestyle="dashed")
        plt.boxplot((X1, X2, X3, X4, X5), notch=True, sym="+", labels=["Cold","IP","Live","Reset","NoDef"], whiskerprops=line_props)
        #plt.title("Avg. Acc. Revenue for Scenario %s" % (scenario.split("_")[1]), fontsize=16, fontweight='bold')
        plt.ylabel('Avg. Acc. Revenue per Round', fontsize=18)
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)

        plt.savefig(os.path.join(outputDir,"bp_aar_"+scenario.split("_")[1]+".pdf"), format="pdf", bbox_inches='tight', pad_inches=0.1)
        #plt.savefig("bp_aar_"+scenario.split("_")[1]+".pdf", format="pdf", bbox_inches='tight', pad_inches=0.1)
        plt.grid()
        if show == True:
            plt.show()
        else:
            plt.close()
