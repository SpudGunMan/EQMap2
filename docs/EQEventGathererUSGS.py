"""
This code gathers Earthquake events via an HTTP GET Request from USGS
The returned results are processed by a JSON parser and 6 pertinent data items are extracted and returned.
Concept, Design by: Craig A. Lindley adapted to USGS by SpudGunMan see github
"""
import json
from operator import truediv
import requests

class EQEventGatherer:

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
        return float(self.jsonData[0]['properties']['mag'])

    def getLocation(self):
        place = self.jsonData[0]['properties']['place']
        # Since we are on a map rempve the "xx km H of " from the start of the string and use best location name
        place = place.split("of ") 
        return place[1]
        
    def getAlert(self):
        return self.jsonData[0]['properties']['alert']

    def getTsunami(self):
        return self.jsonData[0]['properties']['tsunami']

    def getLon(self):
        return float(self.jsonData[0]['geometry']['coordinates'][0])

    def getLat(self):
        return float(self.jsonData[0]['geometry']['coordinates'][1])

    def getDepth(self):
        return float(self.jsonData[0]['geometry']['coordinates'][2])

# Return a class instance
eqGatherer = EQEventGatherer()

'''
# Test Code
eqGatherer.requestEQEvent()
print(eqGatherer.getEventID())
print(eqGatherer.getLocation())
print(eqGatherer.getMag())
print(eqGatherer.getTsunami())
print(eqGatherer.getAlert())
print(eqGatherer.getLon())
print(eqGatherer.getLat())
print(eqGatherer.getDepth())
'''





