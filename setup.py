import json

# create template config file
with open('server.config.json', 'w') as config_file:
    json.dump({
        "techphoneNumber": "+15555555555",
        "managerWhitelist": [],
        "textCommandSymbol": "¥",
        "forwardOutgoingMessages": False
    }, config_file, indent=4)
    config_file.close()

# create empty log.txt
with open('log.txt', 'w') as log_file:
    log_file.close()