"""
Earthquake Display Program
For the Raspberry Pi Model 3B and the official 7" display
Concept, Design by: Craig A. Lindley
"""

import time
from datetime import datetime
from DisplayManager import displayManager
from EQEventGatherer import eqGathererEU
from EQEventGatherer import eqGathererUSGS
from EventDB import eventDB

# Data Sourcing
use_eu = True
use_usgs = True

# Colors for display
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
YELLOW = (255, 255, 0)

# Acquire new EQ data every 15 seconds
ACQUISITION_TIME_MS = 15000

# Blink every .5 seconds
BLINK_TIME_MS = 500

# Title page display every 15 minutes
TITLEPAGE_DISPLAY_TIME_MS = 900000

# Times in the future for actions to occur
ftForAcquisition = 0
ftForBlink = 0
ftForTitlePageDisplay = 0

# Current quake data
cqID  = ""
cqIDUSGS = ""
cqLocation = "loading..."
cqLon = 0.0
cqLat = 0.0
cqMag = 0.0
cqDepth = 0.0
cqAlert = ""
cqTsunami = None
dataToggle = False
blinkToggle = False

# Return system millisecond count
def millis():
	return int(round(time.time() * 1000))

# Repaint the map from the events in the DB
def repaintMap():

	# Display fresh map
	displayManager.displayMap()

	# Display current local time
	displayManager.displayCurrentTime()

	# Display EQ location
	displayManager.displayEventLong(cqLocation, cqMag, cqDepth)

	# Display number of EQ events
	displayManager.displayNumberOfEvents(eventDB.numberOfEvents())

	# Display EQ depth
	displayManager.displayDBStats(cqMag, cqDepth, str(eventDB.getLargestEvent()))

	# Display all of the EQ events in the DB
	count = eventDB.numberOfEvents()
	if count > 0:
		for i in range(count):
			lon, lat, mag, alert, tsunami = eventDB.getEvent(i)

			# Color depends upon magnitude
			color = displayManager.colorFromMag(mag)
			displayManager.mapEarthquake(lon, lat, mag, color)
	return True

# Display title page and schedule next display event
def displayTitlePage():

	global ftForTitlePageDisplay

	# Display the title/ wash page
	displayManager.displayWashPage(str(eventDB.getLargestEvent()))

	# Schedule next title page display
	ftForTitlePageDisplay = millis() + TITLEPAGE_DISPLAY_TIME_MS

# Code execution start
def main():
	# Setup for global variable access
	global ftForAcquisition
	global ftForBlink
	global cqID
	global cqIDUSGS
	global cqLocation
	global cqLon
	global cqLat
	global cqMag
	global cqDepth
	global cqTsunami
	global cqAlert
	global blinkToggle
	global dataToggle

	ftForAcquisition = 0
	ftForBlink = 0

	dbCleared = False

	# True if display is on; false if off
	displayState = False

	#exit loop handler
	running = True

	# Handler for getting and writing new EQ events USCG
	def getUpdatesUSGS():
		global cqIDUSGS,cqLocation,cqLon,cqLat,cqMag,cqDepth,cqTsunami,cqAlert

		# internet check test
		try:
			# Check for new earthquake event
			eqGathererUSGS.requestEQEvent()
		except:
			pass
			
		# Determine if we have seen this event before If so ignore it
		if cqIDUSGS != eqGathererUSGS.getEventID():

			# Extract the EQ data
			cqLocation = eqGathererUSGS.getLocation()
			cqLon = eqGathererUSGS.getLon()
			cqLat = eqGathererUSGS.getLat()
			cqMag = eqGathererUSGS.getMag()
			cqDepth = eqGathererUSGS.getDepth()
			cqTsunami = eqGathererUSGS.getTsunami()
			cqAlert = eqGathererUSGS.getAlert()

			# Add new event to DB if it isnt also from the other source
			if not eventDB.checkDupLonLat(cqLon, cqLat):
				eventDB.addEvent(cqLon, cqLat, cqMag, cqTsunami, cqAlert)

				# Update the current event ID
				cqIDUSGS = eqGathererUSGS.getEventID()

				# Display the new EQ data
				repaintMap()
				return cqIDUSGS,cqLocation,cqLon,cqLat,cqMag,cqDepth,cqTsunami,cqAlert
		return False

	# Handler for getting and writing new EQ events EU
	def getUpdatesEU():
		global cqID,cqLocation,cqLon,cqLat,cqMag,cqDepth,cqTsunami,cqAlert

		# internet check test
		try:
			# Check for new earthquake event
			eqGathererEU.requestEQEvent()
		except:
			pass
			
		# Determine if we have seen this event before If so ignore it
		if cqID != eqGathererEU.getEventID():
			# Extract the EQ data
			cqLocation = eqGathererEU.getLocation()
			cqLon = eqGathererEU.getLon()
			cqLat = eqGathererEU.getLat()
			cqMag = eqGathererEU.getMag()
			cqDepth = eqGathererEU.getDepth()
			cqTsunami=0
			cqAlert=0

			# Add new event to DB if it isnt also from the other source
			if not eventDB.checkDupLonLat(cqLon, cqLat):
				eventDB.addEvent(cqLon, cqLat, cqMag, cqTsunami, cqAlert)

				# Update the current event ID
				cqID = eqGathererEU.getEventID()

				# Display the new EQ data
				repaintMap()
				return cqID,cqLocation,cqLon,cqLat,cqMag,cqDepth,cqTsunami,cqAlert
		return False

	#loop
	try:

		while running:
			
			# Get the current time
			now = datetime.now()

			# Reset the DB at 0:00 so display show EQs per day TODO settings menu
			# And we don't loose the EQ events
			if now.hour == 0 and dbCleared == False:
				eventDB.clear()
				dbCleared = True

			# Now check to see if the display should be off or on TODO settings menu
			if now.hour > 6 and now.hour < 22: 
				# Normal viewing hours have arrived TODO is this working?
				# If display is off, turn it on
				if displayState == False:
					displayManager.backlight(True)
					displayState = True
					dbCleared = False

					# Display the title page
					displayTitlePage()

					# Force a redisplay of all quake data
					repaintMap()
			else:
				# Normal viewing hours over. Turn the display off
				if displayState == True:
					# Turn the display off
					displayManager.backlight(False)
					displayState = False

			# Is it time to display the title page ?
			if millis() > ftForTitlePageDisplay:
				displayTitlePage()

				# Force a redisplay of all quake data
				repaintMap()

			# Is it time to acquire new earthquake data ?
			if millis() > ftForAcquisition:
				# Silly way to balance the server requests from EU and USGS
				if dataToggle:
					dataToggle = False
					if use_eu:
							getUpdatesEU()
					else:
							getUpdatesUSGS
				else:
					dataToggle = True
					if use_usgs:
							getUpdatesUSGS()
					else:
							getUpdatesEU()

				ftForAcquisition = millis() + ACQUISITION_TIME_MS

			# Is it time to blink EQ circle?
			if millis() > ftForBlink:

				if blinkToggle:
					color = displayManager.colorFromMag(cqMag)
					displayManager.mapEarthquake(cqLon, cqLat, cqMag, color)
					blinkToggle = False
				else:
					displayManager.mapEarthquake(cqLon, cqLat, cqMag, BLACK)
					blinkToggle = True
					# Update current display time on the off beat
					displayManager.displayCurrentTime()

				ftForBlink = millis() + BLINK_TIME_MS
	except KeyboardInterrupt:
		print("closing EQMap")
		

# Earthquake Map Program Entry Point
if __name__ == '__main__':
	main()
	

