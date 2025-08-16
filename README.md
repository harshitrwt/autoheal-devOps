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
