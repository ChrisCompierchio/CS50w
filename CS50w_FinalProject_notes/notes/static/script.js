
let counter = 0;
let dragged_id = ""
let color = ""
let drop_id = ""

function selected(note_color){

    color = note_color;
    dragged_id = "new note";
    const new_note = document.querySelector(`#${note_color}`).cloneNode(true);
    const dragged_note = event.target;

    new_note.addEventListener('dragstart', function(){
        event.dataTransfer.setData('text/plain', new_note.class);
    });

    full_containers = document.querySelectorAll('.full');

    full_containers.forEach(function(element){
        element.removeEventListener('dragover', dragOver);
    });

    empty_containers = document.querySelectorAll('.empty');

    empty_containers.forEach(function(element){
        if (counter == 0){

            element.addEventListener('dragover', dragOver);

            element.addEventListener('drop', drop);

            element.addEventListener('dragleave', function(){
                element.classList.remove('change-border');
            });

        };

    });

    counter = counter + 1;
}

function dragOver(){
    if (dragged_id == "new note"){
        event.preventDefault();
        event.target.classList.add('change-border');
    }

}

function drop(){
    drop_id = event.target.id;

    event.target.classList.add(`${color}`);
    event.target.classList.remove('change-border');
    event.target.classList.remove('empty');
    event.target.classList.add('full');

    var pin_div = document.createElement("div");

    pin_div.classList.add('pin-div');
    pin = document.createElement("img");
    pin.src = "static/img/pin.png";
    pin.id = 'pin';
    pin.classList.add('pin');
    let x = (event.target.getBoundingClientRect().left / 2) - 5;
    let y = event.target.getBoundingClientRect().top - 250;


    pin_div.appendChild(pin);
    event.target.appendChild(pin_div);

    new_text = document.createElement("div");

    new_text.classList.add("new-text");

    event.target.appendChild(new_text);

    new_area = document.createElement("textarea");

    new_area.classList.add("new-area");
    new_area.placeholder = "Enter note text here";

    new_text.addEventListener("keypress", function(){
        if (event.key == 'Enter'){
            text = new_area.value;
            new_text.innerHTML = "";
            new_text.innerHTML = text;

            console.log(drop_id);
            document.querySelector(`#${drop_id}`).addEventListener('click', deleteItem);
            document.querySelector(`#${drop_id}`).removeAttribute("onclick");

            fetch(`/new_note`, {
                method: 'POST',
                body: JSON.stringify({
                    content: text,
                    position: parseInt(drop_id.substring(1)),
                    color: document.querySelector(`.${color}-note`).style.backgroundColor
                })
            });
        }
    })


    new_text.appendChild(new_area);
}

function deleteItem(){

    document.getElementById(`${drop_id}`).innerHTML = "";
    document.getElementById(`${drop_id}`).removeAttribute("style");
    document.getElementById(`${drop_id}`).classList.remove(`${color}`);
    document.getElementById(`${drop_id}`).classList.add('empty');
    document.getElementById(`${drop_id}`).classList.remove('full');

    console.log(drop_id.substring(1));
    fetch(`/deleteNote/${parseInt(drop_id.substring(1))}`);

    document.getElementById(`${drop_id}`).removeEventListener('click', deleteItem);
}

function deleteOldItem(noteId){
    colors = ['blue', 'green', 'yellow', 'pink', 'white', 'purple'];
    document.getElementById(`a${noteId}`).innerHTML = "";
    document.getElementById(`a${noteId}`).removeAttribute("style");
    for (color in colors){
        document.getElementById(`a${noteId}`).classList.remove(`${color}`);
    }
    document.getElementById(`a${noteId}`).classList.add('empty');
    document.getElementById(`a${noteId}`).classList.remove('full');

    fetch(`/deleteNote/${parseInt(noteId)}`);

    document.getElementById(`a${noteId}`).removeEventListener('click', deleteItem);
    document.getElementById(`a${noteId}`).removeAttribute("onclick");
}
