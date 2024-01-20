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
    const body = JSON.stringify({
        username: username,
        password: password
      });
    const response = (xhr) => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            resp = JSON.parse(xhr.responseText);
            console.log(resp);
            if (resp.success === true)
            {
                loggedIn(resp.token);
                return;
            }
        }
        document.getElementById("vaild-pass").innerHTML = "Incorrect Username/Password";
        console.log(`Error: ${xhr.status}`);
      };

    sendPost(url, body, response);

}

function sendPost(url, body, responseFunc)
{
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8")
    xhr.setRequestHeader("Access-Control-Allow-Headers", "x-requested-with");
    xhr.onload = () => responseFunc(xhr)
    console.log(body)
    xhr.send(body);
}

function newButton(){
        addButton('poop', 'green', 'testid');
    }

function newButton2(id){
    addButton('poop', 'green', id);
}