from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from flask import Flask, Response, render_template, stream_with_context, request
import platform    
import subprocess 
import json
import os
from time import sleep, time
from gpiozero import LED

config = json.load(open('configuration.json'))
led = LED(config["gpioPin"])

app = Flask(__name__)
counter = 0

def isPinging(): return json.load(open('appData.json'))["isPinging"]

def changeIsPinging(var):
    with open('appData.json', 'r') as file:
        data = json.load(file)
    data["isPinging"] = var
    print(str(data))
    with open('appData.json', 'w') as file:
        json.dump(data, file, indent=1)

def changeIsTimeout(var):
    with open('appData.json', 'r') as file:
        data = json.load(file)
    data["isTimeout"] = var
    print(str(data))
    with open('appData.json', 'w') as file:
        json.dump(data, file, indent=1)

def changeIsOn(var):
    with open('appData.json', 'r') as file:
        data = json.load(file)
    data["isOn"] = var
    print(str(data))
    with open('appData.json', 'w') as file:
        json.dump(data, file, indent=2)

def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    isOn = subprocess.call(command) == 0
    changeIsOn(isOn)
    return isOn

def pingLoop(host):
    start_time = time()
    changeIsPinging(True)
    while True:
        if ping(host):
            break
        
        if time() - start_time >= config["timeout"]:
            changeIsTimeout(True)
            break
        
        sleep(2)

    changeIsPinging(False)
    return False


@app.route('/')
def render_homepage():
    return render_template('index.html')

@app.route("/listen")
def listen():

    def respond_to_client():
        while True:
            global counter
            counter += 1
            with open('appData.json' , 'r') as f:
                appData = json.load(f)
            data = json.dumps({"isPinging": appData["isPinging"], "isOn": appData["isOn"], "isTimeout": appData["isTimeout"],"counter":counter})
            yield f"id: 1\ndata: {data}\nevent: online\n\n"
            sleep(1)

    return Response(respond_to_client(), mimetype='text/event-stream')

@app.route('/ping')
def pingTest(methods=['GET']):
    hostname = config['pcIp']
    response = {"isOn": ping(hostname)}
    return json.dumps(response)

@app.route('/turnon')
def turnOn(methods=['GET']):
    with open('appData.json' , 'r') as f:
        isPinging = json.load(f)["isPinging"]

    if isPinging:
        return
    print("turnOn request from "+ request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    changeIsPinging(True)
    changeIsTimeout(False)
    led.on()
    sleep(config["remainOn"])
    led.off()
    pingLoop(config['pcIp'])
    return

if __name__ == '__main__':
    #app.run(port = config["port"], host=config["host"])
    data_to_write = {"isPinging": False,"isOn": False, "isTimeout": False}
    with open('appData.json', 'w') as file:
        json.dump(data_to_write, file, indent=2)
    http_server = WSGIServer((config["host"], config["port"]), app)
    print("started webapp on: "+config["host"]+":"+str(config["port"]))
    http_server.serve_forever()
