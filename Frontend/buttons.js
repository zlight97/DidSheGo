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

function hideDiv(div){
    var x = document.getElementById(div);
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
}

function login(){
    var username = document.getElementById("username");
    var password = document.getElementById("password");
    if (username === null || password === null)
    {   
        document.getElementById("vaild-pass").innerHTML = "Incorrect Username/Password";
        return false;
    }
    var validpass = password.value

    if (validpass.length <= 8 || validpass.length >= 20) {
        document.getElementById("vaild-pass").innerHTML = "Incorrect Username/Password";
        return false;
    }
    submitLogin(username.value, validpass)
}
function submitLogin(username, password){
    const url = "http://localhost:5000/submitlogin"

    fetch("http://127.0.0.1:5000/submitlogin", {
    method: "POST",
    body: JSON.stringify({
        userId: 1,
        title: "Fix my bugs",
        completed: false
    }),
    headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE',
        'Access-Control-Allow-Headers': 'Content-Type',
        "Content-type": "application/json; charset=UTF-8"
    }
    })
  .then((response) => response.json())
  .then((json) => console.log(json));


}

function newButton(){
        addButton('poop', 'green', 'testid');
    }

function newButton2(id){
    addButton('poop', 'green', id);
}