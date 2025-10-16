from DisplayManager import displayManager
from EQMap import BLACK
from EventDB import eventDB
from time import sleep

EQEventQueue = []

# Initial display
displayManager.displayMap()
displayManager.drawRightJustifiedText(500, "database player")
sleep(2)

def displayDatabase(day):
    # Repaint the map from the events in the DB
    displayManager.displayMap()

    # Load DB event queue for the given day
    EQEventQueue, filecount = eventDB.load(day)
    eventcount = len(EQEventQueue)

    # Print event queue to map
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
    EQEventQueue, filecount = eventDB.load() # grab filecount
    try:
        for day in range(filecount):
            events = displayDatabase(day)
            # Determine trend direction
            if events > lastevents:
                trend = "up"
            elif events < lastevents:
                trend = "down"
            else:
                trend = ""
            lastevents = events

            # Display trending info
            displayManager.drawRightJustifiedText(100, f"db: {day} Events: {events} Trending {trend}")

            # Show the trend graph using getDayTrend
            dayTrend = eventDB.getDayTrend()
            displayManager.displayTrendingGraph(dayTrend)

            displayManager.handleKeyPress()
            sleep(5)
    except KeyboardInterrupt:
        print("Exiting EQMap")
        displayManager.clearDisplay()
        displayManager.drawRightJustifiedText(100, "Exiting EQMap")
        sleep(2)
        displayManager.clearDisplay()
        exit()

if __name__ == '__main__':
    main()