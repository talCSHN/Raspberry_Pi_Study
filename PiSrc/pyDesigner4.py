import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import uic
import RPi.GPIO as GPIO

RED, GREEN, BLUE = 14, 15, 18

GPIO.setmode(GPIO.BCM)
GPIO.setup([RED, GREEN, BLUE], GPIO.OUT, initial=GPIO.HIGH)

def set_rgb(r=False, g=False, b=False):
    GPIO.output(RED,   GPIO.LOW if r else GPIO.HIGH)
    GPIO.output(GREEN, GPIO.LOW if g else GPIO.HIGH)
    GPIO.output(BLUE,  GPIO.LOW if b else GPIO.HIGH)

class WindowClass(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi("design1.ui", self)
        self.press_count = 0

        self.ui.btn1.clicked.connect(self.cycle_led)


    def cycle_led(self):
        self.press_count += 1
        if   self.press_count == 1:
            set_rgb(r=True)
            self.ui.label.setText("RED")
        elif self.press_count == 2:
            set_rgb(g=True)
            self.ui.label.setText("GREEN")
        elif self.press_count == 3:
            set_rgb(b=True)
            self.ui.label.setText("BLUE")
        elif self.press_count == 4:
            set_rgb()
            self.ui.label.setText("OFF")
            self.press_count = 0

    def closeEvent(self, event):
        GPIO.cleanup()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WindowClass()
    win.show()
    sys.exit(app.exec_())
