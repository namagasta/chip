#!/usr/bin/env python
#import utils
#import RPi.GPIO as GPIO
from __future__ import print_function
import cv2
import servoStep
import autoCapture
import time


#Motor Initialization
chipMov = servoStep.channels

#Vision Initiation
chipEye = autoCapture.scanSize

print(chipMov.direction)
print('------------------------')
print('CHIPv4B - neoChip V1')

delay_period = 1
frame_skip = 5

# Use GPIO numbering
#GPIO.setmode(GPIO.BCM)

while True:

        
        chipMov.pulseChange(chipMov.pulseX,chipMov.pulseY)
        time.sleep(delay_period)
        chipMov.servoScanX(frame_skip)       
        chipEye.snap('../hold/dst.jpeg')
        chipMov.pulseY = 120
        
        #Print Stuff
        print('--------------------------')
        print("Frame Number:", chipEye.num)
        print('X:',chipMov.pulseX)
        print('Y:',chipMov.pulseY)

        
        #OPENCV_Plot
        cv2.imshow('Chip 4', chipEye.dst)
        cv2.waitKey(delay_period)

        k = cv2.waitKey(10) & 0xFF

        if k == 32: # Space writes exits
                print("  ")
                print('Kill Me')
                break

        elif k == 9: # Tab writes exits
                print('Trunc')

        elif k == 27: # Esc writes exits
                num = 1
                print(num)
                break
        
chipEye.cam.close()
cv2.destroyWindow('Chip 4')
