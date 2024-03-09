const para = document.querySelector(".MButton");
const menu = document.querySelector("#menu-overlay");
const hidden = menu.style.display;

//boolean representing if menu pop up has appeared
let appear = false;



// Handles clicking menu bar
DisplayMenu = function () {
    if (appear == false) {
        menu.setAttribute("id","menu-appear");
        appear = true;
    } else {
        appear = false;
        menu.setAttribute("id","menu-overlay");


    }
}

//Adds event listener to menu button
para.addEventListener('click',DisplayMenu);
