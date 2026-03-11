![EarthQuakeMapDisplay](/maps/display.jpg) ![EarthQuakeMap](/maps/logo.jpg)

# EQMap2 (Revision 26.03)

EQMap2 is a real-time earthquake map display for Raspberry Pi screens and desktop monitors.

This fork keeps the original EQMap behavior and adds:
- Dual feed polling (USGS + SeismicPortal EU)
- Real-time clock and additional on-screen stats
- High-resolution display support
- Runtime display settings (time format, distance units, map mode)
- Daily event trending graph
- Daily database playback via `python3 EQPlay.py`
- Optional RAM disk storage support (`/run/shm`) to reduce SD card writes
- Volcano alert tracking (USGS HANS)

## Quick Start

```sh
cd ~
git clone https://github.com/SpudGunMan/EQMap2
cd EQMap2
python3 EQMap.py
```

## Requirements

- Python 3
- `requests`
- `pygame-ce` (recommended over legacy `pygame`)

If needed:

```sh
pip uninstall -y pygame
pip install pygame-ce requests
```

## Controls

| Key | Action |
| --- | --- |
| `Esc` / `q` | Quit program |
| `d` | Toggle distance units (`mi` / `km`) |
| `h` | Toggle time format (`12h` / `24h`) |
| `f` | Fullscreen mode |
| `w` | Window mode |
| `m` | Cycle map |

## Playback

Replay saved daily data:

```sh
python3 EQPlay.py
```

## Raspberry Pi Notes

For 7-inch ribbon-attached displays on newer Raspberry Pi OS builds:
1. Enable SSH on first boot if needed by creating an empty `ssh` file in the boot FAT partition.
1. Run `sudo raspi-config` and enable graphics options needed by your display stack.
1. If touchscreen detection is unreliable, add `dtoverlay=edt-ft5406` to `/boot/firmware/config.txt`.
1. Reboot.

## Troubleshooting

- Update first: `git pull`
- If display initialization fails with pygame permissions issues, verify framebuffer permissions:

```sh
ls -l /dev/fb*
sudo chmod a+rw /dev/fb0
```

- If one data source is down, the other source should continue to update.
- Test playback mode (`EQPlay.py`) to validate rendering and stored data.

## Tested Notes

- 2025.10 Trixie
- Known upstream feed instability has occurred at times with SeismicPortal EU.
- Known pygame Pi issue reference:
  - https://github.com/pygame/pygame/issues/3003

## Hardware Tested

- https://www.amazon.com/ElecLab-Raspberry-Touchscreen-Monitor-Capacitive/dp/B08LVC4KRM/
- https://www.amazon.com/Eviciv-Portable-Monitor-Display-1024X600/dp/B07L6WT77H/

## Upstream Credits

- Original project source: http://craigandheather.net/celeearthquakemap.html
- Original EQMap code is included under `docs/src` by Craig A. Lindley (2021).

## Roadmap Ideas

- Additional feeds (tsunami, fault overlays)
- Persist all runtime settings
- More map themes and overlays

Contributions and bug reports are welcome.
