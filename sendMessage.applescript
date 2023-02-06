
on run {targetBuddyPhone, targetMessage}

    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy targetBuddyPhone of targetService
        send targetMessage to targetBuddy
        log "AppleScript: Sent message to " & targetBuddyPhone & " with text: " & targetMessage
    end tell

end run