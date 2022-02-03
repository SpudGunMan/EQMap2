"""
This code handles the Raspberry Pi LCD display by writing directly to the framebuffer
The map image is in the images subdirectory and the font is in the fonts subdirectory.
Concept, Design and Implementation by: Craig A. Lindley
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # hide pygame prompt message
import pygame
import pygame.freetype
import time
import sys
from datetime import datetime

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
		
		except:
			#command line settings for display to console display
			self.screenWidth = -1
			self.screenHeight = -1
			self.screen = (-1, -1)

		# Read the map into memory
		self.mapImage = pygame.image.load('maps/eqm800_shaded.bmp')

		# Get its bounding box
		self.mapImageRect = self.mapImage.get_rect()

		# Center map 
		self.mapImageRect.y = (pygame.display.get_surface().get_height() - self.mapImageRect.height) / 2
		self.mapImageRect.x = (pygame.display.get_surface().get_width() - self.mapImageRect.width) / 2

		# Set the uypper and lower text areas
		self.topTextRow = self.mapImageRect.y - 35
		self.eventsTextRow = self.topTextRow + 415
		self.bottomTextRow = self.topTextRow + 455

		# Setup inital font of initial size
		self.font = pygame.freetype.Font('fonts/Sony.ttf', self.fontSize)

    # Clear the screen
	def clearScreen(self):
		try:	
			self.screen.fill(self.black)
			pygame.display.flip()
			return True
		except:
			return False

	# Backlight control not tested yet
	def backlight(self, b):
		if b:
			# Turn backlight on
			#os.system("sudo sh -c 'echo 0 > /sys/class/backlight/rpi_backlight/bl_power'")
			return True
		else:
			# Turn backlight off
			#os.system("sudo sh -c 'echo 1 > /sys/class/backlight/rpi_backlight/bl_power'")
			return False

	# Select color from magnitude
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

			# Center map 
			self.mapImageRect.y = (pygame.display.get_surface().get_height() - self.mapImageRect.height) / 2
			self.mapImageRect.x = (pygame.display.get_surface().get_width() - self.mapImageRect.width) / 2
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
		self.font = pygame.freetype.Font('fonts/Sony.ttf', self.fontSize)

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
		# Calculate map X and Y
		mapX = ((lon + 180.0) * self.mapImageRect.width) / 360.0 + self.mapImageRect.x
		mapY = ((((-1 * lat) + 90.0) * self.mapImageRect.height) / 180.0) + self.mapImageRect.y

		# Determine circle radius from mag
		if mag < 2:
			mag = 2.0
		radius = mag * 3

		# Draw a circle at earthquake location
		self.drawCircle(mapX, mapY, radius, color)
		return mapX, mapY, radius, color

	# Display current time and input
	def displayCurrentTime(self):
		timeNow = datetime.now()

		if self.time24h:
			timeString = timeNow.strftime("%-H:%M")
		else:
			timeString = timeNow.strftime("%-I:%M%P")

		# Display time to GUI only
		try:
			pygame.draw.rect(self.screen,self.black,(self.mapImageRect.x,self.topTextRow,260,35))
			self.drawText(self.mapImageRect.x, self.topTextRow, "Time: " + timeString)
		except: 
			return timeNow

		# Handle Input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				#press escape to exit
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == pygame.K_q:
					pygame.quit()
					sys.exit()
				if event.key == pygame.K_f:
					self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
					return timeNow
				if event.key == pygame.K_w:
					#window
					self.screen = pygame.display.set_mode((800, 480))
					return timeNow
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
					return timeNow
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
					return timeNow
				if event.key == pygame.K_m:
					#change map
					return timeNow
				if event.key == pygame.K_b:
					#dim brightness
					return timeNow
				if event.key == pygame.K_u:
					#go UTC
					return timeNow
			elif event.type == pygame.KEYUP:
				return timeNow

	# Display Events drawn string
	def displayNumberOfEvents(self, num):
		eventPull = datetime.now()
		if self.time24h:
			self.eventTimeStringLong = eventPull.strftime("%-H:%M %d/%m %Y")
			self.eventTimeString = eventPull.strftime("%-H:%M")
		else:
			self.eventTimeStringLong = eventPull.strftime("%-I:%M %P %m/%d %Y")
			self.eventTimeString = eventPull.strftime("%-I:%M%P")

		self.eventCount = num

		self.setTextColor(self.blue)
		self.setTextSize(20)
		self.drawCenteredText(self.eventsTextRow, str(num) + " total events drawn at " + self.eventTimeStringLong)
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
	def displayDBStats(self, mag, depth, largestmag):
		self.setTextSize(40)
		self.drawRightJustifiedText(self.topTextRow, "LastEQ:" + self.eventTimeString + " High:" + largestmag)
		return True

	# Display title page
	def displayTitlePage(self):
		eventPull = datetime.now()
		eventDayString = eventPull.strftime("%A %B %d week %U day %j") #https://strftime.org

		self.displayMap()
		self.drawCenteredText((self.mapImageRect.y + 90), "Realtime")
		self.setTextSize(70)
		self.drawCenteredText((self.mapImageRect.y + 160), "World Earthquake Map")
		self.setTextSize(40)
		self.drawCenteredText((self.mapImageRect.y + 220), eventDayString)
		
		if not self.firstRun: self.drawCenteredText((self.mapImageRect.y + 300), str(self.eventCount) + " events in database, last quake@" + self.eventTimeStringLong)
		
		if self.firstRun:
			self.setTextSize(20)
			self.drawText((self.mapImageRect.x +2), (self.mapImageRect.y + 300), "R2022-2-2")
			self.drawRightJustifiedText((self.mapImageRect.y + 300), "C.Lindley")
			self.setTextSize(40)
		
		time.sleep(10)
		self.firstRun = False
		return True
		
# Create global instance
displayManager = DisplayManager()

"""
# Test Code
import time

#displayManager.displayTitlePage()

displayManager.displayMap()
time.sleep(5)
displayManager.backlight(False)
time.sleep(5)
displayManager.backlight(True)

displayManager.drawText(0, 240, "This is some text")
displayManager.drawRightJustifiedText( 240, "This is some text")

displayManager.drawCenteredText(100, "This is some text to display")

displayManager.drawCircle(400, 240, 40, (0,0,255))
displayManager.mapEarthquake(0, 0, 2, (0,255,255))

displayManager.displayCurrentTime()
displayManager.displayMagnitude(3.6)
displayManager.displayDepth(-3.6)
displayManager.displayLocation("Tip of south Africa", 6.5)

while True:

	time.sleep(20)
"""

