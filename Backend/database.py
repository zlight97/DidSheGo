import sqlite3
import utils
import queries
#TODO does this need to be threadsafe for flask?
def getCursor():
    con = sqlite3.connect("test.sqlite")
    cursor = con.cursor()
    return cursor, con

def submitQuery(query, params = None, cursor = None, con = None, noid = False):
    if not cursor or not con:
        cursor, con = getCursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    con.commit()
    lastid = cursor.lastrowid if not noid else None
    cursor.close()
    con.close()
    return lastid

def select(query, params):
    cursor, con = getCursor()
    data = cursor.execute(query,params).fetchall()
    col = getColumns(cursor)
    cursor.close()
    con.close()
    return data, col
    
#Should return columns for latest cursor execute or None if latest execute was not a select
def getColumns(cursor):
    return [description[0] for description in cursor.description] if cursor.description else None

#Only to be run as setup. Should be main of this file
def createTables():
    cursor, con = getCursor()
    qs = queries.createTables
    for query in qs:
        cursor.execute(query)

def getUserInfo(id = None, email = None):
    if id:
        query = queries.selectUserId
        params = tuple([id])
    elif email:
        query = queries.selectUserEmail
        params = tuple([email])
    else:
        return None
    return select(query,params)

def insertNewUser(email, password):
    hashedPw = utils.getHashedPassword(password)
    return submitQuery(queries.insertNewUser, (hashedPw.decode('utf-8'), email))

def insertNewAuth(userid, authkey):
    return submitQuery(queries.insertAuth, (userid, authkey))

def cleanupAuths():
    submitQuery(queries.cleanupAuths, noid=True)

def getPetInfo(authkey):
    cleanupAuths()
    return select(queries.petinfo, (authkey,))

def getData():
    cursor, con = getCursor()
    query = "SELECT * FROM users"
    print(cursor.execute(query).fetchall())

def cleanTest():
    createTables()
    insertNewUser("te12asdf34st@test.com", "testtest")
    a, b = getUserInfo(id=1)

if __name__ == "__main__":
    # createTables()
    getData()
    insertNewUser("te12asdf34st@test.com", "testtest")
    a, b = getUserInfo(id=1)
    print(a)
    print(b)