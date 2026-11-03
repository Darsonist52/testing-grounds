"""
Developed for https://neumann-probe.net/
Directory for Neumann-script.py
"""
# Import libraries
import requests
import json

# Main URL, API key, and API get / post auth header
mainUrl = "https://neumann-probe.net"
apiKey = "vng_Y13DbU-0EccDc-7Q8pgLSdq8esyMWRRkQxGYJ1tt_Rs"
authHeader = {
    "Authorization": f"Bearer {apiKey}"
}

# File variables
metalSupplies = ['A']
carbonSupplies = ['A']
iceSupplies = ['A']

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

# Returns total used and free space, as well as total storage for a given probe. 1 API request
def getFreeSpace(probeID):
    # Declare func variables
    totalFreeSpace = 0
    totalUsedSpace = 0
    # Request from API for list of containers
    response = requests.get( mainUrl + "/api/probe/" + probeID + "/storage-containers", headers=authHeader)
    containerList = response.json()
    
    # Find num of containers
    numContainers = len(json.loads(json.dumps(containerList))['containers'])

    # For each container, add up free sapce and used space.
    for i in range(numContainers):
        totalFreeSpace += containerList['containers'][i]['freeCapacity']
        totalUsedSpace += containerList['containers'][i]['usedCapacity']

    # Print amount of space used out of total number of containers
    print("For probe " + probeID + " you have used " + str(totalUsedSpace) + " ECE out of " + str(totalFreeSpace + totalUsedSpace) +" ECE, which leaves " + str(totalFreeSpace) + " ECE free for use.")
    return totalFreeSpace

# Returns total amount of metal in given probe. 1 + num containers API requests
def getProbeMetal(probeID):
    totalMetal = 0
    # Request from API for list of containers
    response = requests.get( mainUrl + "/api/probe/" + probeID + "/storage-containers", headers=authHeader)
    containerList = response.json()
    
    # Find num of containers
    numContainers = len(json.loads(json.dumps(containerList))['containers'])

    # Add up metal from each container
    for i in range(numContainers):
        # Find each container ID
        containerID = containerList['containers'][i]['id']
        
        # Get each containers information from api
        response = requests.get(mainUrl + "/api/probe/" + probeID + "/storage-containers/" + containerID, headers=authHeader)
        containerData = response.json()

        # Get each containers number of resources
        numResources = len(json.loads(json.dumps(containerData))['inventory']['resourceStocks'])
        for j in range(numResources):    
            if(containerData['inventory']['resourceStocks'][j]['type'] == "metals"):
                totalMetal += containerData['inventory']['resourceStocks'][j]['amount']	

    # Print amount of metal in probe
    print("For probe " + probeID + " you have " + str(totalMetal) + " ECE of metals in storage.")
    
    # Updates cache and prevents the death of nick
    metalSupplies.pop(0)
    metalSupplies.append(totalMetal)
    return totalMetal

# Returns the total amount of carbon compounds in the specified probe. 1 + num of containers on specified probe API requests
def getProbeCarbonCompounds(probeID):
    totalCarbonCompounds = 0
    
    # Request from API for list of containers
    response = requests.get( mainUrl + "/api/probe/" + probeID + "/storage-containers", headers=authHeader)
    containerList = response.json()
        
    # Find num of containers
    numContainers = len(json.loads(json.dumps(containerList))['containers'])

    # Add up number of carbon compounds in each container
    for i in range(numContainers):
            # Find each container ID
            containerID = containerList['containers'][i]['id']
            
            # Get each containers information from api
            response = requests.get(mainUrl + "/api/probe/" + probeID + "/storage-containers/" + containerID, headers=authHeader)
            containerData = response.json()
            
            # Get each containers number of resources
            numResources = len(json.loads(json.dumps(containerData))['inventory']['resourceStocks'])
            for j in range(numResources):    
                if(containerData['inventory']['resourceStocks'][j]['type'] == "carbon_compounds"):
                    totalCarbonCompounds += containerData['inventory']['resourceStocks'][j]['amount']

    # Prints the number of Carbon Compounds in the probe
    print("For probe " + probeID + " you have " + str(totalCarbonCompounds) + " ECE of carbon compounds in storage.") 
    
    # Updates cache and prevents the death of nick
    carbonSupplies.pop(0)
    carbonSupplies.append(totalCarbonCompounds)
    return(totalCarbonCompounds)

# Returns the total amount of ice in the specified probe. 1 + num of containers on specified probe API requests
def getProbeIce(probeID):
    totalIce = 0
    
    # Request from API for list of containers
    response = requests.get( mainUrl + "/api/probe/" + probeID + "/storage-containers", headers=authHeader)
    containerList = response.json()
        
    # Find num of containers
    numContainers = len(json.loads(json.dumps(containerList))['containers'])

    # Add up number of ice in each container
    for i in range(numContainers):
            # Find each container ID
            containerID = containerList['containers'][i]['id']
            
            # Get each containers information from api
            response = requests.get(mainUrl + "/api/probe/" + probeID + "/storage-containers/" + containerID, headers=authHeader)
            containerData = response.json()
            
            # Get each containers number of resources
            numResources = len(json.loads(json.dumps(containerData))['inventory']['resourceStocks'])
            for j in range(numResources):    
                if(containerData['inventory']['resourceStocks'][j]['type'] == "ice"):
                    totalIce += containerData['inventory']['resourceStocks'][j]['amount']

    # Prints the number of ice in the probe
    print("For probe " + probeID + " you have " + str(totalIce) + " ECE of ice in storage.") 
    
    # Updates cache and prevents the death of nick
    iceSupplies.pop(0)
    iceSupplies.append(totalIce)
    return(totalIce)

# You guessed it, makes a container
def makeContainer(probeID, numConReq):

    return

# Splits up the wanted resources among the available mannies for mining. 
def delegateMining(probeID):
    # Get info on current sector
    response = requests.get(mainUrl + '/api/probe/'+probeID + '/sector', headers = authHeader)
    sectorInfo = response.json()
    
    # Find the number of minable objects in the probe's current sector.
    numMinables = len(json.loads(json.dumps(sectorInfo))['sector']['objects'][0]['minableTargets'])
    
    return