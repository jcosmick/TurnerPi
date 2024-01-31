import json

appDataFileName = 'appData.json'

def createAppDataFile(data_to_write = {"isPinging": False,"isOn": False, "isTimeout": False}):
    with open(appDataFileName, 'w') as file:
        json.dump(data_to_write, file, indent=2)

def loadAppData():
    with open(appDataFileName , 'r') as f:
        return json.load(f)

def isPinging(): 
    with open(appDataFileName , 'r') as f:
        return json.load(f)["isPinging"]
    
def isOn():
    with open(appDataFileName , 'r') as f:
        return json.load(f)["isOn"]

def changeIsPinging(var):
    with open(appDataFileName, 'r') as file:
        data = json.load(file)
    data["isPinging"] = var
    print(str(data))
    with open(appDataFileName, 'w') as file:
        json.dump(data, file, indent=1)

def changeIsTimeout(var):
    with open(appDataFileName, 'r') as file:
        data = json.load(file)
    data["isTimeout"] = var
    print(str(data))
    with open(appDataFileName, 'w') as file:
        json.dump(data, file, indent=1)

def changeIsOn(var):
    with open(appDataFileName, 'r') as file:
        data = json.load(file)
    data["isOn"] = var
    print(str(data))
    with open(appDataFileName, 'w') as file:
        json.dump(data, file, indent=2)