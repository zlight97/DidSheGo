const BACKEND_URL = "http://localhost:5000/";
var jsonWebToken = "This is a test token";
var currentState = 0;
var petSelected = '';
var allPets = null;

// 0:"loginform",
// 1:"button-displayer"
const stateToDiv = ["loginform", "button-displayer", "button-displayer"]
const stateToDis = ["grid",      "block",            "block"]

function logOut()
{
    document.getElementById("vaild-pass").innerHTML = ""
    clearButtons()
    allPets = null;
    petSelected = '';
    jsonWebToken = '';
    updateState(0)
}

function swapPage(newState)
{
    hideDiv(stateToDiv[currentState]);
    showDiv(stateToDiv[newState], stateToDis[newState]);
    currentState = newState
}

function updateState(newState)
{
    swapPage(newState)
    switch(newState)
    {
        case 0:
            
            break;
        case 1:
            clearButtons();
            petSelected = ''
            drawPets();
            break;
        case 2:
            clearButtons();
        default:
            break;
    }
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

function drawActions(petName){
    if(allPets === null)
    {
        getPets()
        return
    }
    let selected = allPets[petName]
    for (const key of selected) {
        addActionButton(key[0], key[1], key[2])
      }
}

function selectPet(name){
    updateState(2);
    petSelected = name
    drawActions(petSelected)
}

function sendTime(entryId)
{
    console.log(entryId)
    const time = Date.now() / 1000;
    const body = {
        auth: jsonWebToken,
        time: time,
        id:   entryId
      };

    sendPost(body, (xhr) => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let resp = JSON.parse(xhr.responseText);
            if (resp.success === true)
            {
                getPets()//TODO update pet list but stay on this page to and refresh icons/colors
            }
        }
    }, BACKEND_URL + "submitTime");
    //Send post with entry and current time in epoch
}

function addActionButton(name, id, time){
    let elementTag = document.createElement('button');
    let elementText = document.createTextNode(name);
    const diffDate = Date.now()/1000 - time
    console.log(diffDate)
    if(diffDate < 10000000)//These numbers should be config variables
        elementTag.className = "green";
    else if(diffDate < 21600000)
        elementTag.className = "yellow";
    else
        elementTag.className = "red";
    elementTag.onclick =function() { sendTime(id); } //These are set to functions

    elementTag.appendChild(elementText);

    let buttonDisplayer = document.getElementById('button-displayer');
    buttonDisplayer.insertBefore(elementTag, buttonDisplayer.lastChild);
}

function addButton(name, color){
    let elementTag = document.createElement('button');
    let elementText = document.createTextNode(name);
    elementTag.className = color;
    elementTag.onclick =function() { selectPet(name); } //These are set to functions

    elementTag.appendChild(elementText);

    let buttonDisplayer = document.getElementById('button-displayer');
    buttonDisplayer.insertBefore(elementTag, buttonDisplayer.lastChild);
}

function clearButtons()
{
    const buttonDisplayer = document.getElementById("button-displayer");
    while (buttonDisplayer.firstChild != buttonDisplayer.lastChild) {
        buttonDisplayer.removeChild(buttonDisplayer.firstChild);
    }
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
    const username = document.getElementById("username");
    const password = document.getElementById("password");
    if (username === null || password === null)
    {   
        document.getElementById("vaild-pass").innerHTML = "Incorrect Username/Password";
        return false;
    }
    const validpass = password.value;
    password.value = "";
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
            jsonWebToken = resp.token
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

function updatePets(pets){
    allPets = JSON.parse(pets);
}

function drawPets(){
    if(allPets === null)
    {
        getPets()
        return
    }
    for (const [key, value] of Object.entries(allPets)) {
        console.log(`${key}: ${value}`);
        addButton(key, 'red')
      }
}

function getPets(){
    const response = (xhr) => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            resp = xhr.responseText;
            updatePets(resp);
            if(currentState === 2 && petSelected != "")
                selectPet(petSelected)
            else if(currentState!=1)
                updateState(1);
            return;
        }
    document.getElementById("vaild-pass").innerHTML = "Incorrect Username/Password";
    };
    sendGet(BACKEND_URL + "getpets",response )
}

function newButton(){
    
    // clearButtons()
    // addButton('poop', 'green', 'testid');
    logOut()
}