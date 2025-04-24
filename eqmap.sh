#!/bin/bash
# if rpi in uname -a, run the script
if [[ $(uname -a) == *"rpi"* ]]; then

    # replace user pi with whoami in the EQMap.desktop file
    if [ -f /home/pi/Desktop/EQMap.desktop ]; then
        sed -i "s|/home/pi|/home/$(whoami)|g" /home/pi/Desktop/EQMap.desktop
    fi

    # copy the EQMap.desktop file to ~/.config/autostart
    if [ ! -f ~/.config/autostart/EQMap.desktop ]; then
        mkdir -p ~/.config/autostart
        cp /home/pi/Desktop/EQMap.desktop ~/.config/autostart/
    fi
fi

# Run the EQMap.py script
cd "$(dirname "$0")"
python3 EQMap.py
