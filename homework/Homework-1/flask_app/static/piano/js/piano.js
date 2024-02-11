
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


const sound = {65:"http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
                87:"http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
                83:"http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
                69:"http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
                68:"http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
                70:"http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
                84:"http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
                71:"http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
                89:"http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
                72:"http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
                85:"http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
                74:"http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
                75:"http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
                79:"http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
                76:"http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
                80:"http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
                59:"http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav",
                186:"http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"};

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
                    59:document.querySelector("#semi"),
                    186:document.querySelector("#semi")};


document.addEventListener('keydown',logKey);
const weseeyou = "weseeyou";
let index = 0;
let awaken = false;
function logKey(e) {
    console.log(awaken);
    if (!awaken) {

    
        const key_code = e.keyCode;

        const audio = new Audio(sound[key_code]);

        if (key_code in black_keys) {
            const key = black_keys[key_code];
            key.style.backgroundColor = '#5A5A5A';
            console.log("black");


        } else if (key_code in white_keys) {
            const key = white_keys[key_code];
            key.style.backgroundColor = '#5A5A5A';
            console.log("white");

        }

        audio.play();
        
        if (e.key === weseeyou[index]) {
            index = index+1
        } else {
            index = 0
        }

        if (index === weseeyou.length) {
            awaken = true;
            console.log("I have awoken!!!");
            const monster = document.querySelector(".image-and-text");
            const piano_instrument = document.querySelector(".piano");
            
            piano_instrument.style.opacity = "0%"
            const monster_audio = new Audio('https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1');   
            monster_audio.play(); 

            monster.style.opacity = "100%";



        }
        


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