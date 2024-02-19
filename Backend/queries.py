petinfo = """SELECT allpets.name as petname, allpets.petid, act.name as actionname, act.position as actionpos, max(actions.Timestamp) as latestaction
FROM validations as va
INNER JOIN
( SELECT userid, id as petid, name FROM pets
UNION ALL
SELECT guests.userid, petid, p.name FROM guests
INNER JOIN pets as p ON p.id = petid ) allpets 
    ON allpets.userid = va.userid
INNER JOIN actiontype as act ON act.petid = allpets.petid
INNER JOIN actions ON actions.typeid = act.id
WHERE va.validationstr = ? AND actions.deleted = 0;"""
cleanupAuths = "DELETE FROM validations WHERE CURRENT_TIMESTAMP < GETDATE()- 30"
insertAuth = "INSERT INTO validations (userid,validationstr) VALUES (?,?)"
insertNewUser = "INSERT INTO users (password,email,verified) VALUES (?, ?, 0);"
selectUserId = "SELECT * FROM users WHERE id = ?"
selectUserEmail = "SELECT * FROM users WHERE email = ?"