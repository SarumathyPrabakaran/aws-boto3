import boto3
import json

def get_bucket_info(bucket_name):
    s3_client = boto3.client('s3')

    # Get bucket location
    location_response = s3_client.get_bucket_location(Bucket=bucket_name)
    bucket_region = location_response.get('LocationConstraint', 'ap-south-1')

    # Head bucket for metadata
    head_response = s3_client.head_bucket(Bucket=bucket_name)
    bucket_status = "Active"  # Buckets that you can access typically are considered active

    # List objects
    list_objects_response = s3_client.list_objects(Bucket=bucket_name)
    objects = list_objects_response.get('Contents', [])

    # Prepare the output dictionary
    bucket_info = {
        'BucketName': bucket_name,
        'Region': bucket_region,
        'Status': bucket_status,
        'Objects': []
    }

    for obj in objects:
        object_key = obj['Key']
        object_size = obj['Size']

        # Get object metadata
        object_metadata_response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        # Extract metadata from the response

        # Append object information to the bucket info
        bucket_info['Objects'].append({
            'ObjectKey': object_key,
            'Size': object_size,
            'Metadata': object_metadata_response
        })

    return bucket_info

def main():
    s3_client = boto3.client('s3')

    response = s3_client.list_buckets()
    buckets = response['Buckets']

    all_bucket_info = []

    for bucket in buckets:
        bucket_name = bucket['Name']
        bucket_info = get_bucket_info(bucket_name)
        all_bucket_info.append(bucket_info)

    # Print the information in JSON format
    with open('hello.json','w+') as f:
        data = {
            "Buckets" :all_bucket_info
        }
        (json.dump(data,f, indent=2))

if __name__ == "__main__":
    main()
