from DisplayManager import displayManager
from EQMap import BLACK
from EventDB import eventDB

#load DB
EQEventQueue = eventDB.load()
displayManager.displayMap()

# Repaint the map from the events in the DB
def repaintMap():

	# Display fresh map
	displayManager.displayMap()

#print event queue to map
for event in EQEventQueue:
    cqLon = event[0]
    cqLat = event[1]
    cqMag = event[2]
    cqTsunami = event[3]
    cqAlert = event[4]
    color = displayManager.colorFromMag(cqMag)
    displayManager.mapEarthquake(cqLon, cqLat, cqMag, color)


