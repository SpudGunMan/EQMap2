"""
This code handles display by writing directly to the framebuffer in pygame
Concept, Design by: Craig A. Lindley
"""

from cProfile import run
import os, time, sys
from datetime import datetime, timezone

from EventDB import eventDB 
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # hide pygame prompt message
import pygame, pygame.freetype
from pygame.locals import *
current_hour = datetime.now().hour
hours_remaining = 24 - current_hour

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
			self
			pygame.draw.rect(self.screen,self.black,(self.mapImageRect.x,self.topTextRow,130,25))
			self.setTextSize(40)
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
	
	def displayTrendingGraph(self, dayTrend):
			# Draw a simple floating line graph of dayTrend in the middle of the screen
			if not self.hasGUI or not dayTrend or len(dayTrend) < 2:
				return False

			from datetime import datetime

			# Graph placement and size
			if self.screenWidth > 1000:
				graph_width = int(self.screenWidth * 0.2)
				graph_height = 150
				margin_x = 40
				margin_y = 40
				# Move graph more to the left and up for high-res screens
				x0 = int(self.screenWidth * 0.55) + margin_x
				y0 = int(self.screenHeight * 0.40) + margin_y
			else:
				graph_width = int(self.screenWidth * 0.4)
				graph_height = 100
				margin_x = 40
				margin_y = 40
				x0 = int(self.screenWidth * 0.5) + margin_x
				y0 = int(self.screenHeight * 0.5) + margin_y

			# Clean and normalize data
			cleaned_dayTrend = []
			for val in dayTrend:
				try:
					cleaned_dayTrend.append(float(val))
				except (ValueError, TypeError):
					cleaned_dayTrend.append(0.0)
			dayTrend = cleaned_dayTrend

			# Find the first non-zero data point
			start_idx = 0
			for i, val in enumerate(dayTrend):
				if val != 0.0:
					start_idx = i
					break

			# Only plot from the first real data point
			plotTrend = dayTrend[start_idx:]
			if len(plotTrend) < 2:
				return False

			max_val = max(plotTrend)
			min_val = min(plotTrend)
			val_range = max_val - min_val if max_val != min_val else 1
		
			points = []
			for i, val in enumerate(plotTrend):
				x = x0 + int((i) * (graph_width / (len(plotTrend) - 1)))
				y = y0 + graph_height - int((val - min_val) / val_range * (graph_height - 10))
				points.append((x, y, val))

			# Draw the line graph, skipping segments where either value is 0
			for i in range(1, len(points)):
				x1, y1, v1 = points[i-1]
				x2, y2, v2 = points[i]
				if v1 != 0 and v2 != 0:
					pygame.draw.line(self.screen, self.green, (x1, y1), (x2, y2), 2)

			# Calculate dynamic hours remaining and label start hour
			current_hour = datetime.now().hour
			hours_remaining = 24 - current_hour
			start_hour = start_idx  # If your data is hourly, this is the hour of the first data point

			# Draw labels
			if self.screenWidth > 1000:
				graph_width = int(self.screenWidth * 0.2)
				graph_height = 150
				margin_x = 40
				margin_y = 40
				# Move graph more to the left and further down for high-res screens
				x0 = int(self.screenWidth * 0.55) + margin_x
				y0 = int(self.screenHeight * 0.40) + margin_y
			
				self.setTextSize(20)
				label_x = x0 - 140  # Shift labels further left
				label_y_offset = 150 	# Shift labels further down
				self.drawText(label_x, y0 + graph_height - 110 + label_y_offset,
							  f"Freq Trend (hourly, {len(plotTrend)}h shown, {hours_remaining}h left today)")
				self.drawText(label_x, y0 + graph_height - 130 + label_y_offset,
							  f"Start: {start_hour:02d}:00 (local)")
				self.drawRightJustifiedText(y0 + graph_height - 130 + label_y_offset,
										   f"Max Events/hour: {max_val}")
			
				# # Draw a small cross at the center of the graph area for reference
				# center_x = x0 + graph_width // 2
				# center_y = y0 + graph_height // 2 + 30  # Move center down by 30 pixels
				# pygame.draw.line(self.screen, self.red, (center_x - 5, center_y), (center_x + 5, center_y), 2)
				# pygame.draw.line(self.screen, self.red, (center_x, center_y - 5), (center_x, center_y + 5), 2)
			else:
				self.setTextSize(18)
				self.drawText(x0, y0 + graph_height + 15,
							  f"Freq Trend (hourly, {len(plotTrend)}h shown, {hours_remaining}h left today)")
				self.drawText(x0, y0 + graph_height + 2,
							  f"Start: {start_hour:02d}:00 (local)")
				self.drawRightJustifiedText(y0 + graph_height - 8,
										   f"Max Events/hour: {max_val}")

			pygame.display.flip()
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
	
	# Display Last Volcanic Event
	def displayVolcanoEvent(self, lon, lat):
		if self.hasGUI and lon != '':
			# Calculate map X and Y
			mapX = ((float(lon) + 180.0) * self.mapImageRect.width) / 360.0 + self.mapImageRect.x
			mapY = ((((-1 * float(lat)) + 90.0) * self.mapImageRect.height) / 180.0) + self.mapImageRect.y
			
			# Draw a triangle at volcano location
			pygame.draw.polygon(self.screen, self.red, [(mapX, mapY - 6), (mapX - 5, mapY + 4), (mapX + 5, mapY + 4)], 0)
			pygame.display.flip()
			return mapX, mapY, self.blue
		else:
			#CLI 
			return False
	
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

		freq_trend = ""
		try:
			if len(eventDB.dailyevents) > 1:
				if eventDB.dailyevents[-1] > eventDB.dailyevents[-2]:
					freq_trend = "+"
				elif eventDB.dailyevents[-1] < eventDB.dailyevents[-2]:
					freq_trend = "-"
				else:
					freq_trend = "="
		except Exception as e:
			print(f"Error determining frequency trend: {e}")
			pass
		
		self.setTextSize(40)
		self.drawRightJustifiedText(self.topTextRow, currentAlarm + " | EQTotal: " + str(count) + freq_trend + " | HiMag: " + str(largestmag))
		return True

	# Display Wash/Title page
	def displayWashPage(self, largestevent, activeregion, dayTrend, max_location):
		currentRTC = datetime.now()
		eventDayString = currentRTC.strftime("%A %B %d week %U day %j") #https://strftime.org
		if self.hasGUI:

			# Refresh Display by redrawing the map to the screen
			self.displayMap()

			# Data to always display
			self.setTextSize(40)
			if self.screenWidth > 1000:
				self.drawCenteredText((self.mapImageRect.y + 320), eventDayString)
			else:
				self.drawCenteredText((self.mapImageRect.y + 220), eventDayString)
			

			freq_trend = ""
			try:
				if len(eventDB.dailyevents) > 1:
					if eventDB.dailyevents[-1] > eventDB.dailyevents[-2]:
						freq_trend = " Trend increasing"
					elif eventDB.dailyevents[-1] < eventDB.dailyevents[-2]:
						freq_trend = " Trend decreasing"
					else:
						freq_trend = " Trend steady"
			except Exception as e:
				print(f"Error determining frequency trend: {e}")
				pass

			# Display different data throughout the day using the timput value
			if self.firstRun == False:
				# Defensive: convert all to string, handle None/empty
				largestevent_str = "No Data" if largestevent is None or largestevent == "" else str(largestevent)
				max_location_str = "No Data" if max_location is None or max_location == "" else str(max_location)
				activeregion_str = "N/A" if not activeregion or activeregion in ([], (), "") else str(activeregion)
				dayTrend_str = "N/A" if not dayTrend or dayTrend in ([], (), "") else str(len(dayTrend))

				if self.screenWidth > 1000:
					self.setTextSize(40)
					self.drawCenteredText((self.topTextRow + 120), "HiMag:" + largestevent_str + " in " + max_location_str)
					self.drawCenteredText((self.topTextRow + 130), "Active Region:")
					self.drawCenteredText((self.topTextRow + 170), activeregion_str)
					self.drawCenteredText((self.topTextRow + 390), str(self.eventCount) + " events, last quake @" + self.eventTimeStringLong)
					self.drawCenteredText((self.topTextRow + 430), "Yesterdays event count " + dayTrend_str + freq_trend)
				else:
					self.setTextSize(30)
					self.drawCenteredText((self.topTextRow + 90), "HiMag:" + largestevent_str + " in " + max_location_str)
					self.setTextSize(40)
					self.drawCenteredText((self.topTextRow + 130), "Active Region:")
					self.drawCenteredText((self.topTextRow + 170), activeregion_str)
					self.drawCenteredText((self.topTextRow + 300), str(self.eventCount) + " events, last quake @" + self.eventTimeStringLong)
					self.drawCenteredText((self.topTextRow + 430), "Yesterdays event count " + dayTrend_str + freq_trend)
				time.sleep(20) # show page for 20 seconds

			# Initial startup display
			else:
				self.setTextSize(40)
				self.drawCenteredText((self.topTextRow + 90), "Loading")
				self.drawCenteredText((self.topTextRow + 140), "Realtime World")
				self.setTextSize(70)
				self.drawCenteredText((self.topTextRow + 165), "Earthquake Map")
				self.setTextSize(30)
				self.drawText((self.mapImageRect.x +2), (self.bottomTextRow - 80), "   Revision:25.11")
				self.drawRightJustifiedText((self.bottomTextRow - 80), "C.Lindley   ")
				self.firstRun = False
				time.sleep(5) #show startup screen for 5 seconds
				self.firstRun = False
		else:
			#Cli output
			return True
		
# Create global instance
displayManager = DisplayManager()

