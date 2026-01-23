import urllib.request
import json

url = "http://localhost:8000/api/login/"
data = {
    "username": "admin",
    "password": "Admin123!"
}
headers = {'Content-Type': 'application/json'}

req = urllib.request.Request(
    url, 
    data=json.dumps(data).encode('utf-8'), 
    headers=headers, 
    method='POST'
)

try:
    with urllib.request.urlopen(req) as response:
        print("✅ Login exitoso (Estado 200)")
        print(response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"❌ Error en Login: {e.code} {e.reason}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print(f"❌ Error de conexión: {e}")
