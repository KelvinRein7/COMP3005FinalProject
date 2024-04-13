from program import *
from members import *

def isTrainer(username, cur):
        # Check if the username exists in the Trainer table
        cur.execute("SELECT EXISTS(SELECT 1 FROM Trainer JOIN UserLogin ON Trainer.loginID = UserLogin.loginID WHERE UserLogin.username = %s)", (username,))
        return cur.fetchone()[0]

def isMember(username, cur):
        # Check if the username exists in the Member table
        cur.execute("SELECT EXISTS(SELECT 1 FROM Member JOIN UserLogin ON Member.loginID = UserLogin.loginID WHERE UserLogin.username = %s)", (username,))
        return cur.fetchone()[0]

def isAdmin(username, cur):
        # Check if the username exists in the Admin table
        cur.execute("SELECT EXISTS(SELECT 1 FROM Admin JOIN UserLogin ON Admin.loginID = UserLogin.loginID WHERE UserLogin.username = %s)", (username,))
        return cur.fetchone()[0]

def getTrainerID(id, cursor):
    cursor.execute("SELECT trainerID FROM Trainer WHERE loginID = %s", (id,))
    trainerID = cursor.fetchone()[0]
    return trainerID

def getAdminID(id, cursor):
    cursor.execute("SELECT adminID FROM Admin WHERE loginID = %s", (id,))
    adminID = cursor.fetchone()[0]
    return adminID

