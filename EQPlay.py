from DisplayManager import displayManager
from EQMap import BLACK
from EventDB import eventDB
from time import sleep
EQEventQueue = []


displayManager.displayMap()
displayManager.drawRightJustifiedText(500, "database player")
sleep(2)

def displayDatabase(day):

	# Repaint the map from the events in the DB
	displayManager.displayMap()

	# load DB event que
	EQEventQueue, filecount = eventDB.load(day)
	# event count
	eventcount = len(EQEventQueue)

	#print event queue to map
	for event in EQEventQueue:
		cqLon = event[0]
		cqLat = event[1]
		cqMag = event[2]
		cqTsunami = event[3]
		cqAlert = event[4]
		color = displayManager.colorFromMag(cqMag)
		displayManager.mapEarthquake(cqLon, cqLat, cqMag, color)

	return eventcount

def main():
	lastevents = 0
	updateMap = True
	EQEventQueue, filecount = eventDB.load() #grab filecount
	try:
		while updateMap:
			for day in range(filecount):
				#displayManager.displayMap()
				events = displayDatabase(day)
				if events > lastevents: trend = "up"
				if events < lastevents: trend = "down"
				lastevents = events
				displayManager.drawRightJustifiedText(100, "db: " + str(day) + " Events:" + str(events) + " Trending " + trend)
				displayManager.handleKeyPress()
				sleep(5)

	except KeyboardInterrupt:
		pass


if __name__ == '__main__':
	main()

