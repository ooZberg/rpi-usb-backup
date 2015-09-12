import logging
import sys
import os
import time
import subprocess
import RPi.GPIO as GPIO
import threading

# needs to be an actual folder, not a symlink
source_dir = '/media/usb0'
target_dir = '/backup'

#-------------------------------------------

version = 1.0

# setup logging
logger = logging.getLogger('usb-backup')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('/var/log/usb-backup.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

# start app
logger.info('----------------------------------------')
logger.info('Starting...')
logger.info('Version: %f' % (version))
logger.info('Source: %s' % source_dir)
logger.info('Target: %s' % target_dir)

# take led control
logger.info('Taking led control')
ret = os.system("echo none >/sys/class/leds/led0/trigger")

# led control - green ACT/OK led
# Needs to be BCM. GPIO.BOARD lets you address GPIO ports by periperal
# connector pin number, and the LED GPIO isn't on the connector
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

def led_flash(e, t):
    """flash the led continously"""
    while not e.isSet():
        time.sleep(t)
        GPIO.output(16, GPIO.LOW)
        time.sleep(t)
        GPIO.output(16, GPIO.HIGH)

# start slow blinking while wating for device to be connected
e = threading.Event()
t = threading.Thread(target=led_flash, args=(e, 1.0))
t.start()

logger.info('Waiting for files to show up in source directory...')
while os.listdir(source_dir) == []:
    # the usb folder is empty, nothing to copy, just wait
    time.sleep(5)
# stop slow blinking
e.set()


# start fast blinking while coping files for device to be connected
e = threading.Event()
t = threading.Thread(target=led_flash, args=(e, 0.2))
t.start()

logger.info('Files found, starting backup...')

# use rsync without checksums etc
cmd = '/usr/bin/rsync -rtvW %s %s' % (source_dir, target_dir)
logger.info('Command: %s' % cmd)

p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out = p.stdout.read()
logger.info('Output: %s' % out)

# stop fast blinking
e.set()

# set led on
GPIO.output(16, GPIO.LOW)

logger.info('Shutting down')
os.system("halt")

sys.exit(0)
