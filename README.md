![release](https://img.shields.io/badge/release-v0.1.2-lightgrey) ![Tested Python Version](https://img.shields.io/badge/python-3.11-blue) ![jared](https://img.shields.io/badge/jared-compatible-green)
# pyMessageBridge v0.1.2
## An iMessage Communication Bridge (requires: MacOS & ~~jared~~)

The purpose of pyMessageBridge is to allow a small-medium sized team to share a single iPhone's messages. Intended for use as backup communication or in a customer service environment.

pyMessageBridge no longer requires [Jared](https://github.com/ZekeSnider/Jared). Instead;  I recommend using noJared. I wrote it myself, and it's insanely fast. (you can still use classic Jared if you wish.)

Features of pyMessageBridge 0.1.2:

- Replaced Jared with noJared.
- Very configurable.
- Improved Command response, console, and log formatting.
- Web panel for adding numbers to the whitelist.
    - http://localhost:8000/admin

![pyMessageBridge Admin Panel](/documentation/webimage1.png)

*The basic web interface.*

#### How to use (for human beings)

To add yourself to the whitelist at the start of your shift by texting `¥whitelist` to the tech phone. You will now receive all messages. 
To respond to a request: simply text the tech phone, and all staff will be alerted. This increases team awareness, and reaction time.
At the end of the day simply `¥unwhitelist` yourself, or a manager can issue `¥clearwhitelist` to remove all phone numbers at the end of the day. `¥seewhitelist` to verify that it's empty. That's it!

## How to Setup

Before you do anything else: disable mac power settings in system preferences to prevent the server from going to sleep. Since this is intended for business environments where downtime is unacceptable: I recommend pm2 as a process manager.

#### Install pyMessageBridge

#### Server Dependencies:
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

Now, start the server by running `bash run-with-noJared.sh` in the terminal.

Troubleshooting tips:
- restart your terminal often
- restart your mac a few times between steps during initial installation
- send a few test messages to confirm desired functionality before packing the server away for production 

That's it! You now have a working pyMessageBridge server.

Configuration settings are in: `server.config.txt`. 

#### Text Command List

**Security warning!** Change the defaults in server.config.json.

There are currently 5 primary commands:
- ¥help 
- ¥whitelist 
- ¥unwhitelist 
- ¥seewhitelist
- ¥clearwhitelist

## iMessage Authentication on Mac
On some machines this is easy, on others it is an extremely difficult task. What worked for me was:
- Resetting NVRAM.
    - `cmd + alt + P + R` while turning on.
- Clearing iMessage related keys in keychain access.
- Waiting 24-hours.
- Calling Apple Support.

As stated above: this was no problem in one case, and wildly daunting in another. Feel free to reach out to me for troubleshooting help.

## Planned Features

- Message queue architecture 
- Proper reliabilty stress testing
- Teams integration
- Admin panel tunneling for remote login

## Previous Releases

#### pyMessageBridge v0.1.1

The purpose of pyMessageBridge is to allow a small - medium sized team to share a single iPhone's messages.

pyMessageBridge functions as an abstraction layer for [Jared](https://github.com/ZekeSnider/Jared).

Features of pyMessageBridge 0.1.1:

- Improved code readability.
- Fixed many bugs.
- Improved Command response, console, and log formatting.

#### pyMessageBridge v0.1.0

Features of pyMessageBridge 0.1.0:
- An easy way to share messages to multiple numbers
- Web admin panel for adding numbers to the whitelist
    - http://localhost:8000/admin
- Local & remote message log file (MacOS rightly blocks it by default, I will leave this up to the end-user)
-  A remote command feature that works by sending a "¥" character followed by a pre-determined command (Covered in more detail below)