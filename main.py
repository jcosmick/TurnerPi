from flask import Flask, render_template, request
import platform    
import subprocess 
import json
from time import sleep, time
from gpiozero import LED

config = json.load(open('configuration.json'))
def isPinging(): return json.load(open('appData.json'))["isPinging"]
#led = LED(config["gpioPin"])


app = Flask(__name__)

def changeAppData(var):
    print("isPinging: "+var)
    appData = open('appData.json', 'w+')
    appData.write(json.dumps({"isPinging" : var}))
    appData.close()

def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    print("pinging: "+host+" with command: "+ ' '.join(command))
    return subprocess.call(command) == 0

def pingLoop(host):
    start_time = time()
    changeAppData(True)
    while True:
        if ping(host):
            changeAppData(False)
            return True
        
        if time() - start_time >= config["timeout"]:
            break
        
        sleep(2)

    changeAppData(False)
    return False


@app.route('/')
def hello():
    return render_template('index.html', isPinging = json.dumps(isPinging()))

@app.route('/ping')
def pingTest(methods=['GET']):
    hostname = config['pcIp']
    response = {"isOn": ping(hostname)}
    return json.dumps(response)

@app.route('/turnon')
def turnOn(methods=['GET']):
    print("turnOn request from "+ request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    if isPinging():
        return json.dumps({"isPinging": isPinging()})
    #led.on()
    sleep(config["remainOn"])
    #led.off()
    pingLoop(config['pcIp'])
    return json.dumps({"isOn":pingLoop(config["pcIp"])})

if __name__ == '__main__':
    app.run(port = config["port"], host=config["host"])
