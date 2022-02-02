![EarthQuakeMap](/maps/logo.jpg)

![EarthQuakeMapDisplay](/maps/display.jpg)

# About
This is a Earthquake Map Display for RaspberryPi Attached screen

This fork adds additoional features
- command line output
- working clock
- fullscreen mode, escape or q to exit
- new display methods used for additional data on screen

# Installation
```shell
sudo apt-get install python3-pip python3-dev
sudo pip3 install pygame
cd ~
git clone https://github.com/SpudGunMan/EQMap2
cd EQMap2/
python3 EQMap.py
```
## Hardware:
to get 7" ribbon attached display you need to do a few things to bullseye
1. when you flash the OS to SSD open the /boot/config.txt file and `touch ssh` to force enable SSH
1. you need to then use `sudo raspi-config` to enable legacy GL drivers till [this bug is fully fixed](https://github.com/raspberrypi/linux/issues/4686)
1. Reboot to "hopefully" a working Pi Screen on bullseye


### Tested
* Raspberry Pi3 running raspOS-bullseye.Jan28.2022
* https://www.amazon.com/ElecLab-Raspberry-Touchscreen-Monitor-Capacitive/dp/B08LVC4KRM/
  * works nice with a offical raspberry pi4/usb-c power supply at 3A and pi3

### Untested:
* Raspberry Pi4,Pico
* https://www.amazon.com/Eviciv-Portable-Monitor-Display-1024X600/dp/B07L6WT77H/

## EQMap Source 
* http://craigandheather.net/celeearthquakemap.html
  * EQMap orginal project in doc/src directory by Craig A. Lindley 2021

## To-Do
- add RSS/moon/sun/tide
- use memory to lower any disk write
- settings menu for UTC and sleep