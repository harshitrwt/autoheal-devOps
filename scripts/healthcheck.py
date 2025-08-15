#!/usr/bin/env python3
import requests

EC2_IP = "YOUR_EC2_PUBLIC_IP"
LOCAL_IP = "YOUR_LOCAL_PUBLIC_IP"    
EC2_HEALTH_URL = f"http://{EC2_IP}"  

def is_ec2_healthy():
    try:
        resp = requests.get(EC2_HEALTH_URL, timeout=5)
        return resp.status_code == 200
    except requests.RequestException:
        return False

if __name__ == "__main__":
    if is_ec2_healthy():
        print("EC2 is healthy")
    else:
        print("EC2 is down — should switch to local/ngrok")
