import requests

BASE='http://127.0.0.1:5001'
S = requests.Session()
# login
r = S.post(BASE+'/login', data={'username':'admin','password':'password123'})
print('Login status:', r.status_code)
# post a query
r2 = S.post(BASE+'/chat', data={'query':'FIR procedure'}, allow_redirects=True)
print('Chat post status:', r2.status_code)
# fetch chat page
r3 = S.get(BASE+'/chat')
print('Chat page length:', len(r3.text))
# print a snippet around FIR header
idx = r3.text.find('FIR Procedure')
if idx!=-1:
    print(r3.text[idx-200:idx+400])
else:
    print('FIR Procedure not found in page.')
