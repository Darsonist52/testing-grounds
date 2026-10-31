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
"""
from Neumann_Func import *

listProbes()

#Asks user which probe they want to focus on and stores the value
targetID = input("Input the ID of the probe you want to focus on: ")

getFreeSpace(targetID)
getProbeMetal(targetID)
getProbeCarbonCompounds(targetID)
getProbeIce(targetID)