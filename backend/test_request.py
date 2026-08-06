import json
import urllib.request
import urllib.error

url = 'http://127.0.0.1:5000/attendance'
data = json.dumps({'rollNo': 'test', 'password': 'test'}).encode('utf-8')
req = urllib.request.Request(url, data, {'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req, timeout=60) as r:
        print('STATUS', r.status)
        print(r.read().decode())
except urllib.error.HTTPError as e:
    print('HTTP', e.code)
    print(e.read().decode())
except Exception as e:
    print('ERR', e)
