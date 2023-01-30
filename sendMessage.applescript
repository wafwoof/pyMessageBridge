
on run {targetBuddyPhone, targetMessage}

    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy targetBuddyPhone of targetService
        send targetMessage to targetBuddy
        log "Completed Sending Message."
    end tell

end run