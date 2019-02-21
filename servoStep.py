# Servo Control
from __future__ import print_function
import time
import wiringpi
 
class servStep:

        # MAX/MIN left&right
        L1=130
        H1=150

        # MAX/MIN up&down
        L2=80
        H2=170

        # initialize servo direction
        pulseX = 140
        pulseY = 140
        direction = 1
        freezeStep = 1
        freeze = 1
        
        def __init__(self, HORIZ, VERT):
                self.chan1=HORIZ
                self.chan2=VERT
                
        def servoDelay(self, DELAY):
                self.delay_period = DELAY

        def pulseChange(self, MOVEX, MOVEY):
                self.pulseX = MOVEX
                self.pulseY = MOVEY
                wiringpi.pwmWrite(self.chan1, self.pulseX) 
                wiringpi.pwmWrite(self.chan2, self.pulseY)

        def servoScanX(self, FREEZE):

                self.freeze = FREEZE
                                
                if self.pulseX <= self.L1:
                        #change_direction left
                        self.direction = 2
                        #print("Left:",self.direction)  
                                
                elif self.pulseX >= self.H1:
                        #change_direction right
                        self.direction = 1
                        #print("Right:",self.direction)

                if self.freezeStep == self.freeze:
                       self.freezeStep = 0

                else:
                        self.freezeStep = self.freezeStep + 1
                        
                if self.freezeStep >= self.freeze:
                        print("---------------")
                        print("")
                        print("-- STEP X --")
                        print("")
                        if self.direction == 2:
                                #motor step left
                                self.pulseX = self.pulseX + 1
                        
                        elif self.direction == 1:
                                #motor step right
                                self.pulseX = self.pulseX - 1
                         
        def servoScanY(self, FREEZEY):

                self.freeze = FREEZEY
                
                if self.pulseY <= self.L1:
                        #change_direction left
                        self.direction = 2
                        print("Up:",self.direction)  
                                
                elif self.pulseY >= self.H1:
                        #change_direction right
                        self.direction = 1
                        print("Down:",self.direction)

                if self.freezeStep == self.freeze:
                       self.freezeStep = 0

                else:
                        self.freezeStep = self.freezeStep + 1
                        
                if self.freezeStep >= self.freeze:
                        print("")
                        print("-- STEP Y --")
                        print("")
                        if self.direction == 2:
                                #motor step left
                                self.pulseY = self.pulseY + 1
                        
                        elif self.direction == 1:
                                #motor step right
                                self.pulseY = self.pulseY - 1
                
#SETUP
channels = servStep(18,19)
pulse_delay = channels.servoDelay(0.1)

#CHECK
print("GPIO1:", channels.chan1) 
print("GPIO2:", channels.chan2)
print("DELAY:", channels.delay_period)
print("")

#MOTORS INITIALIZE
# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()

# set PWM output PINS
wiringpi.pinMode(channels.chan1, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(channels.chan2, wiringpi.GPIO.PWM_OUTPUT)
 
# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
 
# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)
