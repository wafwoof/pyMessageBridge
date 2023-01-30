# iMessage Forwading Server (requires: MacOS 10.15+ & jared & python 3+)
# MVP: 1
# Written by: Kazei McQuaid
# Admin Panel: http://127.0.0.1:8000/admin
# Submit requests to: http://127.0.0.1:8000/forward
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import requests
import datetime

print("\nThe server is starting...\n")

app = FastAPI(openapi_url=None) # Leaving openapi on is a potential security risk, just saying.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

global whitelist # define whitelist as a global variable.
whitelist = [] # WHITELIST: numbers that will receive the message, including the host will create a loop.

# RECEIVE JARED WEBHOOK
@app.post("/forward")
async def get_body(request: Request):
    data = await request.json()
    handle = data.get("sender")["handle"]
    senderIsMe = data.get("sender")["isMe"]
    message = (handle, "sent to tech phone:", data.get("body")["message"])
    
    # console log just the message with no sugar
    print(message)
    
    # INTERPRET COMMANDS
    # Command Symbol: ¥
    if data.get("body")["message"][0][:1] == "¥":
        print("Command received.")
        # get the command.
        command = data.get("body")["message"][1:]
        print("Command:", command)
        if command in ["kill -9", "antiquing"]: # shutdown the server.
            os.system("kill -9 $(ps -A | grep python | awk '{print $1}')")
        elif command in["weather", "weather ", "temp", "temp ", "wind", "wind "]: # get the weather.
            temp = requests.get("https://wttr.in/Vancouver?format=4").text[0:30]
            print("Temperature:", repr(temp))
            message = repr(temp)
            os.system("osascript sendMessage.applescript -%s -%s"%(int(handle), str(message)))
        elif command in ["random", "random ", "rnd", "rnd "]: # get a random word.
            # get a random word from a dictionary api.
            word = requests.get("https://random-word-api.herokuapp.com/word?number=1").text[2:-2]
            message = repr("Your Word Is: " + "'" + word + "'")
            os.system("osascript sendMessage.applescript -%s -%s"%(int(handle), str(message)))
        else: # if the command is not recognized, return an error.
            print("Command not recognized.")
            return

    # END INTERPRET COMMANDS

    # BEGIN FORWARDING TO WHITE LISTED NUMBERS

    # Check to see if message is from the tech phone.
    if senderIsMe == True:
        return
    elif senderIsMe == False:
        # Forward incoming tech phone messages to numbers contained in the whitelist.
        for num in whitelist:
            modifiedMessage = ("\"" + handle + " SENT: " + message + "\"")
            print(modifiedMessage)
            sendCommand = "osascript sendMessage.applescript -%s -%s"%(int(num), str(modifiedMessage))
            print("send command:", sendCommand)
            print("Contacting:", num)
            os.system(sendCommand)

    
    # Write to a json log file.
    with open("log.txt", "a") as log:
        log.write(str(message))
        log.write("\n")

    # END FORWARDING TO WHITE LISTED NUMBERS


# HTTP GET LOG (for backup)
@app.get("/security/by/obfuscation/admin/log")
def get_log():
    # check the size of the log file.
    logSize = os.path.getsize("log.txt")
    # if the log file is larger than 1MB: delete it.
    if logSize > 1000000:
        os.remove("log.txt")
    else:
        with open("log.txt", "r") as log:
            return log.read()

# HTTP GET Admin Panel (Graphical user friendly interface)
@app.get("/admin" , response_class=HTMLResponse)
def admin_panel():
    with open("./static/index.html", "r") as admin:
        return admin.read()

# HTTP GET whitelist
@app.get("/admin/whitelist")
def get_whitelist():
    return whitelist

# HTTP POST whitelist
@app.post("/admin/whitelist/post")
async def post_whitelist(request: Request):
    data = await request.json()
    whitelist.append(data.get("number"))
    return whitelist

# HTTP DELETE whitelist
@app.get("/admin/whitelist/clear")
def delete_whitelist():
    whitelist.clear()


# Console Log
print("pyMessageBridge Version 0.1.0 - Current date/time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("Visit: http://localhost:8000/admin to get started!\n")
print("THIS IS DEVELOPMENT SOFTWARE AND COMES WITH ABSOLUTELY NO WARRANTY.\n")
print("Available Endpoints:")
print("/forward, /security/by/obfuscation/getlog, /admin, /admin/whitelist, /admin/whitelist/post, /admin/whitelist/clear\n")
