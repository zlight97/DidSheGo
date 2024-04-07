import bcrypt

def getHashedPassword(pw):
    return bcrypt.hashpw(bytes(pw, 'utf-8'), bcrypt.gensalt(15))

def checkPassword(pw, hash):
    return bcrypt.checkpw(bytes(pw, 'utf-8'), bytes(hash, 'utf-8'))

def strToEpoch(dateStr):
    from datetime import datetime
    dt = getDatetime(dateStr)
    return int(dt.timestamp() * 1000)

def getDatetime(time):
    import re
    from datetime import datetime
    #'2024-03-05 04:41:48'
    regexStr = r'([0-9]+)-([0-9]+)-([0-9]+) ([0-9]+):([0-9]+):([0-9]+)'
    res = re.search(regexStr,time)
    g = res.groups()
    return datetime(int(g[0]),int(g[1]),int(g[2]),int(g[3]),int(g[4]),int(g[5]))