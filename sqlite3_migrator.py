from pymongo import MongoClient
import sqlite3
# Imports and stuff.

conn = sqlite3.connect('website.db')
mongocli = MongoClient()
# Sets clients

c = conn.cursor()
db = mongocli.aurorameme
uploadlog = db.uploadlog
userlist = db.userlist
# Sets cursors/collections

def MigrateLog():
    for row in c.execute("SELECT * FROM uploadlog"):
        uploadlog.insert_one({"dkey" : row[0], "filename" : row[1], "ipaddr" : row[2]})

def MigrateKeylist():
    for row in c.execute("SELECT * FROM keylist"):
        userlist.insert_one({"discordid" : row[0], "email" : row[1], "dkey" : row[2]})

MigrateLog()
MigrateKeylist()
# Migrates the DB.
