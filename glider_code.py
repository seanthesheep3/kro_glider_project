from gpiozero import LED
import argparse
import pyaudio
import wave
import time
import datetime
import random
from enum import Enum
import logging
import sys

SOUND_FILE = 'M00188(frankie).WAV'
LEFT_SPEAKER_DEV_ID = 10
RIGHT_SPEAKER_DEV_ID = 10
SECONDS_PER_MIN = 60
TEST_NUM_MINUTES = 5
GPIO_PIN_LED_LEFT = 17
GPIO_PIN_LED_RIGHT = 18 #just guessing here
MAX_INTERVAL_SEC = 30


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

def listAudioDevices():
    """List all available audio output devices."""
    p = pyaudio.PyAudio()
    print("Available audio devices:")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        print(f"Device ID {i}: {device_info['name']}")
    p.terminate()

def playAudio(file_path, device_id):
    """Play a .WAV file on a specific audio device."""
    # Open the WAV file
    wf = wave.open(file_path, 'rb')

    # Set up the PyAudio stream
    p = pyaudio.PyAudio()
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
        output_device_index=device_id
    )

    # Read and play audio data in chunks
    chunk_size = 1024
    data = wf.readframes(chunk_size)
    while data != '':
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Cleanup
    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()

def playLightAndSound(chosen_led, chosen_speaker_dev_id, sound_file):
    chosen_led.on
    playAudio(sound_file, chosen_speaker_dev_id)
    chosen_led.off

def chooseRandomSide():
    rand_side = random.randint(1,2)
    if(rand_side == 1):
        result = Side.LEFT
    else:
        result = Side.RIGHT

    return result


#function to perform the actual test
def runTest(test_endtime, max_interval, sound_file, left_led, right_led, logger):
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info("Test end time is: \t\t" + str(datetime.datetime.fromtimestamp(test_endtime).strftime('%Y-%m-%d %H:%M:%S')))
    #logger.info("Test interval is: " + interval + " seconds")
    logger.info("Now beginning test! Time is: \t" + str(start_time))
    while time.time() < test_endtime:
        interval = random.randint(1,max_interval)

        #sleep for random interval (between 1 and maximum interval)
        logger.info("Interval is " + str(interval) + " seconds. Waiting...")
        time.sleep(interval)

        #choose the random side to play the Sound and LED from
        random_side = chooseRandomSide()
        if(random_side == Side.LEFT):
            chosen_led = left_led
            chosen_speaker_dev_id = LEFT_SPEAKER_DEV_ID
            logger.info("Playing sound to LEFT speaker! Time is: " + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        else:
            chosen_led = right_led
            chosen_speaker_dev_id = RIGHT_SPEAKER_DEV_ID
            logger.info("Playing sound to RIGHT speaker! Time is: " + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        #actually play the light/sound
        playLightAndSound(chosen_led, chosen_speaker_dev_id, sound_file)


def initializeLED(GPIO_PIN):
    #create LED handles
    led = LED(GPIO_PIN)
    return led
    print("")

def main():

    parser = argparse.ArgumentParser(description="Sugar Glider Experiment Script.")
    #parser.add_argument('-h', action='store_true', help='Display usage information.')
    parser.add_argument('--list-audio-devices', action='store_true', help='List available audio devices.')

    args = parser.parse_args()

    #if args.h:
    #    print("glider_code.py [--list-audio-devices] or [-h] ")
    if args.list_audio_devices:
        print("Listing audio devices: ")
        listAudioDevices()
        quit()
    else:
        print("Run the script with -h for more information.")

    #create logger object for logging to file
    logger = initializeLogger()
    #set program to run for 5 mins
    end_time = time.time()+ (TEST_NUM_MINUTES * SECONDS_PER_MIN)
    left_led = initializeLED(GPIO_PIN_LED_LEFT)
    right_led = initializeLED(GPIO_PIN_LED_RIGHT)

    logger.info("Test Duration (mins): \t" + str(TEST_NUM_MINUTES))
    logger.info("Sound File: " + str(SOUND_FILE))
    logger.info("Left Speaker Device ID: \t" + str(LEFT_SPEAKER_DEV_ID))
    logger.info("Right Speaker Device ID:\t" + str(RIGHT_SPEAKER_DEV_ID))
    #so you can dynamically change the time and interval
    runTest(end_time, MAX_INTERVAL_SEC, SOUND_FILE, left_led, right_led, logger)

if __name__ == "__main__":
    main()