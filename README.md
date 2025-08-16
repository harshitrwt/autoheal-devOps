# Autohealing App Deployment

This project demonstrates the deployment of a Dockerized web application on an AWS EC2 instance using Terraform, Ansible, and Minikube for local redundancy and auto-healing simulation. The AWS-hosted app is exposed to the internet, while the same app runs locally in a Kubernetes cluster for potential fallback or testing scenarios.

## Project Structure


## Features

- Deploys an Ubuntu EC2 instance using Terraform
- Provisions the instance with Docker and the application using Ansible
- Docker container exposes the app on port 80 (or 3001)
- Minikube used to run the same app locally as a backup or for development
- ngrok used to tunnel local app traffic for fallback or remote access

## Prerequisites

- AWS CLI configured with access credentials
- Terraform installed and initialized
- Ansible installed
- ngrok installed and authenticated
- A valid `.pem` SSH key registered in AWS EC2 Key Pairs

## Deployment Steps

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/autoheal-devops.git
cd autoheal-devops
```

## What Happens After Deployment

Once the EC2 instance is deployed and configured, the following steps are automatically completed:

1. **Ubuntu EC2 instance is launched**
   - Based on the Ubuntu AMI specified in the Terraform file
   - Accessible via SSH using the `.pem` key file

2. **Security group is configured**
   - Allows inbound traffic on ports:
     - `22` for SSH
     - `80` for HTTP (or `3001` if using custom port mapping)
   - Allows all outbound traffic

3. **Ansible provisions the EC2 instance**
   - Updates the APT package index
   - Installs Docker (`docker.io`)
   - Ensures the Docker service is enabled and running
   - Installs `pip` and Python Docker SDK for managing containers
   - Pulls the application image from Docker Hub
   - Runs the application container with specified port mappings (e.g., `80:3001`)

4. **Application is accessible**
   - Via public IP on port `80`:
     ```
     http://<your-ec2-public-ip>/
     ```
   - Or on port `3001` if configured that way:
     ```
     http://<your-ec2-public-ip>:3001/
     ```

5. **Docker container is active**
   - Verified with `docker ps`
   - The app runs inside the container and listens on port `3001` internally

6. **You can SSH into the instance**
   - Using:
     ```bash
     ssh -i ~/.ssh/your-key.pem ubuntu@<your-ec2-public-ip>
     ```

7. **Optional: Tunnel traffic using ngrok**
   - If needed, expose the app using:
     ```bash
     ngrok http 80
     ```
   - Useful for testing or routing traffic between AWS and Minikube

