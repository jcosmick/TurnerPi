from flask import Flask, render_template
import platform    
import subprocess 
import json
from time import sleep
from gpiozero import LED

config = json.load(open('configuration.json'))
led = LED(config["gpioPin"])


app = Flask(__name__)

def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0

@app.route('/')
def hello():
    hostname = config['pcIp']
    return render_template('index.html', isOn=ping(hostname))

@app.route('/ping')
def pingTest(methods=['GET']):
    hostname = config['pcIp']
    response = {"isOn": ping(hostname)}
    return json.dumps(response)

@app.route('/turnon')
def turnOn(methods=['GET']):
    led.on()
    sleep(config["remainOn"])
    led.off()
    return "ok"

if __name__ == '__main__':
    app.run(port = config["port"], host=config["host"])
