# BenchmarkNetworkAnalysis

Repository containing python scripts, pkl files with condensed data, and ready-made graphs from evaluating 500 automatically generated scenarios.

## Description

The analysis-folder contains all boxplots for "maximum accumulated revenue" and "average accumulated revenue per round" for all of the 500 benchmark networks. Furthermore, this repository contains six python scripts. The files "boxPlotterAvgAccRev.py" and "boxPlotterMaxRev.py" will produce the aforementioned boxplots. The files "hist_avgAccRevBP_compact.py" and "hist_maxRevBP_compact.py" will produce the histograms, showing for how many of the networks the defenses could lower rmax and ravg_j respectively. The file "effect_table.py" will produce an output on the command line that was used to generate the effect distribution table. Finally, "reachingMaxRev.py" calculates the percentage of simulations that reached their respective rmax. For each combination of defense and network, 200 independent simulations have been conducted among which is always at least one simulation (in most cases many more), where the possible rmax was realized. This highest value served as the base line to calculate the percentage of other simulations that reached this max revenue.

The two pkl-files enclosed in the analysis-folder contain the data that are used for computation. These haven been exracted from all conducted simulations and only contain the information needed for the tasks mentioned above. Including the raw data was not possible for exceeding any reasonable limit.
