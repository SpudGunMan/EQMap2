"""
This code handles display by writing directly to the framebuffer in pygame
Concept, Design by: Craig A. Lindley
"""

from cProfile import run
import os, time, sys
from datetime import datetime
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

		pygame.init()

		try:
			#set monitor to use
			self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
			self.displayInfo = pygame.display.Info()
			self.screenWidth  = self.displayInfo.current_w
			self.screenHeight = self.displayInfo.current_h
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
		if mag < 1:
			mag = 1.0

		imag = int(mag + 0.5)
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


	# Display 'Events drawn' string
	def displayBottomDataFeed(self, max_location):
		currentRTC = datetime.now()
		if self.time24h:
			self.eventTimeStringLong = currentRTC.strftime("%-H:%M %d/%m %Y")
			self.eventTimeString = currentRTC.strftime("%-H:%M")
		else:
			self.eventTimeStringLong = currentRTC.strftime("%-I:%M %P %m/%d %Y")
			self.eventTimeString = currentRTC.strftime("%-I:%M%P")


		self.setTextColor(self.blue)
		self.setTextSize(20)
		self.drawCenteredText(self.eventsTextRow, "Largest EQ @ " + max_location + "  Last EQ @" + self.eventTimeStringLong)
		self.setTextSize(40)
		self.setTextColor(self.white)
		return True

	# Display Last EQ Event
	def displayEventLong(self, location, mag, depth):
		self.setTextSize(40)
		self.setTextColor(self.colorFromMag(mag))
		
		miles = (depth / 1.609344)

		if self.dist == "m":
			milesStr =  str(miles)[:4] + "mi"
		else:
			milesStr = str(depth) + "km"
		
		location = location[:24] #truncate long names centering from pygame will just overlap badly
		self.drawCenteredText(self.bottomTextRow,location + (" Mag:" + str(mag)) + "@" + milesStr)
		return True
	
	# Display LastEQ/High Mag String
	def displayDBStats(self, mag, count, largestmag, tsunami, alert, cluster=False):
		currentAlarm = ""
		if cluster: currentAlarm = "CLSTR"
		if mag > 7: currentAlarm = "MAJOR"
		if tsunami != 0: currentAlarm = "TSUNAMI"
		if alert is not None: currentAlarm = "ALERT"
		self.setTextSize(40)
		self.drawRightJustifiedText(self.topTextRow, currentAlarm + "| EQTotal: " + str(count) + "| HiMag:" + largestmag)
		return True

	# Display Wash/Title page
	def displayWashPage(self, largestevent, activeregion, dayTrend):
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
			
			# Display different data throughout the day using the timput value
			if self.firstRun == False:
				if self.screenWidth > 1000:
					self.drawCenteredText((self.topTextRow + 120), "Largest seen Mag:" + largestevent)
					self.drawCenteredText((self.topTextRow + 260), "Active Region: " + activeregion)
					self.drawCenteredText((self.topTextRow + 400), str(self.eventCount) + " events, last quake @" + self.eventTimeStringLong)
					self.drawCenteredText((self.topTextRow + 450), "Yesterdays event count " + dayTrend)
					time.sleep(20)
				else:
					self.drawCenteredText((self.topTextRow + 90), "Largest seen Mag:" + largestevent)
					self.drawCenteredText((self.topTextRow + 160), "Active Region: " + activeregion)
					self.drawCenteredText((self.topTextRow + 300), str(self.eventCount) + " events, last quake @" + self.eventTimeStringLong)
					self.drawCenteredText((self.topTextRow + 350), "Yesterdays event count " + dayTrend)
					time.sleep(20)
				return True
			
			if self.firstRun:
				self.firstRun = False
				self.drawCenteredText((self.topTextRow + 90), "Loading")
				self.drawCenteredText((self.topTextRow + 140), "Realtime World")
				self.setTextSize(70)
				self.drawCenteredText((self.topTextRow + 160), "Earthquake Map")
				self.setTextSize(30)
				self.drawText((self.mapImageRect.x +2), (self.bottomTextRow - 80), "   Revision:22.12")
				self.drawRightJustifiedText((self.bottomTextRow - 80), "C.Lindley   ")
				self.setTextSize(40)
				time.sleep(5)
				return True
		else:
			#Cli output
			return True
		
# Create global instance
displayManager = DisplayManager()

