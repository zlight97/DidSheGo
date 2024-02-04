import sqlite3
import utils
#TODO does this need to be threadsafe for flask?
class DSGDB:
    def __init__(self):
        self.con = sqlite3.connect("test.sqlite")
        self.cursor = self.con.cursor()
    def createTables(self):
        with open("createTables.sql") as f:
            queries = f.readlines()
        for query in queries:
            print(query)
            self.cursor.execute(query)
    def newuser(self, username, password, email):
        hashedPw = utils.getHashedPassword(password)
        query = f"INSERT INTO users (username,password,email,verified) VALUES ('{username}','{hashedPw.decode('utf-8')}', '{email}', 0);"
        print(query)
        self.cursor.execute(query)
    def getData(self):
        query = "SELECT * FROM users"
        print(self.cursor.execute(query).fetchall())
if __name__ == "__main__":
    db = DSGDB()
    db.createTables()
    db.newuser("test","testtest", "test@test.com")
    db.getData()