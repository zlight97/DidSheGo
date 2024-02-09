import database as db
import sqlite3
import utils
import uuid

def createLogin(username, password, email):
    try:
        userid = db.insertNewUser(username,password,email)
    except sqlite3.IntegrityError as e:
        return False
    sendValidationEmail(email, userid)
    return True

def sendValidationEmail(email, userid):
    print("pretending to send a validation email")
    valCode = uuid.uuid4()
    #store code, send email with url to endpoint corresponding to code

def checkLoginExists(username):
    data, col = db.getUserInfo(username=username)
    return len(data) > 0