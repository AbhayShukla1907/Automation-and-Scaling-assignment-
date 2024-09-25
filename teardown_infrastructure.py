import boto3
from botocore.exceptions import ClientError
import time

# Delete the Auto Scaling Group
def delete_auto_scaling_group(as_client, asg_name):
    try:
        as_client.update_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            MinSize=0,
            DesiredCapacity=0
        )
        time.sleep(120)  # Wait for instances to terminate
        as_client.delete_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            ForceDelete=True
        )
        print(f"Auto Scaling Group '{asg_name}' deleted successfully.")
    except ClientError as e:
        print(f"Error deleting Auto Scaling Group: {e}")

# Delete the Launch Configuration
def delete_launch_configuration(as_client, lc_name):
    try:
        as_client.delete_launch_configuration(
            LaunchConfigurationName=lc_name
        )
        print(f"Launch Configuration '{lc_name}' deleted successfully.")
    except ClientError as e:
        print(f"Error deleting Launch Configuration: {e}")

# Delete the Load Balancer
def delete_load_balancer(elb_client, alb_arn):
    try:
        elb_client.delete_load_balancer(
            LoadBalancerArn=alb_arn
        )
        print(f"Load Balancer '{alb_arn}' deleted successfully.")
    except ClientError as e:
        print(f"Error deleting Load Balancer: {e}")

# Delete the Target Group
def delete_target_group(elb_client, tg_arn):
    try:
        elb_client.delete_target_group(
            TargetGroupArn=tg_arn
        )
        print(f"Target Group '{tg_arn}' deleted successfully.")
    except ClientError as e:
        print(f"Error deleting Target Group: {e}")

# Terminate EC2 Instance
def terminate_ec2_instance(ec2_client, instance_id):
    try:
        ec2_client.terminate_instances(
            InstanceIds=[instance_id]
        )
        print(f"EC2 Instance '{instance_id}' terminated successfully.")
        ec2_client.get_waiter('instance_terminated').wait(InstanceIds=[instance_id])
    except ClientError as e:
        print(f"Error terminating EC2 instance: {e}")

# Delete Security Group
def delete_security_group(ec2_client, security_group_id):
    try:
        ec2_client.delete_security_group(
            GroupId=security_group_id
        )
        print(f"Security Group '{security_group_id}' deleted successfully.")
    except ClientError as e:
        print(f"Error deleting Security Group: {e}")

# Delete S3 Bucket
def delete_s3_bucket(s3_client, bucket_name):
    try:
        # First, delete all objects in the bucket
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket.objects.all().delete()
        # Then, delete the bucket itself
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"S3 Bucket '{bucket_name}' deleted successfully.")
    except ClientError as e:
        print(f"Error deleting S3 bucket: {e}")

if __name__ == "__main__":
    region = 'us-west-2'
    s3_bucket_name = 'abhay-web-app-bucket'
    instance_id = 'i-00ead5d124d5cda08'
    security_group_id = 'sg-02b95c4bb391a2617'
    alb_arn = 'arn:aws:elasticloadbalancing:us-west-2:975050024946:loadbalancer/app/abhay-tm-loadbalancer/7fb4ba42223e7cc5'
    tg_arn = 'arn:aws:elasticloadbalancing:us-west-2:975050024946:targetgroup/abhay-tm-targetgroup/9768a6150d65b8b3'
    asg_name = 'my-auto-scaling-group'
    lc_name = 'my-launch-configuration'

    ec2_client = boto3.client('ec2', region_name=region)
    elb_client = boto3.client('elbv2', region_name=region)
    as_client = boto3.client('autoscaling', region_name=region)
    s3_client = boto3.client('s3', region_name=region)

    # 1. Delete Auto Scaling Group
    delete_auto_scaling_group(as_client, asg_name)

    # 2. Delete Launch Configuration
    delete_launch_configuration(as_client, lc_name)

    # 3. Delete Load Balancer
    delete_load_balancer(elb_client, alb_arn)

    # 4. Delete Target Group
    delete_target_group(elb_client, tg_arn)

    # 5. Terminate EC2 Instance
    terminate_ec2_instance(ec2_client, instance_id)

    # 6. Delete Security Group
    delete_security_group(ec2_client, security_group_id)

    # 7. Delete S3 Bucket
    delete_s3_bucket(s3_client, s3_bucket_name)

    print("Infrastructure teardown completed successfully.")
