#!/usr/bin/env python
#import utils
#import RPi.GPIO as GPIO
import cv2
import servoStep
import autoCapture
import time

#Motor Initialization
chipMov = servoStep.channels

#Vision Initiation
chipEye = autoCapture.scanSize

print(chipMov.direction)
print("------------------------")
print('CHIPv4B - neoChip V1')

delay_period = 10
frame_skip = 20

# Use GPIO numbering
#GPIO.setmode(GPIO.BCM)

while True:

        print("-----------------")
        print()
#        print("Freeze Num:", chipMov.freezeStep)
        
        chipMov.pulseChange(chipMov.pulseX,chipMov.pulseY)
        time.sleep(delay_period)
        chipMov.servoScanX(frame_skip)       
        
        chipEye.snap('../hold/dst.jpeg')
        
##        cv2.imshow('Chip 4B', chipEye.TEMPIMAGE)
##        cv2.waitKey(1)
##        k = cv2.waitKey(10) & 0xFF
##
##        if k == 32: # Space writes exits
##                print("  ")
##                print('Kill Me')
##                break
##
##        elif k == 9: # Tab writes exits
##                print('Trunc')
##
##        elif k == 27: # Esc writes exits
##                num = 1
##                print(num)
##                break
