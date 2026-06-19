import requests
BASE='http://127.0.0.1:5001'
S = requests.Session()
S.post(BASE+'/login', data={'username':'admin','password':'password123'})
tamil_query = 'குற்றம் பற்றிய விவரம்'
r2 = S.post(BASE+'/chat', data={'query':tamil_query}, allow_redirects=True)
print('POST status', r2.status_code)
print('---response snippet---')
print(r2.text[:2000])
