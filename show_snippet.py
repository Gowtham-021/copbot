import requests
r = requests.get('http://127.0.0.1:5001/chat')
s = r.text
idx = s.find('குற்றம் பற்றிய விவரம்')
print('idx', idx)
if idx!=-1:
    print(s[idx:idx+1000])
else:
    print('not found')
