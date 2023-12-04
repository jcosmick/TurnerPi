from flask import Flask, render_template, request
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
    print("pinging: "+host+" with command: "+ ' '.join(command))
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
    print("turnOn request from "+ request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    led.on()
    sleep(config["remainOn"])
    led.off()
    return json.dumps(config["timeout"])

if __name__ == '__main__':
    app.run(port = config["port"], host=config["host"])
