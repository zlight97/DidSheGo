import database as db
import utils

def createLogin(username, password, email):
    checkLoginExists(username)

def checkLoginExists(username):
    data, col = db.getUserInfo(username=username)
    return len(data) > 0