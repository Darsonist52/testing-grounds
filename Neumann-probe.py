"""
Developed for https://neumann-probe.net/
Used as experiment into working with APIs
Developed by Darsonist52
"""
#Variables and shit
import requests
import json
mainUrl = "https://neumann-probe.net/api"

apiKey = "vng_IawfKYT7D_ZPyfnWwc1tf5xoPHB4iGCIt8q6b8XPmvo"

#Get default probe and print out probe ID
response = requests.get(
	mainUrl + "/probes",
	headers={"Authorization": f"Bearer {apiKey}"}
)
data = response.json();

if response.status_code != 200 :
	print("Error: " + str(reponse.status_code))
else:
	probeID = str(data['probes'][0]['id'])
	print("Main probe ID: " + probeID)

#Get storage containers for probe
response = requests.get(
mainUrl + "/probe/" + probeID + "/storage-containers",
	headers={"Authorization": f"Bearer {apiKey}"}
)
data = response.json()
numContainers = len(json.loads(json.dumps(data))['containers'])
print("You have a total of " + str(numContainers) + " storage containers.")

# Traverse through the storage containers and add free capacity
totalFreeSpace = 0
totalMetal = 0
totalCarbon = 0
totalIce = 0
for i in range(numContainers):
	totalFreeSpace += data['containers'][i]['freeCapacity']
	containerID = str(data['containers'][i]['id'])
	containerInfo = requests.get(
		mainUrl + "/probe/" + probeID + "/storage-containers/" + containerID,
		headers={"Authorization": f"Bearer {apiKey}"}
	)
	containerData = containerInfo.json()
	numContainers = len(json.loads(json.dumps(containerData))['inventory']['resourceStocks'])
	for i in range(numContainers):
		if(containerData['inventory']['resourceStocks'][i]['type'] == "metals"):
			totalMetal += containerData['inventory']['resourceStocks'][i]['amount']
	for i in range(numContainers):
		if(containerData['inventory']['resourceStocks'][i]['type'] == "ice"):
			totalIce += containerData['inventory']['resourceStocks'][i]['amount']		
	for i in range(numContainers):
		if(containerData['inventory']['resourceStocks'][i]['type'] == "organic_compounds"):
			totalCarbon += containerData['inventory']['resourceStocks'][i]['amount']


print(str(totalMetal) + " metals in total.")
print(str(totalIce) + " ice in total.")
print(str(totalCarbon) + " carbon compounds in total.")
print("Probe " + probeID + " has " + str(totalFreeSpace) + " free capacity in total.")