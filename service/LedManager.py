from time import sleep
from gpiozero import LED
import json

class LedManager:
    def __init__(self, gpioPin: int, remainOn: int) -> None:
        self.led:LED = LED(gpioPin)
        self.remainOn:int = remainOn

    def turnOnLed(self):
        self.led.on()
        sleep(self.remainOn)
        self.led.off()