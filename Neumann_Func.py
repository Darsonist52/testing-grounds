"""
Developed for https://neumann-probe.net/
Directory for Neumann-script.py
"""
# Import libraries
import requests
import json
import math

# Main URL, API key, and API get / post auth header
mainUrl = "https://neumann-probe.net"
apiKey = "vng_lB807-k62WxF99R3vcp2J1v4GMPdu9qB8VrCrO9Z4Tk"
authHeader = {
    "Authorization": f"Bearer {apiKey}"
}

# File variables
metalSupplies = ['A']
carbonSupplies = ['A']
iceSupplies = ['A']
deuteriumSupplies = ['A']
freeCapacity = ['A']
craftingQueue = []


#List out all user probes by name and ID, 1 API request
def listProbes():
    # Request from API for list of probes
    response = requests.get( mainUrl + "/api/probes", headers=authHeader)
    probeData = response.json()

    # Find num of probes
    numProbes = len(json.loads(json.dumps(probeData))['probes'])
    print("You have a total of: " + str(numProbes) + " probe(s)!")

    # For each probe, list out name and ID
    for i in range (numProbes):
        probeName = probeData['probes'][i]['name']
        probeID = str(probeData['probes'][i]['id'])
        print("Probe named " + probeName + " has an ID of " + probeID)
    return

# Finds the values for all of the resources on the given probe, calls the API 1 time.
def queryProbeInventory(probeID):
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

#
def queueCrafting(probeID):
    
        
    return

# WIP You guessed it, makes a container
"""""
def makeContainer(probeID):
    freeMannies = availableMannies(probeID)
    containersWanted = input("Enter the number of containers you want to construct: ")
    print("You have enough metals for " + metalSupplies(0)/0.54 +" containers.")
    if (metalSupplies[0]>= containersWanted*0.54):
        #for i in len(freeMannies):
    else:
        print("Not enough metals for an additional container. ")

    return
"""

# Splits up the wanted resources among the available mannies for mining. 
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

        resourcesToMine = amount/len(freeMannies)

        for i in range(len(freeMannies)):
            mannyTask = mineTaskJson(freeMannies[i], asteroidId, resource, resourcesToMine)
            tasks['tasks'].append(mannyTask)

    print(requests.post(mainUrl + "/api/probe/" + probeID + "/mannies/tasks", json=tasks, headers = authHeader))
    return

def availableMannies(probeID):
    freeMannys = []
    response = requests.get(mainUrl + '/api/probe/'+probeID + '/mannies', headers = authHeader)
    mannyInfo = response.json()
    numMannys = len(json.loads(json.dumps(mannyInfo))['mannies'])

    for i in range(numMannys):
        if mannyInfo['mannies'][i]['currentTask'] == None :
            freeMannys.append(mannyInfo['mannies'][i]['id'])

    return freeMannys

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