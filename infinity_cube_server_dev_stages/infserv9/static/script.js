function setColor() {
    let color = document.getElementById("colorPicker").value;
    let r = parseInt(color.substr(1, 2), 16);
    let g = parseInt(color.substr(3, 2), 16);
    let b = parseInt(color.substr(5, 2), 16);

    fetch(`http://192.168.0.157:5000/set_color?r=${r}&g=${g}&b=${b}`)
        .then(response => response.json())
        .then(data => console.log("Color set:", data))
        .catch(error => console.error("Error:", error));
}

function turnOff() {
    fetch(`http://192.168.0.157:5000/off`)
        .then(response => response.json())
        .then(data => console.log("LEDs turned off:", data))
        .catch(error => console.error("Error:", error));
}


function setBrightness() {
    let brightness = document.getElementById("brightness").value;
    document.getElementById("brightnessValue").innerText = brightness;

    fetch(`http://192.168.0.157:5000/set_brightness?brightness=${brightness}`)
        .then(response => response.json())
        .then(data => console.log("Brightness set:", data))
        .catch(error => console.error("Error:", error));
}

function startAnimation(effect) {
    let delay = document.getElementById("delay").value;  // Pobranie wartości z suwaka
    fetch(`http://192.168.0.157:5000/start_animation?effect=${effect}&delay=${delay}`)
        .then(response => response.json())
        .then(data => console.log("Animation started:", data))
        .catch(error => console.error("Error:", error));
}

function updateDelayValue() {
    document.getElementById("delayValue").innerText = document.getElementById("delay").value;
}

document.addEventListener("DOMContentLoaded", function() {
    console.log("Script loaded successfully");
});