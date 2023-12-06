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
