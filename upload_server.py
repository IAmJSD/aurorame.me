import os
from pymongo import MongoClient
from flask import Flask, request, jsonify
from random import randint
# Imports and stuff.

mongocli = MongoClient()
webserver = Flask(__name__)
# Defines the clients.

db = mongocli.aurorameme
uploadlog = db.uploadlog
userlist = db.userlist
# MongoDB database/collections

final_url = "https://i.aurorame.me/"
# Sets the final upload URL path.

length = 5
# Sets the default length.

@webserver.route("/", methods=['POST', 'GET'])
def uploader():
    if not request.method == 'POST':
        return jsonify({"status" : "ERR", "errormsg" : "The request method is not HTTP POST."})
    elif request.form.get('key') == None:
        return jsonify({"status" : "ERR", "errormsg" : "No key found."})
    elif userlist.find_one({"dkey" : request.form.get('key')}) == None:
        return jsonify({"status" : "ERR", "errormsg" : "Key incorrect."})
    elif request.files['fileform'] == None:
        return jsonify({"status" : "ERR", "errormsg" : "No file form found."})
    else:
        file = request.files['fileform']
        allowed_extensions = ['png', 'jpeg', 'jpg', 'gif', 'txt', 'bmp', 'mp3']
        x = False
        for extension in allowed_extensions:
            if file.filename.split('.')[len(file.filename.split('.'))-1] == extension:
                x = True
        if not x:
            return jsonify({"status" : "ERR", "errormsg" : "File extension not allowed."})
        else:
            if request.form.get('file_length'):
                try:
                    filelen = int(request.form.get('file_length'))
                    if filelen >= 5 and filelen <= 150:
                        length = filelen
                except:
                    pass
            chars = "0123456789qwertyuiopasdfghjklzxcvbnm"
            l = True
            f = ""
            while l:
                y = 0
                rand = ""
                while not y == length:
                    v = randint(0, len(chars)-1)
                    rand = rand + chars[v]
                    y = y + 1
                if uploadlog.find_one({"filename" : rand}) == None:
                    l = False
                    f = rand
            extension = file.filename.split('.')[len(file.filename.split('.'))-1]
            file.save("./i/" + rand + "." + extension)
            uploadlog.insert_one({"dkey" : request.form.get('key'), "filename" : f})
            return jsonify({"status":"OK","errormsg":"","url":final_url+f})
# The uploader.

if __name__ == '__main__':
    webserver.run(port=36)
# Starts the web server on port 36.
