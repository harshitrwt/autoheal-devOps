provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "app_sg" {
  name        = "autohealing-app-sg"
  description = "Allow SSH and HTTP"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app_instance" {
  ami                         = "ami-0c02fb55956c7d316" 
  instance_type               = "t2.micro"              
  key_name                    = "autohealing-key"
  security_groups             = [aws_security_group.app_sg.name]
  associate_public_ip_address = true

  tags = {
    Name = "AutoHealingApp"
  }
}

output "instance_ip" {
  value = aws_instance.app_instance.public_ip
}
