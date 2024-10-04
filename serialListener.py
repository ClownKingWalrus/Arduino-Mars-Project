import serial
import time
import cv2 #imagae library
import pygame #mmusic library
import audioread
# pygame.mixer.music.load("civil-defense-siren-128262.mp3")
# pygame.mixer.music.set_volume(.7)
# pygame.mixer.music.play()

locker = False

#inilize the mixer for sound
pygame.mixer.init()

#inilize the images to show
happyMars = cv2.imread('images.jfif')
mediumMars = cv2.imread('Concept_Mars_colony-1553x1200.jpg')
madMars = cv2.imread('mars panik.JPG')

#initlize timer which gets seconds since epoch
seconds = time.time()
happytimer = 0
notSoHappyTimer = 0
madMarsTimer = 0

#total time of each song
with audioread.audio_open('good-morning-upbeat-happy-ukulele-244395.wav') as f:
    happyMarsSongLenth = f.duration

with audioread.audio_open('In the end - Linkin Park (with) (1).wav') as f:
    mediumMarsSongLength = f.duration


with audioread.audio_open('civil-defense-siren-128262.wav') as f:
    madMarsSongLength = f.duration

if happyMars is None or mediumMars is None or madMars is None:
    exit('failed to load images')

try:
    fabkit = serial.Serial('COM4', 9600) #ensure on right comport
except:
    print('failed to connect')
    exit()

# line = int(input("enter a number"))
while True:
    battery = fabkit.readline().decode().strip()
    print(battery)
    cv2.destroyAllWindows()

    #ensure the current timers are not more than the song lengths
    if (happytimer >= happyMarsSongLenth):
        happytimer = 0

    elif (notSoHappyTimer >= mediumMarsSongLength):
        notSoHappyTimer = 0

    elif (madMarsTimer >= madMarsSongLength):
        madMarsTimer = 0

    if battery > str(50).encode():
        locker = True
        cv2.imshow('Happy Moments', happyMars)
        cv2.waitKey(1000)
        pygame.mixer.music.load("good-morning-upbeat-happy-ukulele-244395.wav")
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(1, happytimer, 1000)
        seconds = time.time() #get start time
        while locker == True:
            battery = fabkit.readline()
            print(battery)
            # line = int(input("enter a number"))
            if battery <= str(50).encode():
                pygame.mixer.music.fadeout(1000)
                happytimer = (time.time() + happytimer) - seconds #get the current amount of time passed since song started
                locker = False

    elif battery > str(20).encode() and battery <= str(50).encode():
        locker = True
        cv2.imshow('not so happy moments', mediumMars)
        cv2.waitKey(1000)
        pygame.mixer.music.load("In the end - Linkin Park (with) (1).wav")
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(1, notSoHappyTimer, 1000)
        seconds = time.time() #get start time
        while locker == True:
            battery = fabkit.readline()
            print(battery)
            # line = int(input("enter a number"))
            if battery < str(20).encode() or battery > str(50).encode():
                pygame.mixer.music.fadeout(1000)
                notSoHappyTimer = (time.time() + notSoHappyTimer) - seconds #get the current amount of time passed since song started
                locker = False

    elif battery <= str(20).encode():
        locker = True
        cv2.imshow('DANGER MOMENTS', madMars)
        cv2.waitKey(1000)
        pygame.mixer.music.load("civil-defense-siren-128262.wav")
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(1, madMarsTimer, 1000)
        seconds = time.time() #get start time
        while locker == True:
            battery = fabkit.readline()
            print(battery)
            # line = int(input("enter a number"))
            if battery >= str(20).encode():
                pygame.mixer.music.fadeout(1000)
                madMarsTimer = (time.time() + madMarsTimer) - seconds #get the current amount of time passed since song started
                locker = False

    # print(line)
    # if (line == 'ENDING SERIAL\r\n'):
    #     fabkit.flushInput()
    #     fabkit.flushOutput()
    #     fabkit.close()
    #     False