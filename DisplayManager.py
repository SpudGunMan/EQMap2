"""
This code handles display by writing directly to the framebuffer in pygame
Concept, Design by: Craig A. Lindley
"""

from cProfile import run
import os, time, sys
from datetime import datetime

from EventDB import EventDB
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # hide pygame prompt message
import pygame, pygame.freetype
from pygame.locals import *

class DisplayManager:

	# Class constructor
	def __init__(self):
		self.fontSize = 40
		self.dist = "m" # or k miles/kilo
		self.time24h = False
		self.firstRun = True
		self.textColor = (255, 255, 255)
		self.black  = (0, 0, 0)
		self.white  = (255, 255, 255)
		self.red    = (255, 0, 0)
		self.yellow = (255, 255, 0)
		self.green  = (0, 255, 0)
		self.blue  = (0, 0, 255)
		self.eventTimeString = "loading..."
		self.eventTimeStringLong = self.eventTimeString
		self.topTextRow = 0
		self.eventsTextRow = 0
		self.bottomTextRow = 0
		self.eventCount = 0

		print("DisplayManager: Initializing...")
		try:
			pygame.init()
		except Exception as e:
			print(f"Error initializing pygame: {e}")
			sys.exit(1)

		try:
			# Set the display mode to fullscreen
			#set monitor to use
			self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
			self.displayInfo = pygame.display.Info()
			self.screenWidth  = self.displayInfo.current_w
			self.screenHeight = self.displayInfo.current_h
			print("DisplayManager: Screen size: " + str(self.screenWidth) + "x" + str(self.screenHeight))
			pygame.mouse.set_visible(0)

			# Read the map into memory
			self.mapImage = pygame.image.load('maps/eqm800_shaded.bmp')
			if self.screenWidth > 1000:
				self.mapImage = pygame.transform.scale(self.mapImage, (1024, 516))

			# Get its bounding box
			self.mapImageRect = self.mapImage.get_rect()

			# Center map 
			self.mapImageRect.y = (pygame.display.get_surface().get_height() - self.mapImageRect.height) / 2
			self.mapImageRect.x = (pygame.display.get_surface().get_width() - self.mapImageRect.width) / 2

			# Set the uypper and lower text areas
			self.topTextRow = self.mapImageRect.y - 25
			self.bottomTextRow = (self.mapImageRect.y + self.mapImageRect.height) + 5
			self.eventsTextRow = self.bottomTextRow - 30

			# Setup inital font of initial size
			self.font = pygame.freetype.Font('fonts/Sony.ttf', self.fontSize) #legacy pygame > v2.0
			#self.font = pygame.font.SysFont('arial',self.fontSize)
			self.hasGUI = True
		
		except:
			#command line settings for display to console display
			self.screenWidth = -1
			self.screenHeight = -1
			self.screen = (-1, -1)
			self.mapImageRect = (-1, -1, -1, -1)
			self.hasGUI = False

	# Clear the screen
	def clearScreen(self):
		try:
			self.screen.fill(self.black)
			pygame.display.flip()
			return True
		except:
			return False

	# Backlight control
	def backlight(self, b):
		if b:
			# Turn backlight on
			return True
		else:
			# Turn backlight off
			return False

	# Return color from magnitude
	def colorFromMag(self, mag):
		# input is a float, convert to color
		try:
			imag = int(mag + 0.5)

			if imag < 1:
				imag = 1.0
		except:
			# if not a number, return value as red for now
			imag = 1.0
			mag = 1.0
		
		case = {
		1: self.green,
		2: self.green,
		3: self.green,
		4: self.yellow,
		5: self.yellow,
		6: self.yellow,
		7: self.red,
		8: self.red,
		9: self.red
		}

		return case.get(imag)

	# Display the map
	def displayMap(self):
		try:
			self.clearScreen()
			self.screen.blit(self.mapImage, self.mapImageRect)
			pygame.display.flip()
			return True
		except:
			return False

	# Draw text
	def drawText(self, x, y, text):
		try:
			self.font.render_to(self.screen, (x, y), text, self.textColor)
			pygame.display.flip()
			return True
		except:
			print(text)
			return False

	# Draw centered text
	def drawCenteredText(self, y, text):
		try:
			textSurface, rect = self.font.render(text, self.textColor)
			x = (self.screenWidth - rect.width) / 2
			self.font.render_to(self.screen, (x, y), text, self.textColor)
			pygame.display.flip()
			return True
		except:
			print(text)
			return False

	# Draw right justified text
	def drawRightJustifiedText(self, y, text):
		try:
			textSurface, rect = self.font.render(text, self.textColor)
			x = (self.mapImageRect.x + self.mapImageRect.width) - rect.width - 2
			self.font.render_to(self.screen, (x, y), text, self.textColor)
			pygame.display.flip()
			return True
		except:
			print(text)
			return False

	# Set text size
	def setTextSize(self, size):
		self.fontSize = size
		self.font = pygame.freetype.Font('fonts/Sony.ttf', self.fontSize) #legacy pygame > v2.0
		#self.font = pygame.font.SysFont('arial',self.fontSize)

	# Set text color
	def setTextColor(self, color):
		self.textColor = color

	# Draw a circle on the scrren
	def drawCircle(self, x, y, radius, color):
		try:
			pygame.draw.circle(self.screen, color, (int(x), int(y)), int(radius), 2)
			pygame.display.flip()
			return True
		except:
			return False

	# Draw a circle with size based on mag at lon, lat position on map
	def mapEarthquake(self, lon, lat, mag, color):
		
		if self.hasGUI and lon != '':
			# Calculate map X and Y
			mapX = ((float(lon) + 180.0) * self.mapImageRect.width) / 360.0 + self.mapImageRect.x
			mapY = ((((-1 * float(lat)) + 90.0) * self.mapImageRect.height) / 180.0) + self.mapImageRect.y
			
			if mag < 0.8: mag = 0.8 #too small to see blink
			
			# Determine circle radius from mag
			radius = mag * 3
			# Draw a circle at earthquake location
			self.drawCircle(mapX, mapY, radius, color)

			return mapX, mapY, radius, color
		else:
			#CLI 
			return False

	# pygames key press
	def handleKeyPress(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				#press escape to exit
				if event.key == pygame.K_ESCAPE:
					pygame.display.quit()
					pygame.quit()
					sys.exit()
				if event.key == pygame.K_q:
					pygame.display.quit()
					pygame.quit()
					sys.exit()
				if event.key == pygame.K_f:
					self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
					return True
				if event.key == pygame.K_w:
					#window
					self.screen = pygame.display.set_mode((800, 480))
					return True
				if event.key == pygame.K_h:
					# flip flop for time24h
					if self.time24h:
						self.time24h = False
						self.setTextSize(20)
						self.drawRightJustifiedText((self.mapImageRect.y + 300), "settings: 12h")
						self.setTextSize(40)
					else:
						self.time24h = True
						self.setTextSize(20)
						self.drawRightJustifiedText((self.mapImageRect.y + 300), "settings: time24h")
						self.setTextSize(40)
					return True
				if event.key == pygame.K_d:
					# flip flop for distance
					if self.dist == "m":
						self.dist = "k"
						self.setTextSize(20)
						self.drawRightJustifiedText((self.mapImageRect.y + 300), "settings: km")
						self.setTextSize(40)
					else:
						self.dist = "m"
						self.setTextSize(20)
						self.drawRightJustifiedText((self.mapImageRect.y + 300), "settings: mi")
						self.setTextSize(40)
					return True
				if event.key == pygame.K_m:
					#change map
					# Read the map into memory, center it and reset text boxes if sized changed
					self.mapImage = pygame.image.load('maps/eqm800.bmp')

					self.mapImageRect = self.mapImage.get_rect()
					self.mapImageRect.y = (pygame.display.get_surface().get_height() - self.mapImageRect.height) / 2
					self.mapImageRect.x = (pygame.display.get_surface().get_width() - self.mapImageRect.width) / 2
					self.topTextRow = self.mapImageRect.y - 25
					self.eventsTextRow = self.topTextRow + 400
					self.bottomTextRow = self.topTextRow + 430
					self.screen.blit(self.mapImage, self.mapImageRect)
					return True
				if event.key == pygame.K_u:
					#go UTC
					return True
			elif event.type == pygame.KEYUP:
				return True

			else:
				return False
	
	# Display current time and input
	def displayCurrentTime(self):
		timeNow = datetime.now()

		if self.time24h:
			timeString = timeNow.strftime("%-H:%M")
		else:
			timeString = timeNow.strftime("%-I:%M%P")

		self.handleKeyPress()
		
		# Display time to GUI only
		try:
			pygame.draw.rect(self.screen,self.black,(self.mapImageRect.x,self.topTextRow,130,25))
			self.drawText(self.mapImageRect.x, self.topTextRow, timeString)
		except: 
			return timeNow


	# Display Bottom Data Bar string
	def displayBottomDataFeed(self, max_location, eventCount):
		currentRTC = datetime.now()
		if self.time24h:
			self.eventTimeStringLong = currentRTC.strftime("%-H:%M %d/%m/%y")
			self.eventTimeString = currentRTC.strftime("%-H:%M")
		else:
			self.eventTimeStringLong = currentRTC.strftime("%-I:%M %P %m/%d/%y")
			self.eventTimeString = currentRTC.strftime("%-I:%M%P")

		self.eventCount = eventCount

		self.setTextColor(self.black)
		self.setTextSize(25)
		if max_location is None or max_location == "":
			max_location = "No Data"
		self.drawCenteredText(self.eventsTextRow, "HiMag: " + max_location + ". updated:" + self.eventTimeStringLong)
		self.setTextSize(40)
		self.setTextColor(self.white)
		return True

	# Display Last EQ Event
	def displayEventLong(self, location, mag, depth):
		self.setTextSize(40)
		self.setTextColor(self.colorFromMag(mag))
		
		try:
			miles = (depth / 1.609344)
		except:
			miles = 0

		if self.dist == "m":
			milesStr =  str(miles)[:4] + "mi"
		else:
			milesStr = str(depth) + "km"
		
		location = location[:24] #truncate long names centering from pygame will just overlap badly
		self.drawCenteredText(self.bottomTextRow,location + (" Mag:" + str(mag)) + " @" + milesStr)
		return True
	
	# Display LastEQ/High Mag String
	def displayDBStats(self, mag, count, largestmag, tsunami, alert, cluster=False):
		currentAlarm = ""
		try:
			if cluster: currentAlarm = "CLSTR"
			if mag > 7: currentAlarm = "MAJOR"
			if tsunami != 0: currentAlarm = "TSUNAMI"
			if alert is not None: currentAlarm = "ALERT"
		except:
			currentAlarm = "UNKNOWN"
		
		self.setTextSize(40)
		self.drawRightJustifiedText(self.topTextRow, currentAlarm + " | EQTotal: " + str(count) + "| HiMag:" + largestmag)
		return True

	# Display Wash/Title page
	def displayWashPage(self, largestevent, activeregion, dayTrend, max_location):
		currentRTC = datetime.now()
		eventDayString = currentRTC.strftime("%A %B %d week %U day %j") #https://strftime.org
		if self.hasGUI:

			# Refresh Display by redrawing the map to the screen
			self.displayMap()

			# Data to always display
			self.setTextSize(30)
			if self.screenWidth > 1000:
				self.drawCenteredText((self.mapImageRect.y + 320), eventDayString)
			else:
				self.drawCenteredText((self.mapImageRect.y + 220), eventDayString)
			
			self.setTextSize(40)

			freq_trend = ""
			try:
				if len(eventDB.dailyevents) > 1:
					if eventDB.dailyevents[-1] > eventDB.dailyevents[-2]:
						freq_trend = " +"
					elif eventDB.dailyevents[-1] < eventDB.dailyevents[-2]:
						freq_trend = " -"
					else:
						freq_trend = " ="
			except Exception:
				pass

			# Display different data throughout the day using the timput value
			if self.firstRun == False:
				try:
					# Defensive: convert all to string, handle None/empty
					largestevent_str = "" if largestevent is None else str(largestevent)
					max_location_str = "" if not max_location else str(max_location)
					activeregion_str = "" if not activeregion else str(activeregion)
					dayTrend_str = "" if not dayTrend else str(dayTrend)

					if self.screenWidth > 1000:
						self.drawCenteredText((self.topTextRow + 120), "HiMag:" + largestevent_str + " in " + max_location_str)
						self.drawCenteredText((self.topTextRow + 230), "Active Region: " + activeregion_str)
						self.drawCenteredText((self.topTextRow + 390), str(self.eventCount) + " events, last quake @" + self.eventTimeStringLong)
						self.drawCenteredText((self.topTextRow + 430), "Yesterdays event count " + dayTrend_str + freq_trend)
						time.sleep(20)
					else:
						self.setTextSize(30)
						self.drawCenteredText((self.topTextRow + 90), "HiMag:" + largestevent_str + " in " + max_location_str)
						self.setTextSize(40)
						self.drawCenteredText((self.topTextRow + 160), "Active Region: " + activeregion_str)
						self.drawCenteredText((self.topTextRow + 300), str(self.eventCount) + " events, last quake @" + self.eventTimeStringLong)
						self.drawCenteredText((self.topTextRow + 430), "Yesterdays event count " + dayTrend_str + freq_trend)
					self.firstRun = False
					return True
				except Exception as e:
					print(f"Error displaying wash page: {e}")
					return False
			
		else:
			#Cli output
			return True
		
# Create global instance
displayManager = DisplayManager()

