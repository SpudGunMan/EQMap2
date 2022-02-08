from DisplayManager import displayManager
from EQMap import BLACK
from EventDB import eventDB
from time import sleep

#load DB
EQEventQueue = eventDB.load()

def displayDatabase():
    # Repaint the map from the events in the DB
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

def main():
    try:
        while True:
            displayDatabase()
           
            displayManager.handleKeyPress()

            sleep(5)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()














