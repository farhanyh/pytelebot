import os
import requests

headers = {}
# headers['Authorization'] = 'Bearer '

# r = requests.get('http://localhost:8000/api/token/', headers = headers)
data = {
    'username': os.environ.get('API_USER'),
    'password': os.environ.get('API_PASS')
}
r = requests.post('http://localhost:8000/api/token/', data=data)

print(r.json()['refresh'])