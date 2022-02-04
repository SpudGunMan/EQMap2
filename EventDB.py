"""
This code handles a simple database of earthquake events in a list
Concept, Design and Implementation by: Craig A. Lindley
"""
from collections import deque

#MAX_EVENTS = 200

class EventDB:

	# Class Constructor
	def __init__(self):
		# Create empty queue
		#self.EQEventQueue = deque(maxlen=MAX_EVENTS)
		self.EQEventQueue = deque()
		self.EQEventQueue.clear()

	# Clear the database of events
	def clear(self):
		self.EQEventQueue.clear()

	# Add an earthquake event
	def addEvent(self, lon, lat, mag, alert=0, tsunami=0):
		self.EQEventQueue.appendleft((lon, lat, mag, alert, tsunami))

	# Return the number of entries
	def numberOfEvents(self):
		return len(self.EQEventQueue)

	def showEvents(self):
		print("Number of entries: ", len(self.EQEventQueue))
		print(self.EQEventQueue)
		print("\n")

	# Retrieve an event by index
	def getEvent(self, index):
		return self.EQEventQueue[index]

	# Retrieve largest event
	def getLargestEvent(self):
		EQlargest = [] #list for mag of events in EventQ
		max_value = 0
		max_index = 0
		
		for event in self.EQEventQueue:
			EQlargest.append(event[2])
			max_value = max(EQlargest)
			
		return max_value

	# Guess if event is duplicated with lat,lon dups
	def checkDupLonLat(self, lon, lat):
		if self.EQEventQueue:
			last_event = self.EQEventQueue[0]
			if str(lon) in str(last_event[0]):
				if str(lat) in str(last_event[1]):
					return True
			# Data is not a duplicate
			return False

# Create instance of database
eventDB = EventDB()

'''
# Test Code
eventDB.showEvents()

eventDB.addEvent(1, 2, 3)
eventDB.showEvents()

eventDB.addEvent(4, 5, 6)
eventDB.showEvents()
eventDB.addEvent(7, 8, 9)
eventDB.showEvents()
eventDB.addEvent(10, 11, 12)
eventDB.showEvents()
eventDB.addEvent(13, 14, 15)
eventDB.showEvents()
eventDB.addEvent(16, 17, 18)
eventDB.showEvents()
eventDB.addEvent(19, 20, 21)
eventDB.showEvents()
eventDB.addEvent(22, 23, 24)
eventDB.showEvents()
eventDB.addEvent(25, 26, 27)
eventDB.showEvents()
eventDB.addEvent(28, 29, 30)
eventDB.showEvents()
eventDB.addEvent(31, 32, 33)
eventDB.showEvents()

print(eventDB.getEvent(3))

lon, lat, mag, alert, tsunami = eventDB.getEvent(3)
print("lon: ", lon, "lat: ", lat, "mag: ", mag, alert, tsunami)

print(eventDB.numberOfEvents())

print(eventDB.getLargestEvent())

print(eventDB.checkDupLonLat(31, 32))

'''