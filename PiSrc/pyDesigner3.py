import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import pyqtSignal, QObject
from PyQt5 import uic
import RPi.GPIO as GPIO
import time

RED = 14
GREEN = 15
BLUE = 18
BUTTON = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup([RED, GREEN, BLUE], GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP)

press_count = 0
prev_input = GPIO.input(BUTTON)

def set_rgb(r=False, g=False, b=False):
        if r:
                GPIO.output(RED, GPIO.LOW)
        else:
                GPIO.output(RED, GPIO.HIGH)
        if g:
                GPIO.output(GREEN, GPIO.LOW)
        else:
                GPIO.output(GREEN, GPIO.HIGH)
        if b:
                GPIO.output(BLUE, GPIO.LOW)
        else:
                GPIO.output(BLUE, GPIO.HIGH)

class GPIOSignalBridge(QObject):
    color_changed = pyqtSignal(str)

bridge = GPIOSignalBridge()

class WindowClass(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = uic.loadUi("design1.ui", self)
        self.press_count = 0
        bridge.color_changed.connect(self.slot1)

        GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=self.gpio_callback, bouncetime=200)

    def gpio_callback(self, channel):
        self.press_count += 1
        if   self.press_count == 1:
            set_rgb(r=True)
            bridge.color_changed.emit("RED")
        elif self.press_count == 2:
            set_rgb(g=True)
            bridge.color_changed.emit("GREEN")
        elif self.press_count == 3:
            set_rgb(b=True)
            bridge.color_changed.emit("BLUE")
        elif self.press_count == 4:
            set_rgb()
            bridge.color_changed.emit("OFF")
            self.press_count = 0

    def slot1(self, color_name):
        self.ui.label.setText(color_name)

    def closeEvent(self, event):
        GPIO.cleanup()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())
