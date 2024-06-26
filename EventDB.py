"""
This code handles a simple database of earthquake events in a list
Concept, Design and Implementation by: Craig A. Lindley
"""
from collections import deque, Counter
from datetime import datetime
import pickle
import glob

#MAX_EVENTS = 200

class EventDB:

	# Class Constructor
	def __init__(self):
		# Create empty queue
		#self.EQEventQueue = deque(maxlen=MAX_EVENTS)
		self.EQEventQueue = deque()
		self.EQElocations = deque()
		self.dailyevents = []
		self.mySettings = []
		self.EQEventQueue.clear()

	# Clear the database of events /save a copy
	def clear(self):
		self.EQEventQueue.clear()
		return True

	# Add an earthquake event
	def addEvent(self, lon, lat, mag, alert, tsunami, location):
		self.EQEventQueue.appendleft((lon, lat, mag, alert, tsunami, location))
		self.EQElocations.append(location)

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

	# Retreve the last day event count
	def getDayTrend(self):
		try:
			return self.dailyevents[-1]
		except:
			return "no data"

	# Retrieve largest event related data
	def getLargestEvent(self):
		EQlargest = deque()
		max_value = 0
		max_location = ''
		eventTrend = ''
		#spin off a table of the events and find the max
		for event in self.EQEventQueue:
			EQlargest.append(event[2])
			max_value = max(EQlargest).real

		#find max item name
		for event in self.EQEventQueue:
			if event[2] >= max_value:
				max_location = event[5]


		#trending - this is dumb not sure its usefull?
		try:
			if EQlargest[1]:
				if EQlargest[0] > EQlargest[1]:
					eventTrend = " mag. increasing"
				elif EQlargest[0] < EQlargest[1]:
					eventTrend = " mag. decreasing"
				else:
					eventTrend = ''		
		except:
				eventTrend = ''

		return (max_value, eventTrend, max_location)

	# Report the most active region since last poll
	def getActiveRegion(self,preserve=False):
		self.region = ''

		self.region_dict = Counter(self.EQElocations)
		self.region = self.region_dict.most_common(1)

		if preserve == False:self.EQElocations = [] # clear this table so its not out of control, USGS recall can get it by the hour

		if self.region:
			self.region = self.region[(0)]
			self.region = self.region[0]
		else:
			pass

		return self.region #returns the first in list

	# Guess if event is duplicated with lat,lon dups
	def checkDupLonLat(self, lon, lat):
		if self.EQEventQueue:
			self.last_event = self.EQEventQueue[0]
			if str(lon) in str(self.last_event[0]):
				if str(lat) in str(self.last_event[1]):
					#data is a dupe
					return True

			# Data is not a duplicate
			return False

	# for the future use of day to day trending graph?
	def getTrend(self):
		return self.getTrend 

	# Save the settings local path
	def saveSettings(self):
		self.dbFileName = "EQMsettings.dat"
		self.dbFile = open(self.dbFileName, "wb")
		pickle.dump(self.mySettings, self.dbFile)
		self.dbFile.close()
		return self.mySettings

	# Load the settings local path
	def loadSettings(self):
		self.dbFileName = "EQMsettings.dat"
		self.dbFile = open(self.dbFileName, "wb")
		self.mySettings = pickle.load(self.dbFile)
		self.dbFile.close()
		return self.mySettings

	# Save the database to local path by default at 0:00
	def save(self):
		#this only works with default save of once a day - daily event trending
		try:
			if len(self.EQEventQueue) > 0:
				self.dailyevents.append(len(self.EQEventQueue))
		except:
			self.dailyevents.append(0)

		# save
		currentRTC = datetime.now()
		eventLogTime = currentRTC.strftime("%Y%m%d") #https://strftime.org

		try:
			self.dbFileName = "/run/shm/" + "EQMdatabase" + eventLogTime + ".dat"
			self.dbFile = open(self.dbFileName, "wb")
		except:
			self.dbFileName = "EQMdatabase" + eventLogTime + ".dat"
			self.dbFile = open(self.dbFileName, "wb")

		pickle.dump(self.EQEventQueue, self.dbFile)
		self.dbFile.close()
		return True

	def load(self, file=0):
		# Load file from database dump file
		self.EQEventQueue.clear()
		filenames = []
		# Try is for raspberryOS ramdisk use
		# then look for files, and load the filename list aka file per day
		# file variable will load a different day in the list
		try:
			path = "/run/shm/EQMdatabase*.dat"
			filenames = sorted(glob.glob(path))
			filename = (filenames[file])
			print("DB:", file, filename)
			self.dbFile = open(filename, "rb")
		except:
			try:
				path = "EQMdatabase*.dat"
				filenames = sorted(glob.glob(path))
				filename = (filenames[file])
				print("DB:", file, filename)
				self.dbFile = open(filename, "rb")
			except:
				path = "eqmap-demo-dat.demo"
				filenames = sorted(glob.glob(path))
				filename = (filenames[file])
				print("DB:", file, filename)
				self.dbFile = open(filename, "rb")

		self.EQEventQueue = pickle.load(self.dbFile)
		self.dbFile.close()
		return self.EQEventQueue, len(filenames)

# Create instance of database
eventDB = EventDB()
'''
# Test Code
eventDB.showEvents()

eventDB.addEvent(1, 2, 3, 1, 0, "frst")
eventDB.showEvents()

eventDB.addEvent(4, 5, 6, 2, 0, "london")
eventDB.showEvents()
eventDB.addEvent(7, 8, 9, 3, 0, "france")
eventDB.showEvents()
eventDB.addEvent(10, 11, 12, 4, 0, "seattle")
eventDB.showEvents()
eventDB.addEvent(13, 14, 15, 5, 0, "alaska")
eventDB.showEvents()
eventDB.addEvent(16, 17, 18, 6, 0, "chicago")
eventDB.showEvents()
eventDB.addEvent(19, 20, 21, 7, 1, "alaska")
eventDB.showEvents()
eventDB.addEvent(22, 23, 99, 8, 0, "alaska")
eventDB.showEvents()
eventDB.addEvent(25, 26, 27, 2, 0, "denver")
eventDB.showEvents()
eventDB.addEvent(28, 29, 33, 3, 0, "lodon")
eventDB.showEvents()
eventDB.addEvent(31, 32, 34, 3, 0, "last")
eventDB.showEvents()

print("event 3 ", eventDB.getEvent(3))

lon, lat, mag, alert, tsunami = eventDB.getEvent(3)
print("lon: ", lon, "lat: ", lat, "mag: ", mag, "alert: ", alert, "tsunami: ", tsunami)

print("number of events", eventDB.numberOfEvents())

print("largest event", eventDB.getLargestEvent())

print("dupe check", eventDB.checkDupLonLat(32, 32))


print("saved", eventDB.save())

print("cleared", eventDB.clear())

eventDB.load()

print("number of events", eventDB.numberOfEvents())

print("largest event", eventDB.getLargestEvent())

print("active region", eventDB.getActiveRegion())

print("trend ", eventDB.getDayTrend())
'''

