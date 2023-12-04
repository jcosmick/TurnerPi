# TurnerPi
simply turn on a led by a flask app to radiate a fotoresistor to turn on a pc/server

## How to install & run
download everything on your raspberry and run main.py with "python main.py"

## Configuration
* "pcIp": a string with the local pc ip you want to check if it's on
* "gpioPin" an integer of the ping the led is connected to
* "remainOn" an integer to indicate how much time (seconds) the led will stay on after clicking the button on the website
* "timeout" integer to indicate how much time (seconds) to ping every 2 sec if pc turned on
* "port" an integer port where the web app will run
* "host" string ip for flask service to run on - 0.0.0.0 to get accessible from all devices
