 ![EarthQuakeMapDisplay](/maps/display.jpg) ![EarthQuakeMap](/maps/logo.jpg)

# About Revision:24.1
This is a Earthquake Map Display for RaspberryPi Attached screen

This fork adds additional features, while keeping the orginal functionality (I hope!)
- added parallel data souce earthquake.usgs.gov 60s polling each source
- command line output 
- realtime clock
- new display data and reporting
- hi-res ability to extend to any monitor
- ability to change basic settings in runtime
- Daily event Trending
- Daily database for playback later `python3 EQPlay.py`
  - RamDisk use to lower any disk write on Pi SD-Card
  - multi day player 

Feel free to pull issues/suggestions or forks to contribute!

# Settings Keys

| Command | Description |
| --- | --- |
| esc / q | end program, exit fuillscreen |
| d | *D*istance calculations in mi/km |
| h | *H*ours calculations in 12p/24h |
| f | Set *f*ullscreen mode |
| w | Set *w*indow mode |
| m | Cycle *m*aps |

# Installation
```shell
cd ~
git clone https://github.com/SpudGunMan/EQMap2
cd EQMap2/
python3 EQMap.py
```
if you are not running a raspberry you may need to install pre-req they are included on raspberry by default so no need to continue here for Pi use...

```shell
sudo apt-get install python3-pip python3-dev python3-pygame
```
# Issues
If you have issues make sure your running the newest code `git pull`, let me know if you see a problem!
if you really get stuck you can start over or try a `git reset --hard` follwed by a pull.

## Hardware:
to get 7" ribbon attached display you might need to do a few things to bullseye
1. when you flash the OS to SSD open the FAT-partition on the SSD you just made and `touch ssh` to force enable SSH (or just make a empty file with the name of `ssh` nothing more no .txt)
1. you need to then use `sudo raspi-config` to enable legacy GL drivers till [this bug is fully fixed](https://github.com/raspberrypi/linux/issues/4686) to adjust 50K rate of screen. UPDATE 9/2022 there will likely be no fix for this workaround is needed.
1. Reboot to "hopefully" a working Pi Screen on bullseye

### Tested
* Raspberry Pi3 running raspOS-bullseye.SEPT.2022
* https://www.amazon.com/ElecLab-Raspberry-Touchscreen-Monitor-Capacitive/dp/B08LVC4KRM/
* https://www.amazon.com/Eviciv-Portable-Monitor-Display-1024X600/dp/B07L6WT77H/
  * both work nice with a offical raspberry pi4/usb-c power supply at 3A and pi3 or Pi4
* osx12 native (need to add python tools like pip3 install pygames)

### Untested:
* Raspberry nano e-ink

## EQMap Source 
* The upstream branch is a straight copy from http://craigandheather.net/celeearthquakemap.html
  * EQMap orginal project in doc/src directory by Craig A. Lindley 2021

## To-Do
normally on a next branch if you see it try it out! `git pull origin next`
- add other types of data (tide)
  - volcano plotting
  - tsunami data
- save settings
  - UTC
- replay from larger returns in USGS (poll more in UK)
- generate some new maps
  - fault lines


