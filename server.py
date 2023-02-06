# iMessage Forwading Server (requires: MacOS 10.15+ & jared & python 3+)
# Version: 0.1.0
# Written by: Kazei McQuaid
# Admin Panel: http://127.0.0.1:8000/admin
# Submit requests to: http://127.0.0.1:8000/forward

if __name__ == '__main__':
    print("\npyMessageBridge Version 0.1.0 ")
    print("Incorrect usage. Please run the server with the following command:")
    print("\"python3 -m uvicorn server:app\"")
    print("For more information, please visit: https://www.github.com/wafwoof/pyMessageBridge")
    exit()

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import os
import requests
import datetime

print("\nThe server is starting...")

# Load server.config.json file
try:
    with open ("server.config.json") as configFile:
        config = json.load(configFile)
except Exception as error:
    raise error
finally:
    configFile.close()
    print("Config file loaded...")

global whitelist
whitelist = [] # WHITELIST: numbers that will receive the message, including the host will create a loop.
for number in config["managerWhitelist"]: # add permanent manager numbers to the whitelist.
    whitelist.append(number)


app = FastAPI(openapi_url=None) # Leaving openapi on is a potential security risk, just saying.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SEND MESSAGES
def sendMessage(num, message):
    try:
        os.system("osascript sendMessage.scpt %s %s"%(str(num), str(message)))
    except Exception as error:
        print("Error sending message:", error)
        raise error

# LOG MESSAGES
def message_log(message):
    # Write to the log file before the message is interpreted.
    with open("log.txt", "r+") as log: # nothing fancy, plaintext
        # get size of log file in kilobytes
        logSize = os.path.getsize("log.txt") / 1000
        if logSize > 1000: # 1000kb
            log.truncate(0)
        # write messages to the top of the log file
        existingLogEntries = log.read()
        log.seek(0, 0)
        log.write(f"{datetime.datetime.now()} {message}" + "\n" + existingLogEntries)
        log.close()

# FORWARD MESSAGES
def message_forward_handler(message):
    # Check to see if the message is a command.
    if message['content'][0][:1] == config["textCommandSymbol"]:
        pass
    elif message['senderHandle'] == config["techphoneNumber"] and config["forwardOutgoingMessages"] == False:
        print("Outgoing messages are not being forwarded. This behavior can be changed in server.config.json")
        pass
    elif message['senderHandle'] == message['recipientHandle']:
        print("Phone texted itself. Ignoring.")
        pass
    else:
        # Forward incoming tech phone messages to numbers contained in the whitelist.
        print("Forwarding message to whitelist", end="")
        for num in whitelist:
            sendMessage(num, message['content'])
            print(".", end="") # print without newline
        print(" DONE")
        print("Contacted:", whitelist)

# INTERPRET COMMANDS
def message_command_interpretter(message):
    if message['content'][0][:1] == config["textCommandSymbol"]: # command symbol is ¥ by default.
        command = message['content'][1:] # chop off the ¥ symbol.
        print("Command detected:", command)
        # COMMAND LIST
        if command in ["antiquing"]: # shutdown the server.
            os.system("kill -9 $(ps -A | grep python | awk '{print $1}')")
            print("Server shutdown by remote text command.")
        elif command in ["help", "help ", "?"]: # get a list of commands.
            response = repr("Commands: ¥help, ¥whitelist, ¥unwhitelist, ¥seewhitelist, ¥clearwhitelist, ¥weather, ¥random")
            sendMessage(message['senderHandle'], response)
        elif command in ["whitelist", "whitelist "]: # add a number to the whitelist.
            whitelist.append(message['senderHandle'])
            response = repr("Your number is now on the whitelist.")
            sendMessage(message['senderHandle'], response)
        elif command in ["unwhitelist", "unwhitelist "]: # remove your number from the whitelist.
            whitelist.remove(message['senderHandle'])
            response = repr("Your number has been removed from the whitelist.")
            sendMessage(message['senderHandle'], response)
        elif command in ["seewhitelist", "seewhitelist "]: # view the whitelist.
            response = repr(whitelist)
            sendMessage(message['senderHandle'], response)
        elif command in ["clearwhitelist", "clearwhitelist "]: # clear the whitelist.
            whitelist.clear()
            response = repr("Whitelist Cleared.")
            sendMessage(message['senderHandle'], response)
        elif command in["weather", "weather "]: # get the weather.
            temp = requests.get("https://wttr.in/Vancouver?format=4").text[0:31]
            print("Weather:", repr(temp))
            response = repr(temp)
            sendMessage(message['senderHandle'], response)
        elif command in ["random", "random "]: # get a random word.
            # get a random word from a dictionary api.
            word = requests.get("https://random-word-api.herokuapp.com/word?number=1").text[2:-2]
            response = repr("Your Word Is: " + "'" + word + "'")
            sendMessage(message['senderHandle'], response)
        else: # if the command is not recognized, return an error.
            print("Command not recognized.")
            # Do not send an error message, this will use up resources and you can solve your own problems.
            #message = repr("Command not recognized.")
            #sendMessage(handle, message)

# RECEIVE JARED WEBHOOK
@app.post("/forward")
async def get_body(request: Request):
    data = await request.json()

    senderHandle = data.get("sender")["handle"]
    recipientHandle = data.get("recipient")["handle"]
    content = data.get("body")["message"]

    # constructed message dict
    message = {
        "senderHandle": senderHandle,
        "recipientHandle": recipientHandle,
        "content": content
    }

    print(f"{message['senderHandle']} -> {message['recipientHandle']}: {message['content']}")

    # message log function
    message_log(message)
    # message forwarding function
    message_forward_handler(message)
    # message command interpretter function
    message_command_interpretter(message)


# END RECEIVE JARED WEBHOOK


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
print("\npyMessageBridge Version 0.1.0 - Current date/time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("Visit: http://localhost:8000/admin to get started!\n")
print("THIS IS DEVELOPMENT SOFTWARE AND COMES WITH ABSOLUTELY NO WARRANTY.\n")
print("Available Text Commands:")
print("¥help, ¥whitelist, ¥unwhitelist, ¥seewhitelist, ¥clearwhitelist, ¥weather, ¥random\n")
print("Available Endpoints:")
print("/forward, /security/by/obfuscation/getlog, /admin, /admin/whitelist, /admin/whitelist/post, /admin/whitelist/clear\n")
