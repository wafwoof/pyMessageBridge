# pyMessageBridge v0.1.0
## An iMessage Communication Bridge (requires: MacOS & jared)

pyMessageBridge functions as an abstraction layer for [Jared](https://github.com/ZekeSnider/Jared).
Designed as a simple approach to forwarding iPhone messages to a small to medium sized team.
It allows advanced users without a programming background to get power features out of their existing devices.

Features of pyMessageBridge:
- An easy way to share messages to multiple numbers
- Web admin panel for adding numbers to the whitelist
    - http://localhost:8000/admin
- Local & remote message log file (MacOS rightly blocks it by default, I will leave this up to the end-user)
-  A remote command feature that works by sending a "¥" character followed by a pre-determined command (Covered in more detail below)

![pyMessageBridge Admin Panel](/static/Screen%20Shot%202023-01-29%20at%2011.14.17%20PM.png)

A very basic graphical overview for those who want it.

## How to setup

Before you do anything else: disable mac power settings in system preferences to prevent the server from going to sleep. Since this is intended for business environments where downtime is unacceptable: I recommend pm2 as a process manager.

#### Install Jared:
- A tested version can be found in ./jared/ unzip it.
- Enable Jared, disable sending messages, enable REST API, do not add a contacts list.

![Jared Main Settings](/jared/JARED_EXAMPLE.png)

- After installing: replace ~/Library/Application Support/Jared/config.json with included backup file in /jared/
- Reboot Jared

Jared is now configured and is already sending messages.

Now we must setup the server itself.

#### Install pyMessageBridge

#### server dependencies:
- MacOS 10.15+
- an iMessage account linked to an iPhone that you wish to share with your team
- Python 3+ (3.11 really speeds up certain things)
- uvicorn, fastapi, requests, pm2 (optional, but recommended)

Clone the project, install all required dependencies, create `/pyMessageBridge/log.txt` and `/pyMessageBridge/server.config.txt` (**very important files!**).

The config file is a simple json file with a object containing:
- techphoneNumber
    - an integer for preventing infinite loops
- managerWhitelist
    - an array for restart presistent numbers
- textCommandSymbol
    - a character symbol for triggering command interpretation
- forwardOutgoingMessages
    - a boolean 

Now, start the server by running `bash server-start.sh` in the terminal. If everything is configured correctly, it should start without any error messages. Note: you will have to clear the old server binds each time you re-run the server. Do this by running `bash server-kill.sh` and then start the server normally.

Troubleshooting tips:
- restart your terminal often
- restart your mac a few times between steps during initial installation
- send a few test messages to confirm desired functionality before packing the server away for production 

That's it! You now have a working pyMessageBridge server.

Config settings are in: `/pyMessageBridge/server.config.txt`. 

## Text commands

**Security warning!** Change the default commands in the server to avoid anyone being able to take it down. The default character ( ¥ ) can also be changed to anything you like.

There are currently 7 primary commands:
- ¥help 
- ¥whitelist 
- ¥unwhitelist 
- ¥seewhitelist
- ¥clearwhitelist
- ¥weather
- ¥random

## Planned features

- Message queue architecture 
- Proper reliabilty stress testing
- Teams integration
- Admin panel tunneling for remote login
