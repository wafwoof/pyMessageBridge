# pyMessageServer setup script

import json

# get input from user
print("\n######################################")
print("#### pyMessageServer setup script ####")
print("######################################")
techphoneNumber = input("Please enter your techphone number (Format: +15555555555): ")

# create template config file
with open('server.config.json', 'w') as config_file:
    json.dump({
        "techphoneNumber": techphoneNumber,
        "managerWhitelist": [],
        "textCommandSymbol": "¥",
        "forwardOutgoingMessages": False
    }, config_file, indent=4)
    config_file.close()

# create empty log.txt
with open('log.txt', 'w') as log_file:
    log_file.close()


print("\nSetup is complete. Thank you for using pyMessageServer!")
print("Please run 'bash run-pyMessageBridge+noJared.sh' to start.")