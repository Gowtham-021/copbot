import requests
S = requests.Session()
S.post('http://127.0.0.1:5001/login', data={'username':'admin','password':'password123'})
r = S.get('http://127.0.0.1:5001/chat')
print(r.text.split('</head>')[0])
