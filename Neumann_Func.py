"""
Developed for https://neumann-probe.net/
Directory for Neumann-script.py
API max query amount is ??? per ???
"""
# Import libraries
import requests
import json
import math

# Main URL, API key, and API get / post auth header
mainUrl = "https://neumann-probe.net"
apiKey = "vng_NKGtXQRDbTHZoSiGiS2VHze30rmO2raL3PsusGhzd3Y"
authHeader = {
    "Authorization": f"Bearer {apiKey}"
}

# File variables
metalSupplies = ['A']
carbonSupplies = ['A']
iceSupplies = ['A']
deuteriumSupplies = ['A']
freeCapacity = ['A']
craftingRecipes = {}
craftingQueue = []


#List out all user probes by name and ID, and update recipe list 2 API request
def listProbes():
    # Request from API for list of probes
    response = requests.get( mainUrl + "/api/probes", headers=authHeader)
    probeData = response.json()
    # Find num of probes
    numProbes = len(json.loads(json.dumps(probeData))['probes'])

    # For each probe, list out name and ID
    for i in range (numProbes):
        probeName = probeData['probes'][i]['name']
        probeID = str(probeData['probes'][i]['id'])
        print("Probe named " + probeName + " has an ID of " + probeID)
    return

def cacheRecipes():
    response = requests.get(mainUrl + "/api/crafting-recipes", headers=authHeader)
    craftingData = response.json()
    craftingRecipes = craftingData
    return

# Finds the values for all of the resources on the given probe, calls the API 1 time.
def cacheProbeInventory(probeID):
    # Get the info about the sector from the API
    response = requests.get(mainUrl + "/api/probe/" + probeID + "/sector", headers=authHeader)
    sectorData = response.json()

    # Finds and stores the free capacity of the target probe in the queue. 
    freeECE = sectorData['inventory']['freeCapacity']
    freeCapacity.pop(0)
    freeCapacity.append(freeECE)

    # Finds and stores the amount of metals in the queue.
    totalMetals = sectorData['inventory']['resourceStocks'][0]['amount']
    metalSupplies.pop(0)
    metalSupplies.append(totalMetals)

    # Finds and stores the amount of ice in the queue.
    totalIce = sectorData['inventory']['resourceStocks'][1]['amount']
    iceSupplies.pop(0)
    iceSupplies.append(totalIce)

    # Finds and storse the amount of carbon compounds in the queue.
    totalCarbonCompounds = sectorData['inventory']['resourceStocks'][2]['amount']
    carbonSupplies.pop(0)
    carbonSupplies.append(totalCarbonCompounds)

    # Finds and stores the amount of deuterium in the queue.
    totalDeuterium = sectorData['inventory']['externalTanks'][0]['fillPercent']
    # Converts the deuterium value from a percentage to an ECE value
    totalDeuterium = totalDeuterium/100
    deuteriumSupplies.pop(0)
    deuteriumSupplies.append(totalDeuterium)
    return

# Returns amounts of a chosen resource
def queryResourceAmnt(probeID, resource):

    return

# Adds crafting tasks to the queue
def queueCrafting(probeID, recipeName, quantity):
    
        
    return

# Finds and returns all needed components of a required recipe, subtracting what is in probe storage
def getComponents(recipeName):
    

    return

# Is it crafted by mannys or by the printer? Return
def getCraftingMethod(recipeName):

    return

# Splits up the wanted resources among the available mannies for mining. 1 API request + 1 API post
def delegateMining(probeID, resource, amount):

    tasks = {
        "tasks": [
        
        ]
    }

    #Finds the total amount of trips and rounds UP to the nearest integer 
    tripCount = amount/.05
    tripCount = math.ceil(tripCount)

    asteroidId = 0

    freeMannies = availableMannies(probeID)

    #Finds the remaining resources after the maximum number of full trips are made.     
    leftoverResources = amount % .05

    #Get the info about the minable objects in the sector.
    response = requests.get(mainUrl + "/api/probe/"+ probeID +"/sector", headers = authHeader)
    sectorInfo = response.json()
    sectorMinables = json.loads(json.dumps(sectorInfo))["sector"]["objects"][0]["minableTargets"]
    
    #Sends the api an order for the mannies to start mining.
    for j in range(len(sectorMinables)):
        resourceType = sectorMinables[j]["resourceTypes"]
        for k in range(len(resourceType)):
            if resourceType[k] == resource:
                asteroidId = sectorMinables[j]["id"]
    
    if tripCount <= len(freeMannies):
        for i in range(tripCount-1):
            mannyTask = mineTaskJson(freeMannies[i], asteroidId, resource, .05)
            tasks['tasks'].append(mannyTask)
        if leftoverResources == 0:
            mannyTask = mineTaskJson(freeMannies[len(freeMannies)-1], asteroidId, resource, .05)
            tasks['tasks'].append(mannyTask)
        else: 
            mannyTask = mineTaskJson(freeMannies[len(freeMannies)-1], asteroidId, resource, leftoverResources)
            tasks['tasks'].append(mannyTask)

    else:

        resourcesToMine = (amount/len(freeMannies))*100
        resourcesToMine = math.ceil(resourcesToMine)/100

        for i in range(len(freeMannies)):
            mannyTask = mineTaskJson(freeMannies[i], asteroidId, resource, resourcesToMine)
            tasks['tasks'].append(mannyTask)

    print(requests.post(mainUrl + "/api/probe/" + probeID + "/mannies/tasks", json=tasks, headers = authHeader))
    return

# return array of availableManny id's, 1 API request
def availableMannies(probeID):
    freeMannys = []
    response = requests.get(mainUrl + '/api/probe/'+probeID + '/mannies', headers = authHeader)
    mannyInfo = response.json()
    numMannys = len(json.loads(json.dumps(mannyInfo))['mannies'])

    for i in range(numMannys):
        if mannyInfo['mannies'][i]['currentTask'] == None :
            freeMannys.append(mannyInfo['mannies'][i]['id'])

    return freeMannys

# formats manny mining work orders into json format
def mineTaskJson(mannyID, asteroidID, resource, amount):
    task = {

    }

    resources = [resource]

    task["mannyId"] = mannyID
    task["task"] = "mine"
    task["payload"]= {}
    task["payload"]["objectId"] = asteroidID
    task["payload"]["resources"] = resources
    task["payload"]["targetAmount"] = amount
    return task