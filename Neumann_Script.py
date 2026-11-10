"""
Developed for https://neumann-probe.net/
Used as experiment into working with APIs

To run:
1. Change apiKey in Neumann_Func.py
2. Type in commandline: python Neumann_Script.py
3. When prompted, enter the probeID out of the list given you want to focus on

"metals"
"ice"
"carbon_compounds"
"deuterium"
"""
from Neumann_Func import *
import time

probeID = ""
validID = False
timer = 1
task = ""

#runs once when program begins
def startUp():
    print("Initiating program..")
    listProbes()
    probeID = input("Input the ID of the probe you would like to manage: ")
    task = input("Using probe " + probeID + " would you like to 'mine' or 'craft'? ")

    if (task == "mine"):
        print("Instantiating mining protocol...")
        print(" ")
        cacheProbeInventory(probeID)
        print("What material would you like to mine? Choose from the below choices: ")
        print("metals, ice, carbon_compounds, deuterium")
        material = input(" ")
        print("How much " + material + " would you like gathered?")
        amnt = input(" ")
        delegateMining(probeID, material, float(amnt))

    elif (task == "craft"):
        print("Instantiating crafting protocol...")
        print(" ")
        cacheRecipes()
        print("What would you like to craft? ")
        recipe = input(" ")
        print("How much of " + recipe + " would you like to craft?")
        amnt = input(" ")
        productionLoop()

    else:
        print("ERROR: Invalid task")

    return

def productionLoop():
    
    return


startUp()