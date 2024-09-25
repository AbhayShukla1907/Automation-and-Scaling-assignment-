import boto3
from botocore.exceptions import ClientError
import time

# Create an S3 Bucket
def create_s3_bucket(bucket_name, region):
    s3_client = boto3.client('s3', region_name=region)
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
        print(f"S3 bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        print(f"Error creating S3 bucket: {e}")

# Create an EC2 Instance
def create_ec2_instance(ec2_client, ami_id, instance_type, key_name, security_group_id, user_data):
    try:
        instances = ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroupIds=[security_group_id],
            MinCount=1,
            MaxCount=1,
            UserData=user_data
        )
        instance_id = instances['Instances'][0]['InstanceId']
        print(f"EC2 Instance '{instance_id}' launched successfully.")
        return instance_id
    except ClientError as e:
        print(f"Error launching EC2 instance: {e}")

# Create a Security Group
def create_security_group(ec2_client, group_name, description, vpc_id):
    try:
        response = ec2_client.create_security_group(
            GroupName=group_name,
            Description=description,
            VpcId=vpc_id
        )
        security_group_id = response['GroupId']
        print(f"Security Group '{group_name}' created successfully with ID: {security_group_id}")
        return security_group_id
    except ClientError as e:
        print(f"Error creating Security Group: {e}")

# Add Security Group Rules
def add_security_group_rules(ec2_client, security_group_id):
    try:
        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            ]
        )
        print("Security Group rules added successfully.")
    except ClientError as e:
        print(f"Error adding Security Group rules: {e}")

# Create a Load Balancer
def create_load_balancer(elb_client, name, subnets, security_group_id):
    try:
        response = elb_client.create_load_balancer(
            Name=name,
            Subnets=subnets,
            SecurityGroups=[security_group_id],
            Scheme='internet-facing',
            IpAddressType='ipv4',
            Type='application'
        )
        lb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
        print(f"Load Balancer '{name}' created successfully: {lb_arn}")
        return lb_arn
    except ClientError as e:
        print(f"Error creating Load Balancer: {e}")

# Create a Target Group
def create_target_group(elb_client, name, vpc_id):
    try:
        response = elb_client.create_target_group(
            Name=name,
            Protocol='HTTP',
            Port=80,
            VpcId=vpc_id,
            HealthCheckProtocol='HTTP',
            HealthCheckPort='80',
            HealthCheckPath='/',
            HealthCheckIntervalSeconds=30,
            HealthCheckTimeoutSeconds=5,
            HealthyThresholdCount=5,
            UnhealthyThresholdCount=2,
            TargetType='instance'
        )
        tg_arn = response['TargetGroups'][0]['TargetGroupArn']
        print(f"Target Group '{name}' created successfully: {tg_arn}")
        return tg_arn
    except ClientError as e:
        print(f"Error creating Target Group: {e}")

# Register Targets with Target Group
def register_targets(elb_client, tg_arn, instance_id):
    try:
        elb_client.register_targets(
            TargetGroupArn=tg_arn,
            Targets=[{'Id': instance_id}]
        )
        print(f"Instance '{instance_id}' registered with Target Group '{tg_arn}'.")
    except ClientError as e:
        print(f"Error registering target: {e}")

# Create Launch Configuration
def create_launch_configuration(as_client, name, ami_id, instance_type, key_name, security_group_id):
    try:
        as_client.create_launch_configuration(
            LaunchConfigurationName=name,
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroups=[security_group_id]
        )
        print(f"Launch Configuration '{name}' created successfully.")
    except ClientError as e:
        print(f"Error creating Launch Configuration: {e}")

# Create Auto Scaling Group
def create_auto_scaling_group(as_client, name, lc_name, tg_arn, subnet_ids, min_size, max_size):
    try:
        as_client.create_auto_scaling_group(
            AutoScalingGroupName=name,
            LaunchConfigurationName=lc_name,
            MinSize=min_size,
            MaxSize=max_size,
            DesiredCapacity=min_size,
            VPCZoneIdentifier=",".join(subnet_ids),
            TargetGroupARNs=[tg_arn],
            HealthCheckType='EC2',
            HealthCheckGracePeriod=300,
        )
        print(f"Auto Scaling Group '{name}' created successfully.")
    except ClientError as e:
        print(f"Error creating Auto Scaling Group: {e}")

# Create Scaling Policy
def create_scaling_policy(as_client, name, asg_name, adjustment_type, scaling_adjustment, cooldown):
    try:
        response = as_client.put_scaling_policy(
            AutoScalingGroupName=asg_name,
            PolicyName=name,
            AdjustmentType=adjustment_type,
            ScalingAdjustment=scaling_adjustment,
            Cooldown=cooldown
        )
        print(f"Scaling policy '{name}' created successfully.")
        return response['PolicyARN']
    except ClientError as e:
        print(f"Error creating Scaling Policy: {e}")

# Create SNS Topic
def create_sns_topic(sns_client, name):
    try:
        response = sns_client.create_topic(Name=name)
        topic_arn = response['TopicArn']
        print(f"SNS Topic '{name}' created successfully: {topic_arn}")
        return topic_arn
    except ClientError as e:
        print(f"Error creating SNS Topic: {e}")

# Subscribe Email to SNS Topic
def subscribe_email_to_topic(sns_client, topic_arn, email_address):
    try:
        sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email_address
        )
        print(f"Email '{email_address}' subscribed to SNS Topic: {topic_arn}")
    except ClientError as e:
        print(f"Error subscribing email to SNS Topic: {e}")

if __name__ == "__main__":
    region = 'us-west-2'
    s3_bucket_name = 'abhay-web-app-bucket'
    ami_id = 'ami-05134c8ef96964280'
    instance_type = 't2.micro'
    key_name = 'AbhayKey'
    vpc_id = 'vpc-0321f38a7b594180d'
    subnet_ids = ['subnet-09bd0e0acc92d4efa', 'subnet-03ca36de9a927fe8e']
    user_data = '''#!/bin/bash
    yum update -y
    yum install -y httpd
    systemctl start httpd
    systemctl enable httpd
    echo "<h1>Welcome to My Web Server</h1>" > /var/www/html/index.html
    '''
    sns_topic_name = 'abhay-scaling-notifications'
    email_address = 'abhay06072002@gmail.com'

    ec2_client = boto3.client('ec2', region_name=region)
    elb_client = boto3.client('elbv2', region_name=region)
    as_client = boto3.client('autoscaling', region_name=region)
    sns_client = boto3.client('sns', region_name=region)

    # 1. Create S3 Bucket
    create_s3_bucket(s3_bucket_name, region)

    # 2. Create Security Group
    security_group_name = 'web-server-sg'
    security_group_description = 'Security group for web server'
    security_group_id = create_security_group(ec2_client, security_group_name, security_group_description, vpc_id)
    add_security_group_rules(ec2_client, security_group_id)

    # 3. Launch EC2 Instance
    instance_id = create_ec2_instance(ec2_client, ami_id, instance_type, key_name, security_group_id, user_data)
    time.sleep(60)  # Wait for the instance to be in running state

    # 4. Create Load Balancer
    alb_name = 'my-alb'
    alb_arn = create_load_balancer(elb_client, alb_name, subnet_ids, security_group_id)

    # 5. Create Target Group and Register Targets
    target_group_name = 'my-alb-tg'
    tg_arn = create_target_group(elb_client, target_group_name, vpc_id)
    register_targets(elb_client, tg_arn, instance_id)

    # 6. Create Launch Configuration
    lc_name = 'my-launch-configuration'
    create_launch_configuration(as_client, lc_name, ami_id, instance_type, key_name, security_group_id)

    # 7. Create Auto Scaling Group
    asg_name = 'my-auto-scaling-group'
    create_auto_scaling_group(as_client, asg_name, lc_name, tg_arn, subnet_ids, min_size=1, max_size=3)

    # 8. Create Scaling Policy
    scaling_policy_name = 'scale-out-policy'
    create_scaling_policy(as_client, scaling_policy_name, asg_name, 'ChangeInCapacity', 1, 300)

    # 9. Create SNS Topic and Subscribe
    sns_topic_arn = create_sns_topic(sns_client, sns_topic_name)
    subscribe_email_to_topic(sns_client, sns_topic_arn, email_address)

    print("Infrastructure deployed successfully.")
