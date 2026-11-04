"""
Developed for https://neumann-probe.net/
Used as experiment into working with APIs

To run:
1. Change apiKey in Neumann_Func.py
2. Type in commandline: python Neumann_Script.py
3. When prompted, enter the probeID out of the list given you want to focus on

Available functions:
listProbes()
getFreeSpace(targetID)
getProbeMetal(targetID)
"metals"
"ice"
"carbon_compounds"
"deuterium"
"""
from Neumann_Func import *

listProbes()

#Asks user which probe they want to focus on and stores the value
targetID = input("Input the ID of the probe you want to focus on: ")

#getFreeSpace(targetID)
#getProbeMetal(targetID)
#getProbeCarbonCompounds(targetID)
#getProbeIce(targetID)

#WIP
material = input("What material would you like to mine pick one of the following ['metals', 'ice', 'carbon_compounds', 'deuterium']: ")
amnt = input("Enter much would you like to mine in ECE (For deuterium, 1 percent is .01 ECE): ")
delegateMining(targetID, material, float(amnt))