"""
This code gathers Earthquake events via an HTTP GET Request from BOTH USGS and EU
The returned results are processed by a JSON parser and 6 pertinent data items are extracted and returned.
Concept, Design by: Craig A. Lindley adapted to USGS by SpudGunMan see github
"""
import json
from operator import truediv
import requests

class EQEventGathererUSGS:

    def requestEQEvent(self):
        while True:
            r = requests.get('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson')
            if r.status_code == 200:
                break
            sleep(2)

        self.jsonData = json.loads(r.text)
        # Extracting all the important key features.
        self.jsonData = self.jsonData['features']

    def getEventID(self):
        return self.jsonData[0]['id']

    def getMag(self):
        mag = float(self.jsonData[0]['properties']['mag'])
        return float(("%.2f" % mag))

    def getLocation(self):
        place = self.jsonData[0]['properties']['place']
        # Since we are on a map remove the "xx km H of " from the start of the string and use best location name
        marker = " of "
        if marker in place:
            place = place.split(marker)
            return str(place[1])
        else:
            #print("Debug USGS Name Split Error: ",place)  #DEBUG 
            return str(place)
            
        
    def getAlert(self):
        return self.jsonData[0]['properties']['alert']

    def getTsunami(self):
        return self.jsonData[0]['properties']['tsunami']

    def getLon(self):
        lon = float(self.jsonData[0]['geometry']['coordinates'][0])
        return float(("%.2f" % lon))

    def getLat(self):
        lat = float(self.jsonData[0]['geometry']['coordinates'][1])
        return float(("%.2f" % lat))

    def getDepth(self):
        return float(self.jsonData[0]['geometry']['coordinates'][2])

class EQEventGathererEU:

    def requestEQEvent(self):
        while True:
            r = requests.get('https://www.seismicportal.eu/fdsnws/event/1/query?limit=1&format=json')
            if r.status_code == 200:
                break
            sleep(2)

        self.jsonData = json.loads(r.text)

    def getEventID(self):
        return self.jsonData['features'][0]['id']

    def getLon(self):
        lon = float(self.jsonData['features'][0]['properties']['lon'])
        return float(("%.2f" % lon))

    def getLat(self):
        lat = float(self.jsonData['features'][0]['properties']['lat'])
        return float(("%.2f" % lat))

    def getMag(self):
        return float(self.jsonData['features'][0]['properties']['mag'])

    def getDepth(self):
        return float(self.jsonData['features'][0]['properties']['depth'])

    def getLocation(self):
        return self.jsonData['features'][0]['properties']['flynn_region']

# Return a class instance
eqGathererEU = EQEventGathererEU()
eqGathererUSGS = EQEventGathererUSGS()

'''
# Test Code
eqGathererEU.requestEQEvent()
print(eqGathererEU.getEventID())
print(eqGathererEU.getLocation())
print(eqGathererEU.getMag())
print(eqGathererEU.getLon())
print(eqGathererEU.getLat())
print(eqGathererEU.getDepth())


eqGathererUSGS.requestEQEvent()
print(eqGathererUSGS.getEventID())
print(eqGathererUSGS.getLocation())
print(eqGathererUSGS.getMag())
print(eqGathererUSGS.getLon())
print(eqGathererUSGS.getLat())
print(eqGathererUSGS.getDepth())
print(eqGathererUSGS.getTsunami())
print(eqGathererUSGS.getAlert())
'''



