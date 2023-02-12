# iMessage Forwading Server (requires: MacOS 10.15+ & python 3+)
# Version: 0.1.2 (noJared 0.1)
# Written by: Kazei McQuaid
# Admin Panel: http://127.0.0.1:8000/admin
# Submit requests to: http://127.0.0.1:8000/forward

if __name__ == '__main__':
    print("\npyMessageBridge Version 0.1.2 ")
    print("Incorrect usage. Please run the server with the following command:")
    print("\"python3 -m uvicorn server:app\"")
    print("For more information, please visit: https://www.github.com/wafwoof/pyMessageBridge")
    exit()

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
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
        os.system(f"osascript sendMessage.scpt {str(num)} \"{str(message)}\"")
    except Exception as error:
        print("Error sending message:", error)
        raise error

# LOG MESSAGES
def message_log(message):
    # Write to the log file before the message is interpreted.
    with open("log.txt", "r+") as log:
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
    if message["content"][0][:1] == config["textCommandSymbol"]:
        pass
    elif message["senderHandle"] == config["techphoneNumber"] and config["forwardOutgoingMessages"] == False:
        print(f"\033[33mForwarding\033[0m" + ": ", end="")
        print("Outgoing messages are not being forwarded. This behavior can be changed in server.config.json")
        pass
    elif message['senderHandle'] == message['recipientHandle']:
        print("Phone texted itself. Ignoring.")
        pass
    else:
        # Forward incoming tech phone messages to numbers contained in the whitelist.
        print(f"\033[32mForwarding\033[0m" + ": ", end="")
        print("Forwarding message to whitelist", end="")
        formattedMessage = f"{message['senderHandle']}: {message['content']}"
        for num in whitelist:
            sendMessage(num, formattedMessage)
            print(".", end="") # print without newline
        print(" DONE")
        print(f"\033[32mForwarding\033[0m" + ": ", end="")
        print("Contacted:", whitelist, "Total:", len(whitelist))

# END FORWARD MESSAGES

# INTERPRET COMMANDS
def message_command_interpretter(message):
    if message['content'][0][:1] == config["textCommandSymbol"]: # command symbol is ¥ by default.
        command = message['content'][1:] # chop off the ¥ symbol.
        print(f"\033[33mCommand\033[0m" + ": ", end="")
        print(command)
        # COMMAND LIST
        if command in ["antiquing"]: # shutdown the server.
            os.system("kill -9 $(ps -A | grep python | awk '{print $1}')")
            print("Server shutdown by remote text command.")
        elif command in ["help", "help "]: # get a list of commands.
            response = "Commands: ¥help, ¥whitelist, ¥unwhitelist, ¥seewhitelist, ¥clearwhitelist"
        elif command in ["whitelist", "whitelist "]: # add a number to the whitelist.
            if message['senderHandle'] in whitelist:
                response = "Your number is already on the whitelist."
            elif message['senderHandle'] in config["managerWhitelist"]:
                response = "Your number is already on the whitelist."
            elif message['senderHandle'] == config["techphoneNumber"]:
                response = "Cannot whitelist the tech phone number."
            else:
                whitelist.append(message['senderHandle'])
            response = "Your number is now on the whitelist."
        elif command in ["unwhitelist", "unwhitelist "]: # remove your number from the whitelist.
            whitelist.remove(message['senderHandle'])
            response = "Your number has been taken off the whitelist."
        elif command in ["seewhitelist", "seewhitelist "]: # view the whitelist.
            response = f"Whitelist: {whitelist}"
        elif command in ["clearwhitelist", "clearwhitelist "]: # clear the whitelist.
            whitelist.clear()
            response = "Whitelist Cleared."
        elif command in["weather", "weather "]: # get the weather.
            try:
                response = requests.get("https://wttr.in/~main+vancouver?format=4").text[5:-1]
            except Exception as error:
                print(error)
                response = "There was an error, please try again later."
        elif command in ["random", "random "]: # get a random word.
            # get a random word from a dictionary api.
            try:
                word = requests.get("https://random-word-api.herokuapp.com/word?number=1").text[2:-2]
            except Exception as error:
                print(error)
                response = "There was an error, please try again later."
            response = f"Your Word Is: {word}"
        else: # if the command is not recognized, return an error.
            print("Command not recognized.")
            # Do not send an error message, this will use up resources and you can solve your own problems.
            #message = repr("Command not recognized.")
            #sendMessage(handle, message)
            return


        response = f"<{config['textCommandSymbol']}> {response}"
        sendMessage(message['senderHandle'], response)

# END COMMAND INTERPRETER

# MESSAGE HANDLER THREAD
def message_handler(message):
    message_log(message)                    # 1
    message_forward_handler(message)        # 2
    message_command_interpretter(message)   # 3

# RECEIVE JARED WEBHOOK
@app.post("/forward")
async def get_body(request: Request):
    data = await request.json()

    senderHandle = data.get("sender")["handle"]
    recipientHandle = data.get("recipient")["handle"]
    content = data.get("body")["message"]
    datetime = data.get("date") # time: 2023-02-08T01:31:16.000Z
    # time = time - first 10 characters are date, last 5 are time, and the middle is a T
    time = datetime[11:19] # time: 24hr format

    # constructed message dict
    message = {
        "senderHandle": senderHandle,
        "recipientHandle": recipientHandle,
        "time": time,
        "content": content
    }

    # print the word "info" in green
    print(f"\n\033[32mJared\033[0m" + ": ", end="")


    print(f"{message['senderHandle']} -> {message['recipientHandle']} @ {message['time']}: {message['content']}")

    message_handler(message) # passoff to the main message router and handler function

    response = json.dumps({
        "success": True,
        "body": {   
            "message": "We're on each other's team" 
        }
    })
    return JSONResponse(status_code=200, content=response)
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
print("\npyMessageBridge Version 0.1.2 - Current date/time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("Visit: http://localhost:8000/admin to get started!\n")
print("THIS IS DEVELOPMENT SOFTWARE AND COMES WITH ABSOLUTELY NO WARRANTY.\n")
print("Tech Phone Number: ", config["techphoneNumber"])
print("Available Text Commands:")
print("¥help, ¥whitelist, ¥unwhitelist, ¥seewhitelist, ¥clearwhitelist, ¥weather, ¥random\n")
print("Available Endpoints:")
print("/forward, /security/by/obfuscation/getlog, /admin, /admin/whitelist, /admin/whitelist/post, /admin/whitelist/clear\n")
