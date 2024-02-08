const key_letters = document.querySelectorAll(".letter");

const white = document.querySelectorAll(".white-key")
const black = document.querySelectorAll(".black-key")


for (const key of white) {
    key.addEventListener('mouseover',DisplayLetters);
    key.addEventListener('mouseout',HideLetters);
}

for (const key of black) {
    key.addEventListener('mouseover',DisplayLetters);
    key.addEventListener('mouseout',HideLetters);
}

function DisplayLetters() {
    for (const letter of key_letters) {

        letter.style.opacity = '100%';
    }
    
}


function HideLetters() {
    for (const letter of key_letters) {
        letter.style.opacity = '0%';
    }
    
}



