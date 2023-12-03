function turnOn(){
    const button = document.getElementById("button");
    if(!button.classList.contains("button-on")){
        button.classList.toggle("button-on")
    }
}