"""
Developed for https://neumann-probe.net/
Used as experiment into working with APIs

To run:
1. Change apiKey in Neumann_Func.py
2. Change targetID to one of your probes IDs
3. Type in commandline: python Neumann_Script.py

Available functions:
listProbes()
getFreeSpace(targetID)
getProbeMetal(targetID)
"""
from Neumann_Func import *

# Targetted Probe
targetID = str(1168)

listProbes()
getFreeSpace(targetID)
getProbeMetal(targetID)