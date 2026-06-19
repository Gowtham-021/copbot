import requests
BASE='http://127.0.0.1:5001'
r = requests.get(BASE+'/login')
print('Status', r.status_code)
idx = r.text.find('tamilnadu-police-logo')
if idx!=-1:
    print(r.text[idx-80:idx+80])
else:
    print('local logo not found')
