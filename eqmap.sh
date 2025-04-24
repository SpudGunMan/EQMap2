#!/bin/bash
# if rpi in uname -a, run the script
if [[ $(uname -a) == *"rpi"* ]]; then

    # replace user pi with whoami in the EQMap.desktop file
    if [ -f /home/pi/Desktop/EQMap.desktop ]; then
        sed -i "s|/home/pi|/home/$(whoami)|g" /home/pi/Desktop/EQMap.desktop
    fi

    # ask to autostart the EQMap.desktop file
    if [ ! -f ~/.config/autostart/EQMap.desktop ]; then
        read -p "Do you want to autostart EQMap? (y/n) " answer
        if [[ $answer == "y" || $answer == "Y" ]]; then
            # copy the EQMap.desktop file to ~/.config/autostart
            cp EQMap.desktop ~/.config/autostart/
        fi
    fi

fi

# Run the EQMap.py script
cd "$(dirname "$0")"
python3 EQMap.py
