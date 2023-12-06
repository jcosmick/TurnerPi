from time import sleep
from gpiozero import LED
import json

class LedManager:
    config = json.load(open('configuration.json'))
    def __init__(self) -> None:
        self.led = LED(self.config["gpioPin"])

    def turnOnLed(self):
        self.led.on()
        sleep(self.config["remainOn"])
        self.led.off()