import boto3
from botocore.exceptions import ClientError

# Create the ALB
def create_alb(name, subnet_ids, security_group_id, ec2_instance_id):
    try:
        elb_client = boto3.client('elbv2', region_name='us-west-2')

        # Create the Load Balancer
        lb_response = elb_client.create_load_balancer(
            Name=name,
            Subnets=subnet_ids,
            SecurityGroups=[security_group_id],
            Scheme='internet-facing',
            Type='application',
            IpAddressType='ipv4'
        )
        lb_arn = lb_response['LoadBalancers'][0]['LoadBalancerArn']
        print(f"Load Balancer created successfully: {lb_arn}")

        # Create Target Group
        target_group_response = elb_client.create_target_group(
            Name=f'{name}-tg',
            Protocol='HTTP',
            Port=80,
            VpcId='vpc-0321f38a7b594180d',
            HealthCheckProtocol='HTTP',
            HealthCheckPort='80',
            HealthCheckPath='/',
            TargetType='instance'
        )
        target_group_arn = target_group_response['TargetGroups'][0]['TargetGroupArn']
        print(f"Target Group created successfully: {target_group_arn}")

        # Register EC2 instance with Target Group
        elb_client.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=[{'Id': ec2_instance_id, 'Port': 80}]
        )
        print(f"EC2 Instance {ec2_instance_id} registered with Target Group.")

        # Create Listener to Forward Traffic to EC2 Instances
        elb_client.create_listener(
            LoadBalancerArn=lb_arn,
            Protocol='HTTP',
            Port=80,
            DefaultActions=[{
                'Type': 'forward',
                'TargetGroupArn': target_group_arn
            }]
        )
        print("Listener created successfully.")

    except ClientError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    name = "my-alb"
    subnet_ids = ["subnet-03ca36de9a927fe8e", "subnet-09bd0e0acc92d4efa"]
    security_group_id = "sg-02b95c4bb391a2617"
    ec2_instance_id = "i-08c3ed9238e31e9ec"

    create_alb(name, subnet_ids, security_group_id, ec2_instance_id)
