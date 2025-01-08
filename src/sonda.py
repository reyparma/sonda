import signal
import sys
import RPi.GPIO as GPIO
import subprocess
import time
import threading
from numbers2 import show_number,matrix_fill

PIR_GPIO = 26
timer = None
countMotion = 0
playing = False 

VOLUME_DOWN_GPIO = 4    #7
VOLUME_UP_GPIO = 17	#11
STATION_DOWN_GPIO = 27 	#13
STATION_UP_GPIO = 22 	#15

MAX_STATIONS = 5
CURRENT_STATION = 1

ENCODER_CLK_GPIO = 4   #23
ENCODER_DTA_GPIO = 17    #24
ENCODER_SW_GPIO = 25
counter = 0
clkLastState = 0
dtLastState = 0
swLastState = 0
step = 5
paused = False

ENCODER2_CLK_GPIO = 27
ENCODER2_DTA_GPIO = 22
counter2 = 0
clkLastState2 = 0
dtLastState2 = 0
swLastState2 = 0
step2 = 1
paused2 = False 

def mpcCommand(cmd):
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	return p.stdout.read()

def signal_handler(sig, frame):
    print('Detected Ctrl-C')
    mpcCommand(['mpc', 'stop'])
    matrix_init()
    matrix_fill(0)
    GPIO.cleanup()
    sys.exit(0)

def station_up_callback(channel):
    global CURRENT_STATION
    CURRENT_STATION = CURRENT_STATION + 1
    if CURRENT_STATION > MAX_STATIONS:
	    CURRENT_STATION = 1
    mpcCommand(['mpc', 'play', str(CURRENT_STATION)])    
    print("Playing "+str(CURRENT_STATION))
    show_number(0,0,CURRENT_STATION)
    matrix_text("Station " + str(CURRENT_STATION))
    matrix_text("")

def station_down_callback(channel):
    global CURRENT_STATION
    CURRENT_STATION = CURRENT_STATION - 1
    if CURRENT_STATION < 1:
	    CURRENT_STATION = 5
    mpcCommand(['mpc', 'play', str(CURRENT_STATION)])    
    print("Playing "+str(CURRENT_STATION))
    show_number(0,0,CURRENT_STATION)
    matrix_text("Station " + str(CURRENT_STATION))
    matrix_text("")

def volume_down_callback(channel):
    mpcRet = mpcCommand(['mpc', 'volume', '-5'])    
    print("Volume "+str(mpcRet))

def volume_up_callback(channel):
    mpcRet = mpcCommand(['mpc', 'volume', '+5'])    
    print("Volume "+str(mpcRet))

# Initialize and clear display
def matrix_init():
   print("Matrix initialize")

def matrix_write(bits, mode):
    print("Matrix write " + bits)

def matrix_text(message):
    matrix_write(message, "noop")

########### ENCODER1 
def clkClicked(channel):
        global counter
        global step
 
        clkState = GPIO.input(ENCODER_CLK_GPIO)
        dtState = GPIO.input(ENCODER_DTA_GPIO)
 
        if clkState == 0 and dtState == 1:
                counter = counter + step
                print ("Counter ", counter)
                mpcRet = mpcCommand(['mpc', 'volume', '+5'])    
                print("Volume "+str(mpcRet))
 
def dtClicked(channel):
        global counter
        global step
 
        clkState = GPIO.input(ENCODER_CLK_GPIO)
        dtState = GPIO.input(ENCODER_DTA_GPIO)
         
        if clkState == 1 and dtState == 0:
                counter = counter - step
                print ("Counter ", counter)
                mpcRet = mpcCommand(['mpc', 'volume', '-5'])    
                print("Volume "+str(mpcRet))
 
def swClicked(channel):
        global paused
        if (not paused):
          mpcRet = mpcCommand(['mpc', 'play'])    
        else:
          mpcRet = mpcCommand(['mpc', 'stop'])    

        paused = not paused
        print ("Paused ", paused)             

####################################

########### ENCODER2

def clkClicked2(channel):
    global counter2
    global step2

    clkState2 = GPIO.input(ENCODER2_CLK_GPIO)
    dtState2 = GPIO.input(ENCODER2_DTA_GPIO)

    if clkState2 == 0 and dtState2 == 1:
        counter2 = counter2 + step2
        print("Counter2 ", counter2)
        station_up_callback(0)
        #mpcRet = mpcCommand(['mpc', 'volume', '+5'])
        #print("Volume " + str(mpcRet))


def dtClicked2(channel):
    global counter2
    global step2

    clkState2 = GPIO.input(ENCODER2_CLK_GPIO)
    dtState2 = GPIO.input(ENCODER2_DTA_GPIO)

    if clkState2 == 1 and dtState2 == 0:
        counter2 = counter2 - step2
        print("Counter2 ", counter2)
        station_down_callback(0)
        #mpcRet = mpcCommand(['mpc', 'volume', '-5'])
        #print("Volume " + str(mpcRet))


def swClicked2(channel):
    global paused2
    if (not paused2):
        mpcRet = mpcCommand(['mpc', 'play'])
    else:
        mpcRet = mpcCommand(['mpc', 'stop'])

    paused2 = not paused2
    print("Paused2 ", paused2)

####################################


def pir_motion(channel):
    pirData = GPIO.input(PIR_GPIO)
    global countMotion
    countMotion = countMotion + 1
    mpcCommand(['mpc', 'play'])
    #GPIO.remove_event_detect(PIR_GPIO)
    print("Hello!!! " + str(countMotion) + " " + str(pirData))
    global timer
    if (timer != None and timer.is_alive()):
        timer.cancel()
    timer = threading.Timer(20, pir_no_motion) 
    timer.start() 

def pir_no_motion():
    mpcCommand(['mpc', 'stop'])
    print("Goodbye!!! ")
    #GPIO.add_event_detect(PIR_GPIO, GPIO.RISING, callback=pir_motion, bouncetime=300)


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Setup Matrix
    matrix_init()

    matrix_text("Sonda Internet Radio")
    matrix_text("Huntington, NY")

    # Setup volume controls
    #GPIO.setup(VOLUME_DOWN_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.add_event_detect(VOLUME_DOWN_GPIO, GPIO.FALLING, 
    #        callback=volume_down_callback, bouncetime=300)
    
    #GPIO.setup(VOLUME_UP_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.add_event_detect(VOLUME_UP_GPIO, GPIO.FALLING, 
    #        callback=volume_up_callback, bouncetime=300)

    #GPIO.setup(STATION_DOWN_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.add_event_detect(STATION_DOWN_GPIO, GPIO.FALLING,
    #        callback=station_down_callback, bouncetime=300)
    
    #GPIO.setup(STATION_UP_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.add_event_detect(STATION_UP_GPIO, GPIO.FALLING,
    #        callback=station_up_callback, bouncetime=300)

    #ENCODER1 setup
    GPIO.setup(ENCODER_CLK_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(ENCODER_DTA_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(ENCODER_SW_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #get the initial states
    clkLastState = GPIO.input(ENCODER_CLK_GPIO)
    dtLastState = GPIO.input(ENCODER_DTA_GPIO)
    swLastState = GPIO.input(ENCODER_SW_GPIO)
    GPIO.add_event_detect(ENCODER_CLK_GPIO, GPIO.FALLING, callback=clkClicked, bouncetime=300)
    GPIO.add_event_detect(ENCODER_DTA_GPIO, GPIO.FALLING, callback=dtClicked, bouncetime=300)
    GPIO.add_event_detect(ENCODER_SW_GPIO, GPIO.FALLING, callback=swClicked, bouncetime=300)

    #ENCODER2 setup
    GPIO.setup(ENCODER2_CLK_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(ENCODER2_DTA_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.setup(ENCODER2_SW_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #get the initial states
    clkLastState2 = GPIO.input(ENCODER2_CLK_GPIO)
    dtLastState2 = GPIO.input(ENCODER2_DTA_GPIO)
    #swLastState2 = GPIO.input(ENCODER2_SW_GPIO)
    GPIO.add_event_detect(ENCODER2_CLK_GPIO, GPIO.FALLING, callback=clkClicked2, bouncetime=300)
    GPIO.add_event_detect(ENCODER2_DTA_GPIO, GPIO.FALLING, callback=dtClicked2, bouncetime=300)
    #GPIO.add_event_detect(ENCODER2_SW_GPIO, GPIO.FALLING, callback=swClicked2, bouncetime=300)


    mpcRet = mpcCommand(['mpc', '-f', '%position%'])
    print("mpcRet= " + str(mpcRet))
    tokens = str(mpcRet).split()
    print(tokens)
    pound = tokens[1][0:1]
    print(pound)
    if (tokens[1][0:1] == '#'):
       tokens2 = tokens[1].split('/')
       print(tokens2)
       tokens3 = tokens2[0][1:]
       print(tokens3)
       CURRENT_STATION = int(tokens3)
       print("CURRENT_STATION=" + str(CURRENT_STATION))
       paused = True
    else:
       paused = False

    show_number(0,0,CURRENT_STATION)

    #PIR setup
    GPIO.setup(PIR_GPIO, GPIO.IN)
    #GPIO.input(PIR_GPIO)
    #GPIO.add_event_detect(PIR_GPIO, GPIO.BOTH, callback=pir_motion)

    while True:
        i=GPIO.input(26)
        if i==0:                 #When output from motion sensor is LOW
            print("No intruders",i)
            if (playing == True):
                print("Playing stopped")
                mpcCommand(['mpc', 'stop'])    
            playing = False
            time.sleep(10)
        elif i==1:               #When output from motion sensor is HIGH
            print("Intruder detected",i)
            if (playing == False):
                print("Playing")
                mpcCommand(['mpc', 'play'])    
            playing = True
            time.sleep(10)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
