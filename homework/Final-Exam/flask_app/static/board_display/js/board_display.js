//Citation:
//https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/drag_event
let CardType = '';
const CreateCardPopup = document.querySelector("#Card-Popup");
const CreateEditCardPopup = document.querySelector("#Card-Edit-Popup");
const Chat = document.querySelector("#Chat");

let CurrentEditedCardId = '';

//Makes card creation visible
CreateCard = function(Column) {
    CardType = Column;
    CreateCardPopup.setAttribute("class","Card-Creation-Structure Card-Creation-Design");
    
}

//Hides card creation pop up
HideCard = function() {
    CreateCardPopup.setAttribute("class","invisible");
}

//Hides card edit pop up
HideEditCard = function() {
    CreateEditCardPopup.setAttribute("class","invisible");
}

// Handles submitting card creation
SubmitCard = function(board_id) {
    const CardName = document.querySelector("#New-Card-Name");
    const CardBody = document.querySelector("#New-Card-Body");

    var data_d = {'CardName': CardName.value, 'CardBody': CardBody.value, 'CardType': CardType, 'BoardId':board_id};
    console.log('data_d', data_d);
    
    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/processCardCreation",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
              retruned_data = JSON.parse(retruned_data);
              console.log(retruned_data);
              // Need to use sockets to update without refresh

            } 
    });
}

//Handles deletion of card
DeleteCard = function(card_id) {
    console.log(card_id);
    console.log("test");
    var data_d = {'CardId' : card_id};
    jQuery.ajax({
        url: "/processCardDeletion",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
                retruned_data = JSON.parse(retruned_data);
                console.log(retruned_data);
                // Need to use sockets to update without refresh
            } 
    });

}

//Joining chatroom
JoinChat = function(board_id) {
    Chat.setAttribute("class","Card-Creation-Structure Card-Creation-Design");
    socket.emit('joined', board_id);
}

//Leaving chatroom
CloseChat = function(board_id) {
    Chat.setAttribute("class","invisible");
    socket.emit('leave',board_id);
}

//Submitting chatroom
SubmitMessage = function(board_id) {
    const message_container = document.querySelector("#message-container");
    let message = message_container.value;
    socket.emit('message',board_id,message);
}

//Handles the start of a card edit
StartEditCard = function(card_id) {
    CurrentEditedCardId = card_id;
    CreateEditCardPopup.setAttribute("class","Card-Creation-Structure Card-Creation-Design");
    let edit_cards = document.querySelectorAll('.Card-Structure');
    let edit_card;
    
    for (let card of edit_cards) {
        if (card.id == card_id) {
            edit_card = card;
            break;
        }
    }

    let body = edit_card.getElementsByClassName("Card-Body-Structure")[0];
    edit_body = document.querySelector('#Edit-Card-Body');
    edit_body.value = body.innerText;

}

//Handles when card edit is done
EditCard = function() {
    console.log(CurrentEditedCardId);
    const CardText = document.querySelector("#Edit-Card-Body");
    var data_d = {'CardId' : CurrentEditedCardId, 'CardText':CardText.value};
    console.log(data_d);
    jQuery.ajax({
        url: "/processCardEdit",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
                retruned_data = JSON.parse(retruned_data);
                console.log(retruned_data);
                // Need to use sockets to update without refresh
            } 
    });

}


// Handles enter button being pressed when editing card
Enter = function(event){
    if (event.key === 'Enter') {
        event.preventDefault();
        EditCard();
    }
}

const EditCardPopup = document.getElementById('Edit-Card-Body');
EditCardPopup.addEventListener('keydown', Enter);





//Test function for dragging
dragging = function(event) {
    console.log("I'm moving!!!!");
}

//Handles when dragging starts
dragstart = function(event) {
    dragged = event.target;
    event.target.classList.add("dragging");
}

//Handles animation when dragging ends
dragend = function(event) {
    event.target.classList.remove("dragging");
}


//Function for when dragging over column
DragOver = function(event) {
  event.preventDefault();
}

//Handles when you drag a card onto a column
DragEnter = function(event) {
  if (event.target.classList.contains("Card-List-Structure")) {
    event.target.classList.add("dragover");
  }
}

//Handles when leaving column
DragLeave = function(event) {
  if (event.target.classList.contains("Card-List-Structure")) {
    event.target.classList.remove("dragover");
  }
}

//Handles dropping card onto column
Drop = function(event) {
  event.preventDefault();
  if (event.target.classList.contains("Card-List-Structure")) {
    
    columns[0].classList.remove("dragover");
    columns[1].classList.remove("dragover");
    columns[2].classList.remove("dragover");

    event.target.appendChild(dragged);
    const targetId = event.target.id;
    let NewColumn = "";
    let card_id = dragged.id;
    if (targetId === "ToDoColumn") {
        NewColumn = "ToDo";
    } else if (targetId === "DoingColumn") {
        NewColumn = "Doing";
    } else {
        NewColumn = "Completed";
    }
    var data_d = {'CardId' : card_id, 'NewColumn':NewColumn};
    jQuery.ajax({
        url: "/processCardMovement",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
                console.log("moved");
                retruned_data = JSON.parse(retruned_data);
                console.log(retruned_data);
            } 
    });
  }
}

//All cards
let cards = document.querySelectorAll('.Card-Structure');
let dragged = "";
for (let card of cards) {
    card.addEventListener('drag',dragging);
    card.addEventListener('dragstart',dragstart);
    card.addEventListener('dragend',dragend);
}


//Now I need to add event listeners to each column of the trello board:
let columns  = document.querySelectorAll('.DropColumn');

for (let column of columns) {
    column.addEventListener("dragover", DragOver, false);
    column.addEventListener("dragenter", DragEnter);
    column.addEventListener("dragleave", DragEnter);
    column.addEventListener("drop",Drop);
}
