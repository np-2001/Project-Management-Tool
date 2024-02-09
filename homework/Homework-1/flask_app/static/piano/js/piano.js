
// const white = document.querySelectorAll(".white-key")
// const black = document.querySelectorAll(".black-key")


// for (const key of white) {
//     key.addEventListener('mouseover',DisplayLetters);
//     key.addEventListener('mouseout',HideLetters);
// }

// for (const key of black) {
//     key.addEventListener('mouseover',DisplayLetters);
//     key.addEventListener('mouseout',HideLetters);
// }


const key_letters = document.querySelectorAll(".letter");

const piano = document.querySelector(".keys")

piano.addEventListener('mouseover',DisplayLetters);
piano.addEventListener('mouseout',HideLetters);

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



//Learned about set from here
//https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set
const black_keys = {87:document.querySelector("#W"),
                    69:document.querySelector("#E"),
                    84:document.querySelector("#T"),
                    89:document.querySelector("#Y"),
                    85:document.querySelector("#U"),
                    79:document.querySelector("#O"),
                    80:document.querySelector("#P")};

const white_keys = {65:document.querySelector("#A"),
                    83:document.querySelector("#S"),
                    68:document.querySelector("#D"),
                    70:document.querySelector("#F"),
                    71:document.querySelector("#G"),
                    72:document.querySelector("#H"),
                    74:document.querySelector("#J"),
                    75:document.querySelector("#K"),
                    76:document.querySelector("#L"),
                    59:document.querySelector("#semi")};


document.addEventListener('keydown',logKey)
function logKey(e) {
    const key_code = e.keyCode;
    if (key_code in black_keys) {
        const key = black_keys[key_code];
        key.style.backgroundColor = '#5A5A5A';
        console.log("black");


    } else if (key_code in white_keys) {
        const key = white_keys[key_code];
        key.style.backgroundColor = '#5A5A5A';
        console.log("white");


    }

    

    

}



document.addEventListener('keyup',logKeyUp)

function logKeyUp(e) {
    const key_code = e.keyCode;
    if (key_code in black_keys) {
        const key = black_keys[key_code];
        key.style.backgroundColor = '#000000';



    } else if (key_code in white_keys) {
        const key = white_keys[key_code];
        key.style.backgroundColor = '#FFFFFF';

    }
}