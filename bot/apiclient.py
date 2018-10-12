import os
import requests

class APIClient:
    token = None

    def set_auth_headers(self):
        data = {
            'username': os.environ.get('API_USER'),
            'password': os.environ.get('API_PASS')
        }
        r = requests.post('http://localhost:8000/api/token/', data=data)
        self.token = r.json()

    def get(self, url):
        headers = {}
        if not self.token:
            self.set_auth_headers()
        headers['Authorization'] = 'Bearer ' + self.token['access']
        r = requests.get(url, headers = headers)
        return r.text