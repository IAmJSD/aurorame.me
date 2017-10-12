import os
from flask import Flask, send_file, abort
# Imports and stuff.

webserver = Flask(__name__)
# Defines the web server.

@webserver.route("/")
def acc_denied():
    return "You cannot browse this subdomain."
# Denies access if user tries to browse the subdomain.

@webserver.route("/<path:imageid>")
def i(imageid):
    imageid = imageid.rstrip('/').split('.')[0]
    x = False
    for file in os.listdir("./i"):
       if file.split('.')[0] == imageid:
           x = True
           return send_file("./i/" + file)
    if not x:
        abort(404)
# If there is a file with the name suggested, load the file.

if __name__ == '__main__':
    webserver.run(port=34)
# Starts the web server on port 34.
