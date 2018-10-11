import requests

headers = {}
# headers['Authorization'] = 'Bearer '

# r = requests.get('http://localhost:8000/api/token/', headers = headers)
r = requests.post('http://localhost:8000/api/token/', data={'username':'admin','password':'Testing321'})

print(r.json()['refresh'])