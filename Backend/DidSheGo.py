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
    token, actiontypeid = createNewAction(token, petid, "pee")
    token, actionid = actionMarked(token, actiontypeid, datetime.datetime.now() -datetime.timedelta(days=30))
    token, actiontypeid = createNewAction(token, petid, "poop")
    token, actionid = actionMarked(token, actiontypeid)
    # token = actionDeleted(token, actionid)
    token, actionid = actionMarked(token, actiontypeid)
    # db.getData()
    token = str(login(email, password))
    print(getPetData(token))

def createLogin(email, password):
    try:
        userid = db.insertNewUser(email.lower(),password)
    except sqlite3.IntegrityError as e:
        print(e)
        return False
    except Exception as e:
        print(e)
        return False
    sendValidationEmail(email, userid)
    return login(email,password)

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
    auth = isAuthValid(time,userid, auth)
    if not auth:
        return False
    return userid, auth

def isAuthValid(time, userid, auth):
    if not isinstance(time, datetime.datetime):
        time = utils.getDatetime(time)
    #TODO fix this:
    if time < datetime.datetime.now()-datetime.timedelta(days=30):
        db.cleanupAuths()
        return False
    if time < datetime.datetime.now()-datetime.timedelta(days=25):
        #TODO this auth needs to go
        if deleteAuth(auth):
            auth = generateToken(userid)
    return auth

def checkPetId(token, petid):
    try:
        data, col = db.authPet(token, petid)
    except Exception as e:
        print(e)
        return False
    if len(data) != 1:
        return False
    return isAuthValid(data[0][col.index("Timestamp")], data[0][col.index("userid")], token)
    
def checkActionTypeId(token, actiontypeid):
    try:
        data, col = db.authActionType(token, actiontypeid)
    except:
        return False
    if len(data) != 1:
        return False
    return isAuthValid(data[0][col.index("Timestamp")], data[0][col.index("userid")], token)
    
def checkActionId(token, actionid):
    try:
        data, col = db.authAction(token, actionid)
    except:
        return False
    if len(data) != 1:
        return False
    return isAuthValid(data[0][col.index("Timestamp")], data[0][col.index("userid")], token)
    

def deleteAuth(auth):
    try:
        db.deleteAuth(auth)
    except:
        return False
    return True

def getActionId(petid, actionName):
    try:
        actionid = db.getActionId(petid, actionName)
    except:
        return False
    return actionid

def createNewAction(token, petid, actionName):
    try: newToken = checkPetId(token, petid)
    except Exception as e: 
        print(e)
        return False
    try: 
        if newToken:
            actionid = db.insertNewActionType(petid, actionName)
    except Exception as e: print(e)
    if newToken:
        try:
            actionid = getActionId(petid, actionName)
            print(actionid)
            print(actionid[0][0][0])
            actionMarked(token, actionid[0][0][0])
        except Exception as e:
            print(e)
            return False
    return newToken, actionid

def createNewPet(token, petname):
    try: userid, newToken = checkAuthToken(token)
    except Exception as e:
        print(e)  
        return False
    try: petid = db.insertNewPet(userid, petname)
    except: return False
    return newToken, petid

def actionInverted(token, actionid):
    try: newToken = checkActionId(token, actionid)
    except Exception as e: 
        print(e)
        return False
    try: 
        if newToken:
            db.invertAction(actionid)
    except: return False
    return newToken

#This doesnt have validation for token mapping to actionid
#Should add petid as well, and validate petid to auth token
def actionMarked(token, actiontypeid, time = False):
    try: newToken = checkActionTypeId(token, actiontypeid)
    except Exception as e: 
        print(e)
        return False
    if not time:
        time = datetime.datetime.now()
    try: 
        if newToken:
            id = db.insertAction(actiontypeid, time)
        else:
            id = None
    except: return False
    return newToken, id
    
def sendValidationEmail(email, userid):
    print("pretending to send a validation email")
    valCode = uuid.uuid4()
    #TODO store code, send email with url to endpoint corresponding to code

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
        noActionData, noActionCols = db.getOnlyPetInfo(token)
    except Exception as e:
        print(e)
        return False
    
    if (data == None or cols == None or len(data)) < 1  and (noActionData == None or noActionCols == None or len(noActionData) < 1):
        try:
            uid, auth = checkAuthToken(token)
        except:
            return False
        print(data)
        if not auth:
            return False
        return []
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
            dataMap[entry[pIdI]] = (entry[pNameI], [{"id":entry[aIdI], "name":entry[aNameI], "pos":entry[aPosI], "time":utils.strToEpoch(entry[timeI])}])
        else:
            dataMap[entry[pIdI]][1].append({"id":entry[aIdI], "name":entry[aNameI], "pos":entry[aPosI], "time":utils.strToEpoch(entry[timeI])})
    for entry in noActionData:
        if entry[pIdI] not in dataMap:
            dataMap[entry[pIdI]] = (entry[pNameI], [{"id":-1, "name":"", "pos":-1, "time":-1}])
    return dataMap

def getAllActionData(token, petid):
    try:
        data, cols = db.getAllPetActions(token, petid)
    except Exception as e:
        print(e)
        return False
    
    if data == None or cols == None or len(data) < 1:
        return False
    i = -1
    for entry in cols:
        i+= 1
        if entry == "id":
            aIdI = i
        elif entry == "actionname":
            aNameI = i
        elif entry == "time":
            timeI = i
        elif entry == "deleted":
            dI = i
    dataList = []
    for entry in data:
        dataList.append({"actionid":entry[aIdI], "name":entry[aNameI], "time":entry[timeI], "deleted":entry[dI]==1})
    return dataList

def login(email, password):
    data, col = db.getUserInfo(email=email.lower())
    pwI = col.index("password")
    i = col.index("id")
    if len(data) == 1:
        pw = data[0][pwI]
        if utils.checkPassword(password, pw):
            token = generateToken(data[0][i])
            return token
    print("login failed")
    return False

if __name__ == "__main__":
    runTest()
