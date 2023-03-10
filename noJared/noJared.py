# noJared v0.1 - a 'drop-in' replacement for Jared
# Intended to be used with pyMessageBridge

import sqlite3
import getpass
import datetime
import json
import requests
import time

print("\n\nStarting noJared...")

# Load noJared.config.json file
try:
    with open("server.config.json") as configFile:
        global config
        config = json.load(configFile)
        configFile.close()
except Exception as error:
    raise error
finally:
    print("Config file loaded...\n")

username = getpass.getuser()
path = f"/Users/{username}/Library/Messages/chat.db"

# open database in read-only mode
chatdb = sqlite3.connect(path, uri=True)

cursor = chatdb.cursor()

def getRowID():
    return cursor.execute('select ROWID from message order by ROWID desc limit 1').fetchone()[0]


def getLastMessage():
    # 1 - gather trackable data
    # stays the same between outgoing and incoming messages
    message = cursor.execute('select ROWID, text from message order by ROWID desc limit 1').fetchone()[1]
    handle_id = cursor.execute('select ROWID, handle_id from message order by ROWID desc limit 1').fetchone()[1]

    
    # 1.1 - get datetime, convert to unix time, and format
    timestamp = cursor.execute('select ROWID, date from message order by ROWID desc limit 1').fetchone()[1]
    timestamp = str(timestamp)[:9]
    # time is cocoa time, so we need to convert it to unix time
    formatted_timestamp = datetime.datetime.fromtimestamp(int(timestamp) + 978307200).strftime('%Y-%m-%d %H:%M:%S')

    # 2 - detect if message is incoming or outgoing
    # detect if message is incoming or outgoing
    sender_isMe = cursor.execute('select ROWID, is_from_me from message order by ROWID desc limit 1').fetchone()[1]
    try:
        if sender_isMe == 1: # outgoing message
            sender_isMe = True
            recipient_isMe = False

            sender_handle = config["techphoneNumber"]
            sender_givenName = sender_handle

            recipient_handle = cursor.execute(f'select ROWID, id from handle where ROWID = {handle_id}').fetchone()[1]
            recipient_givenName = recipient_handle

        elif sender_isMe == 0: # incoming message
            sender_isMe = False
            recipient_isMe = True

            sender_givenName = cursor.execute(f'select ROWID, id from handle where ROWID = {handle_id}').fetchone()[1]
            sender_handle = cursor.execute(f'select ROWID, id from handle where ROWID = {handle_id}').fetchone()[1]   

            recipient_handle = config["techphoneNumber"]
            recipient_givenName = recipient_handle

        # 3 - get guid
        guid = cursor.execute('select ROWID, guid from message order by ROWID desc limit 1').fetchone()[1]


        # finally - create the json response object
        lastMessage = {
            "body": {
                "message": message
            },
            "sendStyle": "regular",
            "attachments": [],
            "recipient": {
                "handle": recipient_handle,
                "givenName": recipient_givenName,
                "isMe": recipient_isMe
            },
            "sender": {
                "handle": sender_handle,
                "givenName": sender_givenName,
                "isMe": sender_isMe
            },
                "date": formatted_timestamp,
                "guid": guid
            }
        return lastMessage

    except Exception:
        return None
# END getLastMessage()

print("\033[92mnoJared v0.1\033[0m", end=": ")
print(f"Monitoring {path} for new messages...")

row_id = getRowID()
while True:
    if row_id != getRowID():
        lastMessage = getLastMessage()
        if lastMessage == None:
            continue
        response = requests.post("http://127.0.0.1:8000/forward", json=lastMessage)
        if response.status_code == 200:          
            # print "noJared: " in green, then the row_id then the status code
            print("\033[92mnoJared\033[0m:", f"#{row_id}", "-->", response.status_code)
            row_id += 1
        else:
            # print "noJared: " in red, then the row_id then the status code
            print("\033[91mnoJared\033[0m:", f"#{row_id}", "-/->", response.status_code)
            print(response.status_code)
            continue
    else:
        time.sleep(0.001) # sleep for 1ms