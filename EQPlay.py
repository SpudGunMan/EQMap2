from DisplayManager import displayManager
from EQMap import BLACK
from EventDB import eventDB
from time import sleep
EQEventQueue = []

displayManager.displayMap()
displayManager.drawRightJustifiedText(500, "database player")
sleep(2)

def displayDatabase(day=0):
    # Repaint the map from the events in the DB
    displayManager.displayMap()

    #load DB
    EQEventQueue, filecount = eventDB.load(file=day)

    #print event queue to map
    for event in EQEventQueue:
        cqLon = event[0]
        cqLat = event[1]
        cqMag = event[2]
        cqTsunami = event[3]
        cqAlert = event[4]
        color = displayManager.colorFromMag(cqMag)
        displayManager.mapEarthquake(cqLon, cqLat, cqMag, color)

    return filecount

def main():
    updateMap = True
    EQEventQueue, filecount = eventDB.load()
    try:
        while updateMap:
            for day in range(filecount):
                displayManager.displayMap()
                displayDatabase(filecount)
                displayManager.drawRightJustifiedText(500, "db: " + str(filecount))
                displayManager.handleKeyPress()
                sleep(5)
                filecount = filecount -1
                if filecount  == 0:
                    EQEventQueue, filecount = eventDB.load()
                    sleep(1)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()














