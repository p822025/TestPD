import requests
import json

req = requests.get('https://github.com/timeline.json')
doc=json.loads(req.text)
print (doc['message'])
