const para = document.querySelector(".MButton");
const menu = document.querySelector("#menu-overlay");
const hidden = menu.style.display;
let appear = false;
para.addEventListener('click',DisplayMenu);

function DisplayMenu() {
    menu.setAttribute("id","menu-appear");
    if (appear == false) {
        menu.setAttribute("id","menu-appear");
        appear = true;
    } else {
        appear = false;
        menu.setAttribute("id","menu-overlay");


    }
}