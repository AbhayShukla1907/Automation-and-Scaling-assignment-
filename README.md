# Automation-and-Scaling-assignment-
This project automates the deployment and management of a web application hosted on AWS EC2 instances. It includes auto-scaling based on traffic, load balancing, health monitoring, and sending notifications to administrators about scaling events and infrastructure status.

## Project Overview
This project uses AWS services like EC2, S3, Application Load Balancer (ALB), Auto Scaling Groups (ASG), and Simple Notification Service (SNS) to manage the lifecycle of the web application. It also employs Python's boto3 library to automate the infrastructure.

## Key Components
1. S3 Bucket: Stores static files for the web application.
2. EC2 Instances: Hosts the web application.
3. Application Load Balancer (ALB): Distributes traffic across multiple EC2 instances.
4. Auto Scaling Group (ASG): Automatically scales the number of EC2 instances based on traffic.
5. SNS Notifications: Sends notifications about the health of the system, scaling events, and traffic spikes.

## Project Structure
"create_s3_bucket.py": Creates an S3 bucket to store static files.
"launch_ec2.py": Launches an EC2 instance and configures it as a web server.
"create_load_balancer.py": Sets up an Application Load Balancer (ALB) and registers the EC2 instance(s).
"setup_auto_scaling.py": Configures an Auto Scaling Group (ASG) to handle scaling based on CPU utilization.
"setup_sns.py": Sets up Simple Notification Service (SNS) to send alerts.
"deploy_infrastructure.py": A single script to deploy, update, or tear down the infrastructure.
"README.md": Documentation for the project.

## Prerequisites
Before running the scripts, ensure you have the following:

1. AWS Account: An active AWS account with permissions to create EC2, S3, ALB, ASG, and SNS resources.
2. Python 3: Installed on your local machine.
3. Boto3: Python library for interacting with AWS. Install it via pip:
"pip install boto3"
4. AWS CLI Configured: Ensure AWS CLI is configured with your credentials:
"aws configure"

## Setup Instructions
### Step 1: Create an S3 Bucket
Create a bucket to store static files of the web application:
"python create_s3_bucket.py"
### Step 2: Launch EC2 Instance
Launch an EC2 instance with the correct AMI ID and configure it as a web server (e.g., Nginx):
"python launch_ec2.py"
### Step 3: Set Up the Load Balancer
Create an Application Load Balancer (ALB) and register the EC2 instance with it:
"python create_load_balancer.py"
### Step 4: Configure Auto Scaling
Set up an Auto Scaling Group (ASG) to automatically scale the EC2 instances based on CPU utilization:
"python setup_auto_scaling.py"
### Step 5: Set Up SNS Notifications
Create SNS topics and configure alerts to notify administrators about the infrastructure's health, scaling events, or traffic surges:
"python setup_sns.py"
### tep 6: Automate Infrastructure Deployment
To automate the deployment, updates, or teardown of the entire infrastructure, run:
"python deploy_infrastructure.py"


## Optional Enhancements
Dynamic Content Handling: The web application can be extended to store user-uploaded files in S3, with the EC2 instance acting as a temporary storage.

## Clean Up Resources
Once you're done with the project, ensure you clean up the resources to avoid unnecessary charges:
"python deploy_infrastructure.py --destroy"

## Technologies Used
AWS EC2: Virtual machines to run the web application.
AWS S3: Object storage for static files and user-generated content.
AWS Application Load Balancer: Distributes incoming traffic across multiple EC2 instances.
AWS Auto Scaling Group: Dynamically adjusts the number of instances based on demand.
AWS SNS: Sends email/SMS notifications.
Python (boto3): Automates infrastructure management using AWS APIs.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any issues, feel free to reach out:

Name: Abhay Kumar Shukla

Email: abhay06072002@gmail.com

GitHub: https://github.com/AbhayShukla1907

LinkedIn: https://www.linkedin.com/in/abhay-shukla-65818330a/


This README serves as a guide for the project and provides all the essential details to understand and run the automation scripts.











