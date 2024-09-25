import boto3
from botocore.exceptions import ClientError

# Create an SNS Topic
def create_sns_topic(name):
    sns_client = boto3.client('sns', region_name='us-west-2')
    try:
        response = sns_client.create_topic(Name=name)
        topic_arn = response['TopicArn']
        print(f"SNS Topic '{name}' created successfully: {topic_arn}")
        return topic_arn
    except ClientError as e:
        print(f"Error creating SNS Topic: {e}")

# Subscribe an Email Address to an SNS Topic
def subscribe_email_to_topic(topic_arn, email_address):
    sns_client = boto3.client('sns', region_name='us-west-2')
    try:
        sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email_address
        )
        print(f"Email '{email_address}' subscribed to SNS Topic: {topic_arn}")
    except ClientError as e:
        print(f"Error subscribing email to SNS Topic: {e}")

# Subscribe a Phone Number to an SNS Topic (for SMS)
def subscribe_sms_to_topic(topic_arn, phone_number):
    sns_client = boto3.client('sns', region_name='us-west-2')
    try:
        sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='sms',
            Endpoint=phone_number
        )
        print(f"Phone number '{phone_number}' subscribed to SNS Topic: {topic_arn}")
    except ClientError as e:
        print(f"Error subscribing phone number to SNS Topic: {e}")

if __name__ == "__main__":
    # Replace with your own values
    topic_name = "abhay-scaling-notifications"
    email_address = "abhay06072002@gmail.com"
    phone_number = "+916268970026"

    # Create SNS Topic
    topic_arn = create_sns_topic(topic_name)

    # Subscribe to the SNS Topic
    subscribe_email_to_topic(topic_arn, email_address)
