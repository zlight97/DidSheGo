#Create scripts
createTables = ["CREATE TABLE users( id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL,  password TEXT NOT NULL, verified INTEGER NOT NULL, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)",
"CREATE TABLE loginsessions (id INTEGER PRIMARY KEY, logintoken TEXT NOT NULL, userid INTEGER NOT NULL, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (userid)    REFERENCES users (id) )",
"CREATE TABLE pets( id INTEGER PRIMARY KEY, userid INTEGER NOT NULL, name TEXT NOT NULL, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (userid)    REFERENCES users (id) )",
"CREATE TABLE guests( id INTEGER PRIMARY KEY, petid INTEGER NOT NULL, userid INTEGER NOT NULL, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (userid)    REFERENCES users (id), FOREIGN KEY (petid)    REFERENCES pets (id) )",
"CREATE TABLE actions( id INTEGER PRIMARY KEY, typeid INTEGER NOT NULL, deleted INTEGER NOT NULL, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (typeid)    REFERENCES actiontype (id) )",
"CREATE TABLE validations( id INTEGER PRIMARY KEY, userid INTEGER NOT NULL, validationstr TEXT UNIQUE NOT NULL,Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (userid) REFERENCES users (id) )",
"CREATE TABLE actiontype( id INTEGER PRIMARY KEY, petid INTEGER NOT NULL, name TEXT NOT NULL, position INTEGER, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (petid)    REFERENCES pets (id) )"]

#Delete queries
cleanupAuths = "DELETE FROM validations WHERE CURRENT_TIMESTAMP < date()- 30"
deleteAuth = "DELETE FROM validations WHERE validationstr = ?"
invertAction = "UPDATE actions set deleted = (SELECT NOT deleted) WHERE actions.id = ?"
deleteAction = "UPDATE actions set deleted = 1 WHERE actions.id = ?;"

#Insert queries
insertAuth = "INSERT INTO validations (userid,validationstr) VALUES (?,?);"
insertNewUser = "INSERT INTO users (password,email,verified) VALUES (?, ?, 0);"
insertNewPet = "INSERT INTO pets (userid,name) VALUES (?,?);"
insertActionType = "INSERT INTO actiontype (petid,name,position) VALUES (?,?,(SELECT ifnull(MAX(position) + 1,0) FROM actiontype WHERE petid=?));"
insertAction = "INSERT INTO actions (typeid,deleted,Timestamp) VALUES (?,0,?);"
sharePet = "INSERT INTO guests (petid, userid) VALUES (?, (SELECT id FROM users WHERE email=?));"
getSharedPet = "SELECT id FROM guests WHERE petid=? userid=(SELECT id FROM users WHERE email=?);"

#Select queries
selectUserId = "SELECT * FROM users WHERE id = ?;"
selectUserEmail = "SELECT * FROM users WHERE email = ?;"
selectUserIdFromAuth = "SELECT userid, timestamp from validations WHERE validationstr = ?;"
selectActionId = "SELECT id FROM actiontype WHERE petid = ? AND name = ?;"
selectPetList = """SELECT allpets.name as petname, allpets.petid
FROM validations as va
INNER JOIN
( SELECT userid, id as petid, name FROM pets
UNION ALL
SELECT guests.userid, petid, p.name FROM guests
INNER JOIN pets as p ON p.id = petid ) allpets 
    ON allpets.userid = va.userid
WHERE va.validationstr = ?;"""
selectAllActions = """SELECT actions.id, act.name as actionname, actions.Timestamp as time, actions.deleted
FROM validations as va
INNER JOIN
( SELECT userid, id as petid FROM pets
UNION ALL
SELECT guests.userid, petid FROM guests
INNER JOIN pets as p ON p.id = petid ) allpets 
    ON allpets.userid = va.userid
INNER JOIN actiontype as act ON act.petid = allpets.petid
INNER JOIN actions ON actions.typeid = act.id
WHERE va.validationstr = ? AND act.petid = ?
ORDER BY time desc;
"""
petinfo = """SELECT allpets.name as petname, allpets.petid, act.name as actionname, act.position as actionpos, max(actions.Timestamp) as latestaction, act.id as actionid
FROM validations as va
INNER JOIN
( SELECT userid, id as petid, name FROM pets
UNION ALL
SELECT guests.userid, petid, p.name FROM guests
INNER JOIN pets as p ON p.id = petid ) allpets 
    ON allpets.userid = va.userid
INNER JOIN actiontype as act ON act.petid = allpets.petid
INNER JOIN actions ON actions.typeid = act.id
WHERE va.validationstr = ? AND actions.deleted = 0
GROUP BY actionid
ORDER BY act.position;"""
validatePetInfo = """SELECT va.id, allpets.petid, allpets.userid, va.Timestamp
FROM validations as va
INNER JOIN
( SELECT userid, id as petid FROM pets
UNION ALL
SELECT guests.userid, petid FROM guests
INNER JOIN pets as p ON p.id = petid ) allpets 
    ON allpets.userid = va.userid
WHERE va.validationstr = ? AND petid = ?;"""
validateActionType = """SELECT va.id, act.id as actionid, va.Timestamp, va.userid
FROM validations as va
INNER JOIN
( SELECT userid, id as petid FROM pets
UNION ALL
SELECT guests.userid, petid FROM guests
INNER JOIN pets as p ON p.id = petid ) allpets 
    ON allpets.userid = va.userid
INNER JOIN actiontype as act ON act.petid = allpets.petid
WHERE va.validationstr = ? and actionid = ?;"""
validateAction = """SELECT va.id, actions.id as actionid, va.Timestamp, va.userid
FROM validations as va
INNER JOIN
( SELECT userid, id as petid FROM pets
UNION ALL
SELECT guests.userid, petid FROM guests
INNER JOIN pets as p ON p.id = petid ) allpets 
    ON allpets.userid = va.userid
INNER JOIN actiontype as act ON act.petid = allpets.petid
INNER JOIN actions ON actions.typeid = act.id
WHERE va.validationstr = ? and actionid = ?;"""

migrationSelect = "SELECT Timestamp FROM actions;"
migrationUpdate = "UPDATE actions set Timestamp = ? WHERE Timestamp = ?"