//Citation:
//https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/drag_event
let CardType = '';
const CreateCardPopup = document.querySelector("#Card-Popup");
const CreateEditCardPopup = document.querySelector("#Card-Edit-Popup");

let CurrentEditedCardId = '';
// const CreateCardButton = document.querySelector("")
function CreateCard(Column) {
    CardType = Column
    CreateCardPopup.setAttribute("class","Card-Creation-Structure Card-Creation-Design");
    
}

function HideCard() {
    CreateCardPopup.setAttribute("class","invisible");
}

function HideEditCard() {
    CreateEditCardPopup.setAttribute("class","invisible");
}

function SubmitCard(board_id) {
    const CardName = document.querySelector("#New-Card-Name");
    const CardBody = document.querySelector("#New-Card-Body");

    var data_d = {'CardName': CardName.value, 'CardBody': CardBody.value, 'CardType': CardType, 'BoardId':board_id}
    console.log('data_d', data_d);
    
    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/processCardCreation",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
              retruned_data = JSON.parse(retruned_data);
              console.log(retruned_data)
              // Need to use sockets to update without refresh

            } 
    });
}

function DeleteCard(card_id) {
    console.log(card_id)
    console.log("test")
    var data_d = {'CardId' : card_id}
    jQuery.ajax({
        url: "/processCardDeletion",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
                retruned_data = JSON.parse(retruned_data);
                console.log(retruned_data)
                // Need to use sockets to update without refresh
            } 
    });

}

function StartEditCard(card_id) {
    CurrentEditedCardId = card_id;
    CreateEditCardPopup.setAttribute("class","Card-Creation-Structure Card-Creation-Design");

}

function EditCard() {
    console.log(CurrentEditedCardId)
    const CardText = document.querySelector("#Edit-Card-Body");
    var data_d = {'CardId' : CurrentEditedCardId, 'CardText':CardText.value}
    console.log(data_d)
    jQuery.ajax({
        url: "/processCardEdit",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
                retruned_data = JSON.parse(retruned_data);
                console.log(retruned_data)
                // Need to use sockets to update without refresh
            } 
    });

}


const EditCardPopup = document.getElementById('Edit-Card-Body')
EditCardPopup.addEventListener('keydown', Enter)

function Enter(event){
    if (event.key === 'Enter') {
        event.preventDefault();
        EditCard();
    }
}



//All cards
let cards = document.querySelectorAll('.Card-Structure');
let dragged;
for (let card of cards) {
    card.addEventListener('drag',dragging);
    card.addEventListener('dragstart',dragstart);
    card.addEventListener('dragend',dragend);
}

function dragging(event) {
    console.log("I'm moving!!!!");
}

function dragstart(event) {
    dragged = event.target;
    event.target.classList.add("dragging");
}

function dragend(event) {
    event.target.classList.remove("dragging");
}

//Now I need to add event listeners to each column of the trello board:
let columns  = document.querySelectorAll('.DropColumn');

for (let column of columns) {
    column.addEventListener("dragover", DragOver, false);
    column.addEventListener("dragenter", DragEnter);
    column.addEventListener("dragleave", DragEnter);
    column.addEventListener("drop",Drop);
}

function DragOver(event) {
  event.preventDefault();
}

function DragEnter(event) {
  if (event.target.classList.contains("Card-List-Structure")) {
    event.target.classList.add("dragover");
  }
}

function DragLeave(event) {
  if (event.target.classList.contains("Card-List-Structure")) {
    event.target.classList.remove("dragover");
  }
}

function Drop(event) {
  event.preventDefault();
  if (event.target.classList.contains("Card-List-Structure")) {
    
    columns[0].classList.remove("dragover");
    columns[1].classList.remove("dragover");
    columns[2].classList.remove("dragover");

    event.target.appendChild(dragged);
    const targetId = event.target.id;
    let NewColumn;
    let card_id = dragged.id;
    if (targetId == "ToDoColumn") {
        NewColumn = "ToDo";
    } else if (targetId == "DoingColumn") {
        NewColumn = "Doing";
    } else {
        NewColumn = "Completed";
    }
    var data_d = {'CardId' : card_id, 'NewColumn':NewColumn}
    jQuery.ajax({
        url: "/processCardMovement",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
                console.log("moved")
                retruned_data = JSON.parse(retruned_data);
                console.log(retruned_data)
            } 
    });
  }
}
