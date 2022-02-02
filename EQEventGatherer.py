"""
This code gathers Earthquake events via an HTTP GET Request
The returned results are processed by a JSON parser and 6 pertinent data items are extracted and returned.

Concept, Design and Implementation by: Craig A. Lindley
"""
import json
import requests

class EQEventGatherer:

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
		return float(self.jsonData['features'][0]['properties']['lon'])

	def getLat(self):
		return float(self.jsonData['features'][0]['properties']['lat'])

	def getMag(self):
		return float(self.jsonData['features'][0]['properties']['mag'])

	def getDepth(self):
		return float(self.jsonData['features'][0]['properties']['depth'])

	def getLocation(self):
		return self.jsonData['features'][0]['properties']['flynn_region']

# Return a class instance
eqGatherer = EQEventGatherer()

"""
# Test Code

eqGatherer.requestEQEvent()
print(eqGatherer.getEventID())
print(eqGatherer.getLon())
print(eqGatherer.getLat())
print(eqGatherer.getMag())
print(eqGatherer.getDepth())
print(eqGatherer.getLocation())
"""



