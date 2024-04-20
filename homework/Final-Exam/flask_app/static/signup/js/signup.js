function accountCreation() {
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
              if (retruned_data["success"] == 1) {
                console.log("Valid")
                window.location.href = "/login";

              } else {
                console.log("Incorrect signup");
              }              
            } 
    });
}