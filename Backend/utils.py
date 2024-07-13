import bcrypt

def getHashedPassword(pw):
    return bcrypt.hashpw(bytes(pw, 'utf-8'), bcrypt.gensalt(15))

def checkPassword(pw, hash):
    return bcrypt.checkpw(bytes(pw, 'utf-8'), bytes(hash, 'utf-8'))

def epochToDatetime(epoch):
    from datetime import datetime
    epoch = int(epoch/1000)
    return str(epoch)#datetime.fromtimestamp(epoch)

def strToEpoch(dateStr):
    try:
        from datetime import datetime
        dt = getDatetime(dateStr)
        e = int(dt.timestamp())
        return e
    except:
        print("ERROR: strToEpoch. String not recognized: " + str(dateStr))
        return dateStr

def getDatetime(time):
    import re
    from datetime import datetime
    #'2024-03-05 04:41:48'
    regexStr = r'([0-9]+)-([0-9]+)-([0-9]+) ([0-9]+):([0-9]+):([0-9]+)'
    res = re.search(regexStr,time)
    g = res.groups()
    return datetime(int(g[0]),int(g[1]),int(g[2]),int(g[3]),int(g[4]),int(g[5]))