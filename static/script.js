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

document.addEventListener('DOMContentLoaded', async function() {
    document.body.style="background-color: var(--bs-dark);transition: 0.5s;"
    document.getElementById("break-circle").style ="background-color: var(--bs-dark);transition: 0.5s;"
    const sun = "https://www.uplooder.net/img/image/55/7aa9993fc291bc170abea048589896cf/sun.svg";
    const moon = "https://www.uplooder.net/img/image/2/addf703a24a12d030968858e0879b11e/moon.svg"

    var theme = "dark";
    const root = document.querySelector(":root");
    const container = document.getElementsByClassName("theme-container")[0];
    const themeIcon = document.getElementById("theme-icon");
    const text = document.getElementById("text")
    container.addEventListener("click", setTheme);
    function setTheme() {
        switch (theme) {
        case "dark":
            setLight();
            theme = "light";
            break;
        case "light":
            setDark();
            theme = "dark";
            break;
        }
    }
    function setLight() {
        root.style.setProperty(
        "--bs-dark",
        "white"
        );
        text.classList.remove("text-dark")
        container.classList.remove("shadow-dark");
        setTimeout(() => {
        container.classList.add("shadow-light");
        themeIcon.classList.remove("change");
        }, 300);
        themeIcon.classList.add("change");
        themeIcon.src = sun;
    }
    function setDark() {
        root.style.setProperty("--bs-dark", "#212529");
        container.classList.remove("shadow-light");
        text.classList.add("text-dark")
        setTimeout(() => {
        container.classList.add("shadow-dark");
        themeIcon.classList.remove("change");
        }, 300);
        themeIcon.classList.add("change");
        themeIcon.src = moon;
    }
})
