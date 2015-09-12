# rpi-usb-backup

Automatically backup connected usb storage devices (e.g. cameras) to the RPi SD card.

Why is this useful?

* Backup your camera photos without a laptop, great for traveling
* No monitor/TV or keyboard needed
* Fully automated, just plug and play

Typical backup speed with RPi 1 model B is 5 MB/s.


## Requirements

* Raspberry Pi (tested with RPi 1 model B)
* SD card (preferably large)


## Installation

1. Install Raspbian (e.g. using the excellent "Pi Filler")
2. Copy all files to device, then execute:

 ./install.sh

3. Done

## Usage

1. Turn on the RPi.
2. When the RPi is booted ut, the green ACT/OK LED with start blinking slowly (1 Hz).
3. Connect your USB device, e.g. camera. It will be mounted automatically.
4. The backup will start and the LED will blink faster (5 Hz)
5. When the backup is finished, the LED will turn off and the RPi will shut down.
6. Disconnect your USB device. 
7. The backup is located in /backup

To backup another USB device, just start the RPi again. 

## Under the hood

This tool is basically a Python script that waits for USB storage devices to be mounted. Once a device is mounted, the files will be copied using rsync to the local file system. To make the process nice and smooth without any monitor, the green OK/ACT led is used to inform about the progress. The Python script is configured as autostarting service using supervisor.

### Trouble shooting

* Log file location: /var/log/usb-backup.log