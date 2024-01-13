function addButton(name, color){
    let elementTag = document.createElement('button');
    let elementText = document.createTextNode(name);
    elementTag.className = color;

    elementTag.appendChild(elementText);

    let buttonDisplayer = document.getElementById('button-displayer');
    buttonDisplayer.appendChild(elementTag)
}

function newButton(){
        addButton('poop', 'yellow-orange');
    }