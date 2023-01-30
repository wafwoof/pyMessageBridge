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
-  A command system for remote kill-switch and other power user features

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
- Python 3+ (3.11 really speeds up certain things)
- uvicorn, fastapi, requests, pm2 (optional, but recommended)

Start by running ./server-start.sh in the terminal. If everything is configured correctly, it should start without any error messages.

