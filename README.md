![EarthQuakeMap](/maps/logo.jpg)  ![EarthQuakeMapDisplay](/maps/display.jpg)

# About
This is a Earthquake Map Display for RaspberryPi Attached screen

This fork adds additional features, while keeping the orginal functionality.
- added additional data souce earthquake.usgs.gov
  - its a bit dodgy, alternating data sources 30 second intervals by default
- command line output
- working clock
- fullscreen mode, native
- new display data
- hi-res ability to extend to any monitor (early support)
- ability to change settings for customization (early support)

Feel free to pull issues/suggestions or forks to contribute!

# Settings Keys

| Command | Description |
| --- | --- |
| esc / q | end program, exit fuillscreen |
| d | *D*istance calculations in mi/km |
| h | *H*ours calculations in 12p/24h |
| u | Hours to *U*TC (TODO) |
| f | Set *f*ullscreen mode |
| w | Set *w*indow mode (TODO) |
| m | Cycle *m*aps (TODO) |
| b | Set *b*rightness/Dim Display (TODO) |

# Installation
```shell
sudo apt-get install python3-pip python3-dev
sudo pip3 install pygame
cd ~
git clone https://github.com/SpudGunMan/EQMap2
cd EQMap2/
python3 EQMap.py
```

# Issues
If you have issues make sure your running the newest code `git pull`, let me know if you see a problem!

## Hardware:
to get 7" ribbon attached display you need to do a few things to bullseye
1. when you flash the OS to SSD open the FAT-partition on the SSD you just made and `touch ssh` to force enable SSH (or just make a empty file with the name of `ssh` nothing more no .txt)
1. you need to then use `sudo raspi-config` to enable legacy GL drivers till [this bug is fully fixed](https://github.com/raspberrypi/linux/issues/4686) to adjust 50K rate of screen.
1. Reboot to "hopefully" a working Pi Screen on bullseye


### Tested
* Raspberry Pi3 running raspOS-bullseye.Jan28.2022
* https://www.amazon.com/ElecLab-Raspberry-Touchscreen-Monitor-Capacitive/dp/B08LVC4KRM/
  * works nice with a offical raspberry pi4/usb-c power supply at 3A and pi3
* osx12 native (need to add python tools like pip3 install pygames)

### Untested:
* Raspberry Pi4, nano
* https://www.amazon.com/Eviciv-Portable-Monitor-Display-1024X600/dp/B07L6WT77H/

## EQMap Source 
* The upstream branch is a straight copy from http://craigandheather.net/celeearthquakemap.html
  * EQMap orginal project in doc/src directory by Craig A. Lindley 2021

## To-Do
- add RSS or sun/moon/tide
- use memory to lower any disk write
- settings menu for UTC and sleep
- save settings
- save database for playback later
