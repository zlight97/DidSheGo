import bcrypt

def getHashedPassword(pw):
    return bcrypt.hashpw(bytes(pw, 'utf-8'), bcrypt.gensalt(15))

def checkPassword(pw, hash):
    return bcrypt.checkpw(bytes(pw, 'utf-8'), bytes(hash, 'utf-8'))