#### How to Install Jared:
*Note:* I strongly recommend using noJared as it is much faster.

- A tested version can be found in ./jared/ unzip it.
- Enable Jared, disable sending messages, enable REST API, do not add a contacts list.

![Jared Main Settings](/jared/JARED_EXAMPLE.png)

- After installing: replace ~/Library/Application Support/Jared/config.json with included backup file in /jared/
    - `cp .../pyMessageBridge/jared/backup_jared_config.json ~/Library/Application\ Support/Jared/config.json`
- Reboot Jared.
    - (Rebooting your Mac frequently solves lots of small issues from experience)

Jared is now configured and is already sending messages.