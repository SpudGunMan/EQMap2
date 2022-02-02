"""
Earthquake Display Program
For the Raspberry Pi Model 3B and the official 7" display
Concept, Design and Implementation by: Craig A. Lindley
"""

import time
from datetime import datetime
from DisplayManager import displayManager
from EQEventGatherer import eqGatherer
from EventDB import eventDB

# Colors for display
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
YELLOW = (255, 255, 0)

# Acquire new EQ data every 30 seconds
ACQUISITION_TIME_MS = 30000

# Blink every .5 seconds
BLINK_TIME_MS = 500

# Title page display every 15 minutes
TITLEPAGE_DISPLAY_TIME_MS = 900000

# Times in the future for actions to occur
ftForAcquisition = 0
ftForBlink = 0
ftForTitlePageDisplay = 0

# Current quake data
cqID  = "27"
cqLocation = "loading..."
cqLon = 0.0
cqLat = 0.0
cqMag = 0.0
cqDepth = 0.0

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

	# Display EQ magnitude
	#displayManager.displayMagnitude(cqMag)
	#replaced with below displayDBStats

	# Display EQ location
	#displayManager.displayLocation(cqLocation, cqMag)
	displayManager.displayEventLong(cqLocation, cqMag, cqDepth)

	# Display number of EQ events
	displayManager.displayNumberOfEvents(eventDB.numberOfEvents())

	# Display EQ depth
	#displayManager.displayDepth(cqDepth)
	displayManager.displayDBStats(cqMag, cqDepth, str(eventDB.getLargestEvent()))

	# Display all of the EQ events in the DB
	count = eventDB.numberOfEvents()
	for i in range(count):
		lon, lat, mag = eventDB.getEvent(i)

		# Color depends upon magnitude
		color = displayManager.colorFromMag(mag)
		displayManager.mapEarthquake(lon, lat, mag, color)

# Display title page and schedule next display event
def displayTitlePage():

	global ftForTitlePageDisplay

	# Display the title page
	displayManager.displayTitlePage()

	# Schedule next title page display
	ftForTitlePageDisplay = millis() + TITLEPAGE_DISPLAY_TIME_MS

# Code execution start
def main():
	# Setup for global variable access
	global ftForAcquisition
	global ftForBlink
	global cqID
	global cqLocation
	global cqLon
	global cqLat
	global cqMag
	global cqDepth
	global blinkToggle

	ftForAcquisition = 0
	ftForBlink = 0

	dbCleared = False

	# True if display is on; false if off
	displayState = False

	#exit loop handler
	running = True


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
				# Check for new earthquake event
				eqGatherer.requestEQEvent()

				# Determine if we have seen this event before
				# If so ignor it
				if cqID != eqGatherer.getEventID():
					#print("New Event")
					# Extract the EQ data
					cqLocation = eqGatherer.getLocation()
					cqLon = eqGatherer.getLon()
					cqLat = eqGatherer.getLat()
					cqMag = eqGatherer.getMag()
					cqDepth = eqGatherer.getDepth()

					# Add new event to DB
					eventDB.addEvent(cqLon, cqLat, cqMag)

					# Update the current event ID
					cqID = eqGatherer.getEventID()

					# Display the new EQ data
					repaintMap()

				ftForAcquisition = millis() + ACQUISITION_TIME_MS

			# Is it time to blink ?
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
	

