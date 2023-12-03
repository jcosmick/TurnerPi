# TurnerPi
simply turn on a led by a flask app to radiate a fotoresistor to turn on a pc/server

## How to install & run
download everything on your raspberry and run main.py with "python main.py"

## Configuration
"pcIp": a string with the local pc ip you want to check if it's on
"gpioPin" an integer of the ping the led is connected to
"toRemainOn" an integer to indicate how much time (seconds) the led will stay on after clicking the button on the website
