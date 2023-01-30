import sys
import requests

url = 'https://rdmap.dev/chat/submit'

for line in sys.stdin:
    response = requests.post(url, json = {'username': 'iMessage-Forward', 'content': line})
    print(response)