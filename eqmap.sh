#!/bin/bash
# if rpi in uname -a, run the script
if [[ $(uname -a) == *"rpi"* ]]; then
    # check /dev/fb0 has permissions for all
    if [ ! -w /dev/fb0 ]; then
        echo "Setting permissions for /dev/fb0"
        sudo chmod 666 /dev/fb0
    fi
fi

# Run the EQMap.py script
cd "$(dirname "$0")"
python3 EQMap.py
