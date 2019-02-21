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

print('------------------------')
print('CHIPv4B - neoChip V1')

#Pull DATE & TIME
#Print into TXT file & save in ../hold
tick = time.asctime(time.localtime(time.time()))
print('Time:', tick)
file = open('%sdata.txt' % chipEye.filePrep,'w') 
file.write('CHIP4')
file.write('\n')
file.write('\n')
#file.next()
file.write('Time Begin:')
file.write('\n')
file.write(tick)
file.close()
##file.write('Series:', chipEye.seriesNum)

delay_period = 3
frame_skip = 15
chipMov.pulseY = 120
num = 0

while True:
        
        chipMov.pulseChange(chipMov.pulseX,chipMov.pulseY)
        chipMov.servoScanX(frame_skip)
        time.sleep(delay_period)
        chipEye.target()
        
        #Print Stuff
        print('--------------------------')
        print("Frame Number:", chipEye.num)
        print('X:', chipMov.pulseX)
        print('Y:', chipMov.pulseY)
        print("---------------")
        print('Target Area:', chipEye.area_tar)
        print('Target X:', chipEye.x_tar)
        print('Target Y:', chipEye.y_tar)

        if chipEye.area_tar > 3000:
                chipEye.snap('../hold/dst.jpeg')
                num = num + 1


        
        #OPENCV_Plot
        cv2.imshow('Chip 4', chipEye.frame)

        k = cv2.waitKey(10) & 0xFF

        if k == 32: # Space writes exits
                print("  ")
                print("---------------")
                print("  ")
                print('Shut Down')
                print("  ")
                print("---------------")
                break
        

        elif k == 9: # Tab writes exits
                print('Trunc')

        elif k == 27: # Esc writes exits
                num = 1
                print(num)
                break

        elif k != 255:
                print('key:',[chr(k)])

tock = time.asctime(time.localtime(time.time()))
file = open('%sdata.txt' % chipEye.filePrep,'a')
file.write('\n')
file.write('\n')
#file.write(chipEye.num)
file.write('Time Over:')
file.write('\n')
file.write(tock)
file.close()

chipEye.cam.close()
cv2.destroyWindow('Chip 4')
