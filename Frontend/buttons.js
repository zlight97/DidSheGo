function addButton(name, color, id){
    let elementTag = document.createElement('button');
    let elementText = document.createTextNode(name);
    elementTag.className = color;
    elementTag.id = id //can use id to refrence which entry
    elementTag.onclick =function() { newButton2("test2"); } //These are set to functions

    elementTag.appendChild(elementText);

    let buttonDisplayer = document.getElementById('button-displayer');
    buttonDisplayer.appendChild(elementTag)
}

function newButton(){
        addButton('poop', 'green', 'testid');
    }

function newButton2(id){
    addButton('poop', 'green', id);
}