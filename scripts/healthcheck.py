#!/usr/bin/env python3
import requests
import os

CLOUDFLARE_API_TOKEN = "YOUR_CLOUDFLARE_API_TOKEN"  # Generate in Cloudflare Dashboard to My Profile to API Tokens
ZONE_ID = "YOUR_CLOUDFLARE_ZONE_ID"  # in Cloudflare Dashboard under domain's settings
RECORD_ID = "YOUR_DNS_RECORD_ID"     # Use Cloudflare API or dashboard to get it
DNS_NAME = "yourdomain.com"          # domain or subdomain you want to switch
EC2_IP = "YOUR_EC2_PUBLIC_IP"        # Public IP of EC2
LOCAL_IP = "YOUR_LOCAL_PUBLIC_IP"    # Public IP from home network or tunnel
EC2_HEALTH_URL = f"http://{EC2_IP}"  # Endpoint to check (HTTP or HTTPS)


def is_ec2_healthy():
    try:
        resp = requests.get(EC2_HEALTH_URL, timeout=5)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def update_dns(ip):
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{RECORD_ID}"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "type": "A",
        "name": DNS_NAME,
        "content": ip,
        "ttl": 1,      
        "proxied": True 
    }
    r = requests.put(url, headers=headers, json=payload)
    if r.status_code == 200:
        print(f" DNS updated to {ip}")
    else:
        print(f"Failed to update DNS: {r.text}")

if __name__ == "__main__":
    if is_ec2_healthy():
        print("EC2 is healthy")
        update_dns(EC2_IP)
    else:
        print("EC2 is down — Switching to local server")
        update_dns(LOCAL_IP)
