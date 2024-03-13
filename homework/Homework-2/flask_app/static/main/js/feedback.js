const feedback_button = document.querySelector("#Feedback");
const feedback = document.querySelector("#Feedback-Form-Invisible");

//boolean representing if menu pop up has appeared
let appear_form = false;
// Handles clicking menu bar
DisplayForm = function () {
    if (appear_form == false) {
        feedback.setAttribute("id","Feedback-Form-Visible");
        appear_form= true;
    } else {
        appear_form = false;
        feedback.setAttribute("id","Feedback-Form-Invisible");
    }
}

//Adds event listener to menu button
feedback_button.addEventListener('click',DisplayForm);