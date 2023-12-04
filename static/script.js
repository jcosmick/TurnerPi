buttonClasses = ["button-on", "button-clicked"]
serviceUrl = window.location.href

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
        response = await httpGetAsync(serviceUrl+"turnon")
        console.log(response)
        if(response){
            intervalId = setInterval(async function(){
                responsePing = await httpGetAsync(serviceUrl+"ping")
                if(responsePing == "True"){
                    turnOn()
                }
            }, 2000)
            setTimeout(() => {clearInterval(intervalId); turnOff()}, response*1000)
        }
    }
}

function turnOn(){
    const button = document.getElementById("button");
    const text = document.getElementById("text");

    text.classList.remove("text-on")
    text.classList.remove("text-off")
    text.innerHTML=""

    button.classList.remove("button-off")
    button.classList.remove("button-clicked")
    button.classList.add("button-on")
    
}

function turnOff(){
    const button = document.getElementById("button");
    const text = document.getElementById("text");

    text.classList.remove("text-on")
    text.innerHTML = "Server does not respond.\nClick to retry"
    text.classList.add("text-off")

    button.classList.remove("button-on")
    button.classList.remove("button-clicked")
    button.classList.add("button-off")
    
}

function turnClicked(){
    const button = document.getElementById("button");
    const text = document.getElementById("text");

    text.classList.remove("text-off")
    text.innerHTML = "Turning on the server..."
    
    button.classList.remove("button-on")
    button.classList.remove("button-off")

    text.style.opacity = 0.5
    button.classList.add("button-clicked")
    text.classList.add("text-on")
}

async function httpGetAsync(url)
{
    return fetch(url)
        .then((response) => response.json())
        .then((responseJson)=>{return responseJson})
}