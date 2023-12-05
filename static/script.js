buttonClasses = ["button-on", "button-clicked"]
serviceUrl = window.location.href
eventSource = new EventSource("/listen")
firstTime = true

function isPressed(buttonClassList = Array){
    return !buttonClasses.some(className => button.classList.contains(className))
}

function textClicked(){
    const text = document.getElementById("text")
    if(text.classList.contains("text-off")){
        buttonClicked();
    }
}

async function buttonClicked(){
    const button = document.getElementById("button");
    if(isPressed(button.classList)){
        turnClicked()
        firstTime = false
        await httpGetAsync(serviceUrl+"turnon")
    }
}

async function turnOnCondition(){
    turnClicked()
    document.getElementById("text").innerHTML = "Checking if server is ON..."
    response = await httpGetAsync(serviceUrl+"ping")
    if(response.isOn){
        turnOn()
    }
    else{
        removeStates();
    }
    return response.isOn
}

function eventListener(){
    eventSource.addEventListener("message", function(e) {
    console.log(e.data)
    }, false)

    eventSource.addEventListener("online", listener, true)
}

var listener = function(e){
    data = JSON.parse(e.data)
    console.log(data)
    if(data.isPinging)
    {
        firstTime = false
        turnClicked()
    }
    else if(data.isOn){
        firstTime = false
        turnOn()
    }
    else if(data.isTimeout && !firstTime){
        turnOff()
    }
    else{
        removeStates()
    }
}

function removeStates(){
    const button = document.getElementById("button");
    const text = document.getElementById("text");

    text.classList.remove("text-on")
    text.classList.remove("text-off")
    text.innerHTML="."

    button.classList.remove("button-off")
    button.classList.remove("button-clicked")
    button.classList.remove("button-on")
}

function turnOn(){
    const button = document.getElementById("button");
    removeStates()
    button.classList.add("button-on")
    
}

function turnOff(){
    const button = document.getElementById("button");
    const text = document.getElementById("text");

    removeStates()

    text.innerHTML = "Server does not respond.\nClick to retry"
    text.classList.add("text-off")
    button.classList.add("button-off")
    
}

function turnClicked(){
    const button = document.getElementById("button");
    const text = document.getElementById("text");
    
    removeStates()

    text.innerHTML = "Turning on the server..."
    button.classList.add("button-clicked")
    text.classList.add("text-on")
}

async function httpGetAsync(url)
{
    return fetch(url)
        .then((response) => response.json())
        .then((responseJson)=>{return responseJson})
}