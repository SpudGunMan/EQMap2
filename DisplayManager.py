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
		self.topTextRow = 12
		self.eventsTextRow = 415
		self.bottomTextRow = 455
		self.fontSize = 40
		self.textColor = (255, 255, 255)
		self.black  = (0, 0, 0)
		self.white  = (255, 255, 255)
		self.red    = (255, 0, 0)
		self.yellow = (255, 255, 0)
		self.green  = (0, 255, 0)
		self.blue  = (0, 0, 255)
		self.eventTimeString = "loading..."

		pygame.init()

		try:
			#set monitor to use
			self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
			self.displayInfo = pygame.display.Info()
			self.screenWidth  = self.displayInfo.current_w
			self.screenHeight = self.displayInfo.current_h
			pygame.mouse.set_visible(0)
		
		except:
			#command line settings for display to console display
			#error with prior init for pygame
			self.screenWidth = -1
			self.screenHeight = -1
			self.screen = (-1, -1)
		
		screenWidth = self.screenWidth
		screenHeight = self.screenHeight

		# Read the map into memory
		self.mapImage = pygame.image.load('maps/eqm800_shaded.bmp')

		# Get its bounding box
		self.mapImageRect = self.mapImage.get_rect()

		# Center map vertically
		self.mapImageRect.y = (self.screenHeight - self.mapImageRect.height) / 2;

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
			os.system("sudo sh -c 'echo 0 > /sys/class/backlight/rpi_backlight/bl_power'")
		else:
			# Turn backlight off
			os.system("sudo sh -c 'echo 1 > /sys/class/backlight/rpi_backlight/bl_power'")

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
			x = self.screenWidth - rect.width - 1
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
		mapX = ((lon + 180.0) * self.mapImageRect.width) / 360.0
		mapY = ((((-1 * lat) + 90.0) * self.mapImageRect.height) / 180.0) + self.mapImageRect.y

		# Determine circle radius from mag
		if mag < 2:
			mag = 2.0
		radius = mag * 3

		# Draw a circle at earthquake location
		self.drawCircle(mapX, mapY, radius, color)
		return mapX, mapY, radius, color

	# Display current time
	def displayCurrentTime(self):
		timeNow = datetime.now()
		timeString = timeNow.strftime("%-I:%M %P")
		try:
			pygame.draw.rect(self.screen,self.black,(0,0,260,35))
			self.drawText(0, self.topTextRow, "Time: " + timeString)
		except:
			return timeNow

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
			elif event.type == pygame.KEYUP:
				return timeNow

	# Display magnitude
	def displayMagnitude(self, mag):
		self.setTextColor(self.colorFromMag(mag))
		self.drawCenteredText(self.topTextRow, "Mag: " + str(mag))
		self.setTextColor(self.white)

	# Display depth
	def displayDepth(self, depth):
		# Convert kilometers to miles
		miles = depth / 1.609344
		milesStr = "Depth: {d:.2f} m"
		self.drawRightJustifiedText(self.topTextRow, milesStr.format(d = miles))

	# Display number of events in DB
	def displayNumberOfEvents(self, num):
		eventPull = datetime.now()
		eventTimeStringLong = eventPull.strftime("%-I:%M %P %d/%m/%y")
		self.eventTimeString = eventPull.strftime("%-I:%M %P")
		self.setTextColor(self.blue)
		self.setTextSize(20)
		self.drawCenteredText(self.eventsTextRow, str(num) + " total events drawn at " + eventTimeStringLong)
		self.setTextSize(40)
		self.setTextColor(self.white)
		return True

	# Display location with color from magnitude
	def displayLocation(self, location, mag):
		try:
			self.setTextColor(self.colorFromMag(mag))
			self.drawCenteredText(self.bottomTextRow, location)
			self.setTextColor(self.white)
			return True
		except:
			print(location)
			return False

	def displayEventLong(self, location, mag, depth):
		self.setTextColor(self.colorFromMag(mag))
		# Convert kilometers to miles, otherwise change to just pront depth TODO add menu option
		miles = depth / 1.609344
		milesStr = "@{d:.2f}mi"
		location = location[:24] #truncate long names centering from pygame will just overlap badly
		self.drawCenteredText(self.bottomTextRow,location + (" Mag:" + str(mag)) + (milesStr.format(d = miles)))
		return True
	
	def displayDBStats(self, mag, depth, largestmag):
		#pygame.draw.rect(self.screen,self.black,(270,0,(self.screenWidth - 1),35))
		self.drawRightJustifiedText(self.topTextRow, "LastEQ:" + self.eventTimeString + " High:" + largestmag)
		return True

	# Display title page
	def displayTitlePage(self):
		self.displayMap()
		self.drawCenteredText(90, "Realtime")
		self.setTextSize(70)
		self.drawCenteredText(160, "World Earthquake Map")
		self.setTextSize(40)
		self.drawText(0, 350, "Nightly-Build")
		self.drawRightJustifiedText(350, "C.Lindley")
		time.sleep(10)
		
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

