let count     = 0
function checkCredentials() {
    // package data in a JSON object
    const email = document.querySelector("#email");
    const feedback = document.querySelector("#password");
    // owner@email.com
    // password
    var data_d = {'email': email.value, 'password': feedback.value}
    console.log('data_d', data_d);
    
    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/processlogin",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
              retruned_data = JSON.parse(retruned_data);
              if (retruned_data["success"] == 1) {
                // document.getElementsByClassName("Login-structure")[0].style.display = "none";
                // document.getElementsByClassName("board-option-structure")[0].style.display = "flex";
                window.location.href = "/login"
                // window.location.href = "/home";
                count = 0;
              } else {
                count += 1
                console.log(count);
              }
            } 
    });
}

function routeToBoardCreation() {
    window.location.href = "/board_creation";
}


