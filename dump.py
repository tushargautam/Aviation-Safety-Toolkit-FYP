import json
import requests

response = requests.get("https://public-api.adsbexchange.com/VirtualRadar/AircraftList.json")
data = json.loads(response.text)

counter=0
for i in range(0,len(data["acList"])):
    if "Lat" in data["acList"][i]:
        counter=counter+1;

print(counter)
print(len(data["acList"]))
faultyRecord=[]
for i in range(0,len(data["acList"])):
    try:
        if "Lat" in data["acList"][i] and "Alt" in data["acList"][i] and "Spd" in data["acList"][i] and "PosTime" in data["acList"][i] and "TrkH" in data["acList"][i] and "Vsi" in data["acList"][i] :
            print(i,data["acList"][i]["Icao"],"True")
            continue
        else:
            print(i,data["acList"][i]["Icao"],"FalseFalseFalse")
            faultyRecord.append(i);
    except:
            print(i)

for i in range(0, len(faultyRecord)):
    del data["acList"][faultyRecord[i]]
    faultyRecord[:] = [x - 1 for x in faultyRecord]

with open("data_file.json", "w") as write_file:
    json.dump(data["acList"], write_file)