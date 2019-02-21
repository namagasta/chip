#Interface
import sys
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QDialog, QApplication

# Servo Control
import time
import wiringpi

class AppWindow(QDialog):

    # use 'GPIO naming'
    wiringpi.wiringPiSetupGpio()

    chan1=18
    chan2=19

    # set #18 to be a PWM output
    wiringpi.pinMode(chan1, wiringpi.GPIO.PWM_OUTPUT)
    wiringpi.pinMode(chan2, wiringpi.GPIO.PWM_OUTPUT)

    # set the PWM mode to milliseconds stype
    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
     
    # divide down clock
    wiringpi.pwmSetClock(192)
    wiringpi.pwmSetRange(2000)
     
    delay_period = 0.01
    
    
    def btn_clk(self, b, string):
        print(b.text())
        print(type(b.text()))
        
        
        if b.text() == 'Print':
            print(self.lineEdit.text())
        else:
            self.lineEdit.clear()
        print(string)
        

    def v_change(self):
        my_value = str(self.horizontalSlider.value())
        self.lineEdit.setText(my_value)
        wiringpi.pwmWrite(self.chan1, int(my_value))
        #time.sleep(self.delay_period)
        my_value2 = str(self.horizontalSlider_2.value())
        self.lineEdit_2.setText(my_value2)
        wiringpi.pwmWrite(self.chan2, int(my_value2))

    def __init__(self):
        super().__init__()
        uic.loadUi('slider.ui', self)
##        self.pushButton.clicked.connect(lambda: self.pressedOnButton())
##        self.pushButton_2.clicked.connect(lambda: self.pressedOffButton())
        self.pushButton.clicked.connect(lambda: self.btn_clk(self.pushButton, 'Grind'))
        self.pushButton_2.clicked.connect(lambda: self.btn_clk(self.pushButton_2, 'Axe'))
        self.horizontalSlider.valueChanged.connect(self.v_change)
        self.horizontalSlider_2.valueChanged.connect(self.v_change)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())

