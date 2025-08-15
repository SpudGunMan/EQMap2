"""
This code gathers Earthquake events via an HTTP GET Request from BOTH USGS and EU
The returned results are processed by a JSON parser and 6 pertinent data items are extracted and returned.
Concept, Design by: Craig A. Lindley adapted to USGS by SpudGunMan see github
"""
import json
from operator import truediv
import requests, time
from datetime import datetime, timedelta

class EQEventGathererUSGS:

	def requestEQEvent(self, days=0):
		while True:
			try:
				# API https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
				if days == 30:
					r = requests.get('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson', timeout=10)
				elif days == 7:
					r = requests.get('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson', timeout=10)
				elif days == 1:
					r = requests.get('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson', timeout=10)
				elif days == 0:
					r = requests.get('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson', timeout=10)

				# Check if the request was successful
				r.raise_for_status()

				# If successful, break the loop
				if r.status_code == 200:
					break
			except requests.exceptions.Timeout:
				#print("Request timed out. Retrying...")
				retrycount += 1
			except requests.exceptions.RequestException as e:
				#print(f"An error occurred: {e}. Retrying...")
				retrycount += 1
			except ValueError as ve:
				#print(f"Error: {ve}")
				retrycount += 1
			time.sleep(2)

		try:
			self.jsonData = r.json()
		except json.JSONDecodeError:
			#print("Failed to decode JSON response.")
			self.jsonData = []
			return False

		if not self.jsonData or 'features' not in self.jsonData:
			#print("No data found in the response.")
			self.jsonData = []
			return False

		# Extracting all the important key features.
		self.jsonData = self.jsonData['features']
		return days

	def getEventID(self):
		if not hasattr(self, 'jsonData') or self.jsonData is None:
			return None
		try:
			return self.jsonData[0]['id']
		except (IndexError, KeyError, TypeError):
			return None

	def getMag(self):
		self.mag = float(self.jsonData[0]['properties']['mag'])
		if self.mag is None: self.mag = 0
		return float(("%.2f" % self.mag))

	def getLocation(self):
		try:
			self.place = self.jsonData[0]['properties']['place']
		except:
			self.place = ""
		# Since we are on a map remove the "xx km H of " from the start of the string and use best location name
		self.marker = " of "
		if self.marker in self.place:
			self.place = self.place.split(self.marker)
			return str(self.place[1])
		else:
			#print("Debug USGS Name Split Error: ",place)  #DEBUG 
			return str(self.place)
			
	def getAlert(self):
		try:
			self.alert = self.jsonData[0]['properties']['alert']
			return self.alert
		except IndexError:
			return ""

	def getTsunami(self):
		try:
			self.tsunami = self.jsonData[0]['properties']['tsunami']
			return self.tsunami
		except IndexError:
			return ""

	def getLon(self):
		try:
			self.lon = float(self.jsonData[0]['geometry']['coordinates'][0])
			return float(("%.2f" % self.lon))
		except IndexError:
			return ""

	def getLat(self):
		try:
			self.lat = float(self.jsonData[0]['geometry']['coordinates'][1])
			return float(("%.2f" % self.lat))
		except IndexError:
			return ""

	def getDepth(self):
		try:
			return float(self.jsonData[0]['geometry']['coordinates'][2])
		except IndexError:
			return ""

class EQEventGathererEU:

	def requestEQEvent(self, limit=1, days=0):
		currentRTC = datetime.now()

		if days > 1:
			startAdjusted = datetime.today() - timedelta(days=days)
			startQuery = startAdjusted.strftime("%Y-%m-%dT00:00:00") #https://strftime.org
			endQuery = currentRTC.strftime("%Y-%m-%dT23:59:59")
			start=startQuery
			end=endQuery
			requestTime = '&start=' + start + '&end=' + end
			print(requestTime)
		
		if days == 1:
			startQuery = currentRTC.strftime("%Y-%m-%dT00:00:00") #https://strftime.org
			endQuery = currentRTC.strftime("%Y-%m-%dT23:59:59")
			start=startQuery
			end=endQuery
			requestTime = '&start=' + start + '&end=' + end

		if days == 0:
			start=''
			end=''
			requestTime = ''

		while True:
			try:
				self.r = requests.get(
					'https://www.seismicportal.eu/fdsnws/event/1/query?limit=' + str(limit) + requestTime + '&format=json',
					timeout=10  # Set a timeout to avoid hanging indefinitely
				)
				self.r.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
				break  # Exit the loop if the request is successful
			except requests.exceptions.Timeout:
				#print("Request timed out. Retrying...")
				retrycount += 1
			except requests.exceptions.RequestException as e:
				#print(f"An error occurred: {e}. Retrying...")
				retrycount += 1
			time.sleep(2)

		try:
			self.jsonData = self.r.json()  # Use the built-in JSON parser for better error handling
		except json.JSONDecodeError:
			print("Failed to decode JSON response.")
			self.jsonData = None

		try:
			self.jsonData = json.loads(self.r.text)
		except:
			self.jsonData = None
		return days

	def getEventID(self):
		if not hasattr(self, 'jsonData') or self.jsonData is None:
			return None
		try:
			return self.jsonData['features'][0]['id']
		except (IndexError, KeyError, TypeError):
			return None

	def getLon(self):
		if not hasattr(self, 'jsonData') or self.jsonData is None:
			return ""
		try:
			self.lon = float(self.jsonData['features'][0]['properties']['lon'])
			return float(("%.2f" % self.lon))
		except (IndexError, KeyError, TypeError, ValueError):
			return ""

	def getLat(self):
		try:
			lat = float(self.jsonData['features'][0]['properties']['lat'])
			return float(("%.2f" % lat))
		except IndexError:
			return ""

	def getMag(self):
		try:
			return float(self.jsonData['features'][0]['properties']['mag'])
		except IndexError:
			return ""

	def getDepth(self):
		try:
			return float(self.jsonData['features'][0]['properties']['depth'])
		except IndexError:
			return ""

	def getLocation(self):
		if not hasattr(self, 'jsonData') or self.jsonData is None:
			return ""
		try:
			return self.jsonData['features'][0]['properties']['flynn_region']
		except (IndexError, KeyError, TypeError):
			return ""
				
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

