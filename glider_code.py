from gpiozero import LED
import pygame
import time
import random


led = LED(17)

#initialize pygame mixer
pygame.mixer.init()

soundfile = '/home/test/glidertestcode/M00188(frankie).WAV'
sound = pygame.mixer.Sound(soundfile)

def playlightsound():

    led.on
    sound.play()
   
    led.off
   
   
#program runs for 5 mins

end_time = time.time()+300


while time.time() < end_time:
    interval = random.randint(1,30)
    time.sleep(interval)
    playlightsound()