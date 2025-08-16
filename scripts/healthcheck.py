#!/usr/bin/env python3
import requests

EC2_IP = "54.173.115.63"
NGROK_URL = "https://your-ngrok-url.ngrok.io"  # replace with your actual ngrok URL

EC2_HEALTH_URL = f"http://{EC2_IP}"

def is_ec2_healthy():
    try:
        resp = requests.get(EC2_HEALTH_URL, timeout=5)
        return resp.status_code == 200
    except requests.RequestException:
        return False

def is_local_healthy():
    try:
        resp = requests.get(NGROK_URL, timeout=5)
        return resp.status_code == 200
    except requests.RequestException:
        return False

if __name__ == "__main__":
    if is_ec2_healthy():
        print("EC2 is healthy")
    elif is_local_healthy():
        print("EC2 is down — switching to local/ngrok which is healthy")
    else:
        print("Both EC2 and local/ngrok are down")
