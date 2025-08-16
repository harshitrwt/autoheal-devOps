import requests
from flask import Flask, request, Response
import threading
import time

app = Flask(__name__)

EC2_IP = "54.173.115.63"            
NGROK_URL = "https://ngrok-url.ngrok.io"  

EC2_HEALTH_URL = f"http://{EC2_IP}"

current_target = EC2_IP

def health_check():
    global current_target
    while True:
        try:
            r = requests.get(EC2_HEALTH_URL, timeout=5)
            if r.status_code == 200:
                current_target = EC2_IP
                print("EC2 is healthy, routing to EC2")
            else:
                current_target = NGROK_URL
                print("EC2 unhealthy, routing to ngrok")
        except:
            current_target = NGROK_URL
            print("EC2 unreachable, routing to ngrok")
        time.sleep(10) 

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    global current_target
    if current_target == EC2_IP:
        url = f"http://{EC2_IP}/{path}"
    else:
        url = f"{NGROK_URL}/{path}"
    method = request.method
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}
    try:
        resp = requests.request(method, url, headers=headers, data=request.get_data(), allow_redirects=False)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        return Response(resp.content, resp.status_code, response_headers)
    except Exception as e:
        return f"Error connecting to backend: {e}", 502

if __name__ == "__main__":
    threading.Thread(target=health_check, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
