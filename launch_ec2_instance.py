import boto3
from botocore.exceptions import ClientError

def launch_ec2_instance():
    try:
        # Create EC2 client
        ec2_client = boto3.client('ec2', region_name='us-west-2')
        
        # Launch the EC2 instance
        instances = ec2_client.run_instances(
            ImageId='ami-05134c8ef96964280',
            InstanceType='t2.micro',
            KeyName='AbhayKey',
            MinCount=1,
            MaxCount=1,
            SecurityGroupIds=['sg-062dec5485f28b71a'],
            SubnetId='subnet-0f30c30418def6379',
            UserData='''#!/bin/bash
                        sudo apt update -y
                        sudo apt install apache2 -y
                        sudo systemctl start apache2
                        sudo systemctl enable apache2
                        echo "Hello from EC2 instance!" > /var/www/html/index.html
                        '''
        )
        
        # Print instance details
        print("EC2 Instance launched successfully. Instance ID:", instances['Instances'][0]['InstanceId'])

    except ClientError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    launch_ec2_instance()
