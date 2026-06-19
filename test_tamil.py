import requests
BASE='http://127.0.0.1:5001'
S = requests.Session()
# login
r = S.post(BASE+'/login', data={'username':'admin','password':'password123'})
print('Login status:', r.status_code)
# post a tamil query
tamil_query = 'குற்றம் பற்றிய விவரம்'  # asks about crimes
r2 = S.post(BASE+'/chat', data={'query':tamil_query}, allow_redirects=True)
print('Chat post status:', r2.status_code)
# fetch chat page
r3 = S.get(BASE+'/chat')
print('Chat page length:', len(r3.text))
idx = r3.text.find('குற்ற')
if idx!=-1:
    print('Found Tamil snippet:')
    print(r3.text[idx-80:idx+200])
else:
    print('Tamil keywords not found in page.')
