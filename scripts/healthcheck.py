import os
import requests
import boto3
from dotenv import load_dotenv

load_dotenv("config.env")

AWS_REGION = os.getenv("AWS_REGION")
PRIMARY_INSTANCE_ID = os.getenv("PRIMARY_INSTANCE_ID")
BACKUP_INSTANCE_ID = os.getenv("BACKUP_INSTANCE_ID")
HOSTED_ZONE_ID = os.getenv("HOSTED_ZONE_ID")
DNS_RECORD_NAME = os.getenv("DNS_RECORD_NAME")
HEALTH_CHECK_URL = os.getenv("HEALTH_CHECK_URL")

ec2 = boto3.client("ec2", region_name=AWS_REGION)
route53 = boto3.client("route53")

def is_healthy():
    try:
        response = requests.get(HEALTH_CHECK_URL, timeout=5)
        return response.status_code == 200
    except:
        return False

def start_instance(instance_id):
    ec2.start_instances(InstanceIds=[instance_id])
    print(f"Started instance {instance_id}")

def stop_instance(instance_id):
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Stopped instance {instance_id}")

def get_instance_ip(instance_id):
    reservations = ec2.describe_instances(InstanceIds=[instance_id])["Reservations"]
    for reservation in reservations:
        for instance in reservation["Instances"]:
            return instance["PublicIpAddress"]

def update_dns(ip):
    route53.change_resource_record_sets(
        HostedZoneId=HOSTED_ZONE_ID,
        ChangeBatch={
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": DNS_RECORD_NAME,
                        "Type": "A",
                        "TTL": 60,
                        "ResourceRecords": [{"Value": ip}],
                    }
                }
            ]
        }
    )
    print(f"DNS updated to {ip}")

def main():
    if is_healthy():
        print("Primary is healthy.")
        stop_instance(BACKUP_INSTANCE_ID)
    else:
        print("Primary failed. Switching to backup...")
        start_instance(BACKUP_INSTANCE_ID)
        ip = get_instance_ip(BACKUP_INSTANCE_ID)
        update_dns(ip)

if __name__ == "__main__":
    main()
