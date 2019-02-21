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

#Pull DATE & TIME
#Print into TXT file & save in ../hold
file = open('%sdata.txt' % chipEye.filePrep,'w') 

tick = time.asctime(time.localtime(time.time()))
file.write('CHIP4') 
print('Time:', tick)
file.write("")
file.write(tick)
##file.write('Series:', chipEye.seriesNum) 
 
file.close() 


delay_period = 5
frame_skip = 30

# Use GPIO numbering
#GPIO.setmode(GPIO.BCM)

while True:

        chipMov.pulseY = 120
        chipMov.pulseChange(chipMov.pulseX,chipMov.pulseY)
        chipMov.servoScanX(frame_skip)
        time.sleep(delay_period)
        chipEye.snap('../hold/dst.jpeg')

        
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
