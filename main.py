from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from flask import Flask, Response, render_template, request
import platform    
import subprocess 
import json
from time import sleep, time
from service.fileService import *
from service.ledService import LedManager

config = json.load(open('configuration.json'))
app = Flask(__name__)

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
            appData = loadAppData()
            data = json.dumps({"isPinging": appData["isPinging"], "isOn": appData["isOn"], "isTimeout": appData["isTimeout"]})
            yield f"id: 1\ndata: {data}\nevent: online\n\n"
            sleep(1)

    return Response(respond_to_client(), mimetype='text/event-stream')

@app.route('/ping')
def pingTest(methods=['GET']):
    response = {"isOn": ping(config['pcIp'])}
    return json.dumps(response)

@app.route('/turnon')
def turnOn(methods=['GET']):
    if isPinging() or isOn():
        return 'alredy pressed', 200
    print("turnOn request from "+ request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    changeIsPinging(True)
    changeIsTimeout(False)
    LedManager().turnOnLed()
    pingLoop(config['pcIp'])
    return '', 200

if __name__ == '__main__':
    #app.run(port = config["port"], host=config["host"])
    data_to_write = {"isPinging": False,"isOn": False, "isTimeout": False}
    createAppDataFile(data_to_write)
    http_server = WSGIServer((config["host"], config["port"]), app)
    print("started webapp on: "+config["host"]+":"+str(config["port"]))
    http_server.serve_forever()
