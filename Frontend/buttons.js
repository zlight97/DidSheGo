const BACKEND_URL = "http://localhost:5000/";
var jsonWebToken = "This is a test token";
var currentState = 0;

// 0:"loginform",
// 1:"button-displayer"
const stateToDiv = ["loginform", "button-displayer"]
const stateToDis = ["grid",      "block"]

function updateState(newState)
{
    hideDiv(stateToDiv[currentState]);
    currentState = newState;
    showDiv(stateToDiv[newState], stateToDis[newState]);
}

function sendPost(body, responseFunc, url)
{
    body['Access-Token']=  jsonWebToken;
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    xhr.setRequestHeader("Access-Control-Allow-Headers", "x-requested-with");
    xhr.onload = () => responseFunc(xhr);
    xhr.send(JSON.stringify(body));
}
function sendGet(url, responseFunc)
{
    const request = new XMLHttpRequest();
    request.open("GET", url);
    // request.setRequestHeader("Content-Type", "application/json; charset=UTF-8")
    request.setRequestHeader("Access-Token", jsonWebToken);
    request.onreadystatechange = () => responseFunc(request);
    request.send(null);
}



function addButton(name, color, id){
    let elementTag = document.createElement('button');
    let elementText = document.createTextNode(name);
    elementTag.className = color;
    elementTag.id = id; //can use id to refrence which entry
    elementTag.onclick =function() { updateState(0); } //These are set to functions

    elementTag.appendChild(elementText);

    let buttonDisplayer = document.getElementById('button-displayer');
    buttonDisplayer.insertBefore(elementTag, buttonDisplayer.lastChild);
}

function hideDiv(div){
    let x = document.getElementById(div);
    x.style.display = "none";
}
function showDiv(div, display){
    let x = document.getElementById(div);
    x.style.display = display;
}

function login(){
    let username = document.getElementById("username");
    let password = document.getElementById("password");
    if (username === null || password === null)
    {   
        document.getElementById("vaild-pass").innerHTML = "Incorrect Username/Password";
        return false;
    }
    let validpass = password.value

    if (validpass.length <= 8 || validpass.length >= 20) {
        document.getElementById("vaild-pass").innerHTML = "Incorrect Username/Password";
        return false;
    }
    submitLogin(username.value, validpass)
}

function parseSubmitLogin(xhr) {
    if (xhr.readyState == 4 && xhr.status == 200) {
        let resp = JSON.parse(xhr.responseText);
        if (resp.success === true)
        {
            getPets();
            return;
        }
    }
    document.getElementById("vaild-pass").innerHTML = "Incorrect Username/Password";
    console.log(`Error: ${xhr.status}`);
  }

function submitLogin(username, password){
    const body = {
        username: username,
        password: password
      };

    sendPost(body, parseSubmitLogin, BACKEND_URL + "submitlogin");

}

function createPets(pets){
    pets = JSON.parse(pets);
    for (const [key, value] of Object.entries(pets)) {
        console.log(`${key}: ${value}`);
        addButton(key, 'red', key)
      }
    // addButton()
    updateState(1);
}

function getPets(){
    const response = (xhr) => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            resp = xhr.responseText;
            createPets(resp);
            return;
        }
    document.getElementById("vaild-pass").innerHTML = "Incorrect Username/Password";
    };
    sendGet(BACKEND_URL + "getpets",response )
}

function newButton(){
    addButton('poop', 'green', 'testid');
}

function newButton2(id){
    addButton('poop', 'green', id);
}