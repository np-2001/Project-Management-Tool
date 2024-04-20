function CreateBoard() {
    // package data in a JSON object
    const boardName = document.querySelector("#board-name");
    const allowedEmails = document.querySelector("#Allowed-Emails");

    var data_d = {'boardName': boardName.value, 'allowedEmails': allowedEmails.value}
    console.log('data_d', data_d);
    
    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/processBoardCreation",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
              retruned_data = JSON.parse(retruned_data);
              console.log(retruned_data)
              if (retruned_data["success"] == 1) {
                new_route = "/board_display/" + retruned_data["id"][0]["COUNT(*)"] 
                window.location.href = new_route
                count = 0;
              } else {
                count += 1
                console.log(count);
              }
            } 
    });
}