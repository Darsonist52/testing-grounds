"""
Developed for https://neumann-probe.net/
Used as experiment into working with APIs
Developed by Darsonist52
"""

import requests
mainUrl = "https://neumann-probe.net/api"
print("Enter your API token:")
apiKey = input()

reponse = requests.get(mainUrl + "/version")
print(reponse.json())

reponse = requests.get(
	mainUrl + "/probes",
	headers={"Authorization": f"Bearer {apiKey}"},
)

data = reponse.json();

if reponse.status_code != 200 :
	print("Error: " + str(reponse.status_code))
else:
	print(f"Probe: {data['probes'][0]['name']}")

    
    