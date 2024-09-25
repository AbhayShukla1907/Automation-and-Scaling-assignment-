import boto3
from botocore.exceptions import ClientError

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

# Create Scaling Policies
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

if __name__ == "__main__":
    as_client = boto3.client('autoscaling', region_name='us-west-2')  # Use your region
    ec2_client = boto3.client('ec2', region_name='us-west-2')

    lc_name = "my-launch-configuration"
    asg_name = "my-auto-scaling-group"
    tg_arn = "arn:aws:elasticloadbalancing:us-west-2:975050024946:targetgroup/my-alb-tg/db9ef0f419430992"  # Replace with your target group ARN
    subnet_ids = ["subnet-09bd0e0acc92d4efa", "subnet-03ca36de9a927fe8e"]
    security_group_id = "sg-02b95c4bb391a2617"
    ami_id = "ami-05134c8ef96964280"
    instance_type = "t2.micro"
    key_name = "AbhayKey"

    # Create Launch Configuration
    create_launch_configuration(as_client, lc_name, ami_id, instance_type, key_name, security_group_id)

    # Create Auto Scaling Group
    create_auto_scaling_group(as_client, asg_name, lc_name, tg_arn, subnet_ids, min_size=1, max_size=3)

    # Create Scaling Policies
    scale_up_policy_arn = create_scaling_policy(as_client, "scale-up", asg_name, "ChangeInCapacity", 1, 300)
    scale_down_policy_arn = create_scaling_policy(as_client, "scale-down", asg_name, "ChangeInCapacity", -1, 300)

    print(f"Scale Up Policy ARN: {scale_up_policy_arn}")
    print(f"Scale Down Policy ARN: {scale_down_policy_arn}")
