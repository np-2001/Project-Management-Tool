// Used to create a user account
accountCreation = function () {
    // package data in a JSON object
    const email = document.querySelector("#email");
    const feedback = document.querySelector("#password");
    // owner@email.com
    // password
    var data_d = {'email': email.value, 'password': feedback.value}
    console.log('data_d', data_d);
    
    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/processsignup",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
              retruned_data = JSON.parse(retruned_data);
              if (retruned_data["success"] === 1) {
                console.log("Valid")
                window.location.href = "/login";

              } else {
                console.log("User Exists");
                const message = document.createElement("p");
                message.textContent = "User already exists. Please choose a different email.";
                const signup_container = document.querySelector("#signup-container")
                message.style.color = "#fff";
                signup_container.appendChild(message);
              }              
            } 
    });
}