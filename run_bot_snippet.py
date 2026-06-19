import requests
BASE='http://127.0.0.1:5001'
S = requests.Session()
S.post(BASE+'/login', data={'username':'admin','password':'password123'})
tamil_query = 'குற்றம் பற்றிய விவரம்'
r2 = S.post(BASE+'/chat', data={'query':tamil_query}, allow_redirects=True)
text = r2.text
bot_idx = text.rfind('<div class="message bot">')
print('bot_idx', bot_idx)
if bot_idx!=-1:
    print(text[bot_idx:bot_idx+2000])
else:
    print('bot div not found')
