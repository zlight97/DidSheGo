import database as db
import sqlite3
import utils
import uuid

def createLogin(email, password):
    try:
        userid = db.insertNewUser(email,password)
    except sqlite3.IntegrityError as e:
        return False
    except:
        return False
    sendValidationEmail(email, userid)
    return True

def sendValidationEmail(email, userid):
    print("pretending to send a validation email")
    valCode = uuid.uuid4()
    #store code, send email with url to endpoint corresponding to code

def generateToken(userid):
    newToken = uuid.uuid4()
    try:
        db.insertNewAuth(userid, newToken)
        return newToken
    except:
        return False

# def checkToken(token):
#     try:
        

def getPetData(token):
    try:
        data, cols = db.getPetInfo(token)
    except:
        return False
    
    if data == None or cols == None:
        return False

def login(email, password):
    data, col = db.getUserInfo(email=email)
    pwI = col.index("password")
    i = col.index("id")
    if len(data) == 1:
        pw = data[0][pwI]
        if utils.checkPassword(password, pw):
            token = generateToken(data[0][i])
            return token
        
    return False