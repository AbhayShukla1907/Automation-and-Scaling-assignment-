import boto3
from botocore.exceptions import ClientError

def create_s3_bucket(bucket_name, region=None):
    # Create S3 client
    s3_client = boto3.client('s3', region_name=region)
    
    try:
        # Create S3 bucket
        if region:
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        else:
            s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created successfully.")
    except ClientError as e:
        print(f"Error: {e}")
        return False
    return True

if __name__ == "__main__":
    bucket_name = "abhaywebbucket"
    region = "us-west-2"
    
    # Call the function to create the bucket
    create_s3_bucket(bucket_name, region)
