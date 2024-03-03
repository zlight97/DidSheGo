import database as db
import sqlite3
import utils
import uuid
import datetime

def runTest():
    db.resetServer()
    email = "test@bigtest.com"
    password = "ordtest1234!"
    createLogin(email, password)
    token = str(login(email, password))
    token, petid = createNewPet(token, "testPet")
    token, actionid = createNewAction(token, petid, "pee")
    token = actionMarked(token, actionid)
    db.getData()

def createLogin(email, password):
    try:
        userid = db.insertNewUser(email,password)
    except sqlite3.IntegrityError as e:
        return False
    except:
        return False
    sendValidationEmail(email, userid)
    return True

def checkAuthToken(auth):
    try:
        data, col = db.getUserId(auth)
    except Exception as e:
        print(e)
        return False
    if len(data) != 1:
        return False
    userid = data[0][col.index("userid")]
    time = data[0][col.index("Timestamp")]
    auth = isAuthValid(time,userid)
    if not auth:
        return False
    return userid, auth

def isAuthValid(time, userid):
    if time.date < datetime.datetime.now()-datetime.timedelta(days=30):
        db.cleanupAuths()
        return False
    if time.date < datetime.datetime.now()-datetime.timedelta(days=25):
        if deleteAuth(auth):
            auth = generateToken(userid)
    return auth

def checkPetId(token, petid):
    try:
        data, col = db.authPet(token, petid)
    except:
        return False
    if len(data) != 1:
        return False
    return isAuthValid(data[0][col.index("timestamp")])
    
def checkActionId(token, actionid):
    try:
        data, col = db.authAction(token, actionid)
    except:
        return False
    if len(data) != 1:
        return False
    return isAuthValid(data[0][col.index("timestamp")])
    

def deleteAuth(auth):
    try:
        db.deleteAuth(auth)
    except:
        return False
    return True

def createNewAction(token, petid, actionName):
    try: newToken = checkPetId(token, petid)
    except: return False
    try: 
        if newToken:
            actionid = db.insertNewActionType(petid, actionName)
    except: return False
    return newToken, actionid

def createNewPet(token, petname):
    try: userid, newToken = checkAuthToken(token)
    except Exception as e:
        print(e)  
        return False
    try: petid = db.insertNewPet(userid, petname)
    except: return False
    return newToken, petid

#This doesnt have validation for token mapping to actionid
#Should add petid as well, and validate petid to auth token
def actionMarked(token, actionid, time = False):
    try: newToken = checkActionId(token, actionid)
    except: return False
    if not time:
        time = datetime.now()
    try: 
        if newToken:
            db.insertAction(actionid, time)
    except: return False
    return newToken
    
def sendValidationEmail(email, userid):
    print("pretending to send a validation email")
    valCode = uuid.uuid4()
    #store code, send email with url to endpoint corresponding to code

def generateToken(userid):
    newToken = uuid.uuid4()
    try:
        db.insertNewAuth(userid, str(newToken))
        return newToken
    except Exception as e:
        print(e)
        print(e.with_traceback)
        return False
        
#TODO test that this query gets the needed results
def getPetData(token):
    try:
        data, cols = db.getPetInfo(token)
    except:
        return False
    
    if data == None or cols == None or len(data) < 1:
        return False
    i = -1
    for entry in cols:
        i+= 1
        if entry == "petname":
            pNameI = i
        elif entry == "petid":
            pIdI = i
        elif entry == "actionname":
            aNameI = i
        elif entry == "actionpos":
            aPosI = i
        elif entry == "latestaction":
            timeI = i
        elif entry == "actionid":#This is action type id
            aIdI = i
    dataMap = {}
    for entry in data:
        if entry[pIdI] not in dataMap:
            dataMap[pIdI] = (entry[pNameI], [(entry[aIdI], entry[aNameI], entry[aPosI], entry[timeI])])
        else:
            dataMap[pIdI][1].append((entry[aIdI], entry[aNameI], entry[aPosI], entry[timeI]))
    return dataMap

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

if __name__ == "__main__":
    runTest()