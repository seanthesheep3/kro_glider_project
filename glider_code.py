from gpiozero import LED
import pygame
import time
import datetime
import random
from enum import Enum
import logging
import sys

#Define Speaker ENUM
class Side(Enum):
    LEFT = 1
    RIGHT = 2

def initializeLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    log_file_name = datetime.datetime.now().strftime('glider_log_%Y_%m_%d_%H_%M.log')
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)
    return logger


def playLightAndSound(chosen_led, chosen_speaker):
    chosen_led.on
    chosen_speaker.play()
    chosen_led.off

def chooseRandomSide():
    rand_side = random.randint(1,2)
    if(rand_side == 1):
        result = Side.LEFT
    else:
        result = Side.RIGHT

    return result


#function to perform the actual test
def runTest(test_endtime, max_interval):
    start_time = datetime.datetime.now()
    logger.info("Test end time is: " + str(datetime.datetime.fromtimestamp(test_endtime).strftime('%c')))
    #logger.info("Test interval is: " + interval + " seconds")
    logger.info("Now beginning test! Time is: " + str(start_time))
    while time.time() < test_endtime:
        interval = random.randint(1,max_interval)

        #sleep for random internval (between 1 and maximum interval)
        time.sleep(interval)

        #choose the random side to play the Sound and LED from
        random_side = chooseRandomSide()
        if(random_side == Side.LEFT):
            chosen_led = left_led
            chosen_speaker = left_speaker
            logger.info("Playing sound to LEFT speaker! Time is: " + str(datetime.datetime.now()))
        else:
            chosen_led = right_led
            chosen_speaker = right_speaker
            logger.info("Playing sound to RIGHT speaker! Time is: " + str(datetime.datetime.now()))

        #actually play the light/sound
        playLightAndSound(chosen_led, chosen_speaker)


#initialize pygame mixer
def initializeSound():
    pygame.mixer.init()
    soundfile = '/home/test/kro_glider_project/M00188(frankie).WAV'
    sound = pygame.mixer.Sound(soundfile)
    return sound

def initializeLED(GPIO_PIN):
    #create LED handles
    led = LED(GPIO_PIN)
    return led

#create logger object for logging to file
logger = initializeLogger()
#set program to run for 5 mins
SECONDS_PER_MIN = 60
TEST_NUM_MINUTES = 5
GPIO_PIN_LED_LEFT = 17
GPIO_PIN_LED_RIGHT = 18 #just guessing here
MAX_INTERVAL_SEC = 30
end_time = time.time()+ (TEST_NUM_MINUTES * SECONDS_PER_MIN)
left_speaker = initializeSound()
right_speaker = initializeSound()
left_led = initializeLED(GPIO_PIN_LED_LEFT)
right_led = initializeLED(GPIO_PIN_LED_RIGHT)
#so you can dynamically change the time and interval
runTest(end_time, MAX_INTERVAL_SEC)

#TODO: figure out how to play out to two different speakers.
#1st idea: modify .WAV file so that one side is completely "left balanced" and the other is "right balanced"
#then save two copies. One file will only play out of the left side speaker, the other will only do the right

