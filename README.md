# README #

![Internet Radio Prototype](https://github.com/reyparma/sonda/blob/main/images/internet_radio_prototype.png)
<p align="center">Figure 1. Internet Radio Prototype</p>

### Quick Install of Sonda Reference Implementation on Pi Zero ###
* Using Raspberry Pi Imager, install the Sonda Reference Implementation by choosing "sonda-reference-v1-4gb-zero.img" file as the OS
* Wire the Pi Zero to the LED Matrix, PCM5102, Power Amp and speaker, PIR Sensor and Encoders 
* Insert the SD Card in the Pi Zero and power up
* ssh pi@sonda-radio using 'bluenote' password
* In the "tests" folder, run test-matrix.sh and test-sound.sh
* Enjoy!


### How to create a Sonda image for Raspberry Pi Zero from scratch ###

	* Using Raspberry Pi Imager, install Raspbian 32-bit OS Lite on a 4GB SD card
	* Copy ssh and wpa_supplicant.conf files from headless-wifi-setup folder to boot folder of the newly created SD card
	* Insert the card and power up the Zero
	* Login using default pi/raspberry credentials
    * Edit /etc/default/keyboard - Change to "us"
	* Run raspi-config to configure the following settings:
	    1. System Options
           1. Password - Change password to ‘xxxxx’
           2. Hostname - Change hostname to ‘sonda-radio’
        2. Display Options
           1. No changes
        3. Interface Options
           1. I2C - Enable
        4. Performance Options
           1. No changes
        5. Localisation Options
           1. Locale - set to en_US.UTF-8 UTF-8
           2. Timezone - set to US/Eastern
           3. Keyboard - Doesn’t work.  Leave it alone.  Edit keyboard settings from command line
           4. WLAN Country - US
        6. Advanced Options
           1. No changes
        7. Update
           1. No changes
        8. About raspi-config
           1. No changes
    * Reboot

### Checks ###

1. I2C
    1. ```ls /dev/i2c* /dev/spi*```
    2. Check: lsmod | grep -i i2c
        1. i2c_bcm2835	16384	0
        2. i2c_dev		20480	0
    3. lsmod | grep -i spi
    4. Check address:  sudo i2cdetect -y 1
        1. 0x70


### Install Matrix drivers ###
This will take approximately 10min

2. sudo apt-get update
3. sudo apt install python3-pip
4. sudo pip3 install rpi.gpio
5. sudo pip3 install adafruit-circuitpython-busdevice
6. sudo pip3 install adafruit-circuitpython-ht16k33
7. sudo pip3 install adafruit-circuitpython-framebuf
8. sudo apt-get install python3-pil
9. Reboot
10. Create test code and run:
```
import math
import time

import board
import busio
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from adafruit_ht16k33 import matrix

i2c = busio.I2C(board.SCL, board.SDA)

disp = matrix.Matrix8x8(i2c)

# Get display width and height.
width = 8
height = 8

# Create image buffer.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))

# Load default font.
#font = ImageFont.load_default()
#font = ImageFont.truetype('Minecraftia.ttf', 8)
font = ImageFont.truetype('Minecraftia-Regular.ttf', 8)

# Create drawing object.
draw = ImageDraw.Draw(image)

# Define text and get total width.
text = 'hello'
maxwidth, unused = draw.textsize(text, font=font)

# Set animation and sine wave parameters.
#Clear matrix
draw.rectangle((0,0,width,height), outline=0, fill=0)
draw.text((1, -2), 'a', font=font, fill=255)
imt = image.rotate(0)
disp.image(imt)
time.sleep(2)
imt = image.rotate(90)
disp.image(imt)
time.sleep(2)
imt = image.rotate(180)
disp.image(imt)
time.sleep(2)
imt = image.rotate(270)
disp.image(imt)
time.sleep(2)
disp.fill(0)
```

### Install I2S - NOTE: Follow new instructions located in pcm-setup/ folder! ###
	* Install I2S drivers for PCM1502
	    * curl -sS https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh | bash
	    * Need to reboot after install
		* Then run the script again and answer yes to test audio
		* Reboot again after test
		* Instructions - https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/raspberry-pi-usage
		* Convert to mono - create .asoundrc file in home folder with the following lines:
		pcm.!default {
            type plug
            slave.pcm {
                type asym
                playback.pcm {
                    type route
                    slave.pcm "dmix:0"
                    ttable.0.0 0.66
                    ttable.0.1 0.33
                    ttable.1.0 0.33
                    ttable.1.1 0.66
                }
                capture.pcm "hw:0"
            }
        }
        * Log out and log in
		* speaker-test  -t wav -c 2
		
### Install MPD MPC ###
	* Install mpd mpc
		* sudo apt-get install mpd mpc
		* Test mpc
		   * mpc volume 50
		   * mpc add http://64.95.243.43:8002/stream
		   * mpc play 1
 
### Only for Raspberry Pi (Not Zero) Configure mpd.conf to output audio to RPI audio jack
audio_output {
		type		"alsa"
	name		"My ALSA Device"
	device		"hw:CARD=Headphones,DEV=0"	# optional
	mixer_type      "software"      # optional
	'#	mixer_device	"default"	# optional
	mixer_control	"Headphone"		# optional
	mixer_index	"1"		# optional
}
    
### Wiring for PCM5102 ###
* DAC BOARD   > Raspberry Pi 3 Model B connector J8
* -----------------------------------------------
* SCK         > PIN 6 or any (GND)
* BCK         > PIN 12    (GPIO18)
* DIN         > PIN 40    (GPIO21)
* LRCK        > PIN 35    (GPIO19)
* GND         > PIN 6     (GND) Ground
* VIN         > PIN 2     (5V)


* How to run
  * python3 sonda.py 
