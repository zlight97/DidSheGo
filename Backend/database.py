import sqlite3
import utils
#TODO does this need to be threadsafe for flask?
def getCursor():
    con = sqlite3.connect("test.sqlite")
    cursor = con.cursor()
    return cursor, con
#Should return columns for latest cursor execute or None if latest execute was not a select
def getColumns(cursor):
    return [description[0] for description in cursor.description] if cursor.description else None

#Only to be run as setup. Should be main of this file
def createTables():
    cursor, con = getCursor()
    with open("createTables.sql") as f:
        queries = f.readlines()
    for query in queries:
        cursor.execute(query)

def getUserInfo(id = None, username = None, email = None):
    cursor, con = getCursor()
    if id:
        query = f"SELECT * FROM users WHERE id = {id}"
    elif username:
        query = f"SELECT * FROM users WHERE username = '{username}'"
    elif email:
        query = f"SELECT * FROM users WHERE email = '{email}'"
    else:
        return None
    return cursor.execute(query).fetchall(), getColumns(cursor)

def insertNewUser(username, password, email):
    cursor, con = getCursor()
    hashedPw = utils.getHashedPassword(password)
    query = f"INSERT INTO users (username,password,email,verified) VALUES ('{username}','{hashedPw.decode('utf-8')}', '{email}', 0);"
    cursor.execute(query)
    con.commit()
def getData():
    cursor, con = getCursor()
    query = "SELECT * FROM users"
    print(cursor.execute(query).fetchall())

if __name__ == "__main__":
    # db.createTables()
    insertNewUser("test","testtest", "test@test.com")
    getData()
    a, b = getUserInfo(id=1)
    print(a)
    print(b)