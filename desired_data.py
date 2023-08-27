import boto3
import json
from check_public_private import get_bucket_data,get_object_data

def get_object_info(s3_client, bucket_name, object_key):
    object_metadata_response = s3_client.get_object_attributes(Bucket=bucket_name, Key=object_key,ObjectAttributes=[
       'ETag','Checksum','ObjectParts','StorageClass','ObjectSize',
    ])

    # object_info = {
    #     'Key': object_key,
    #     'LastModified': object_metadata_response['LastModified'].isoformat(),
    #     'ETag': object_metadata_response['ETag'],
    #     'Size': object_metadata_response['ContentLength'],
    #     'StorageClass': object_metadata_response['StorageClass'],
    #     'Public': 'Public' in object_metadata_response['WebsiteRedirectLocation'],  # Check if it's public
    #     'Owner': object_metadata_response['Owner'],
    #     
    # }
    for key,val in object_metadata_response.items():
        if key=='last-modified' or key=="date" or key=='LastModified':
            object_metadata_response[key]  = str(val)
            print("yes")
    return object_metadata_response

def get_bucket_info(s3_client, bucket_name):
    location_response = s3_client.get_bucket_location(Bucket=bucket_name)
    bucket_region = location_response.get('LocationConstraint', 'us-east-1')

    head_response = s3_client.head_bucket(Bucket=bucket_name)
    bucket_status = "Active"  # Buckets that you can access typically are considered active

    list_objects_response = s3_client.list_objects(Bucket=bucket_name)
    objects = list_objects_response.get('Contents', [])

    bucket_info = {
        'BucketName': bucket_name,
        'Region': bucket_region,
        'Status': bucket_status,
        'IsPublic': head_response.get('ResponseMetadata', {}).get('HTTPHeaders', {}).get('x-amz-acl', '') == 'public-read',
        'Objects': []
    }

    for obj in objects:
        object_key = obj['Key']
        object_info = get_object_info(s3_client, bucket_name, object_key)
        bucket_info['Objects'].append(object_info)

    return bucket_info



def main():
    s3_client = boto3.client('s3')

    response = s3_client.list_buckets()
    
    buckets = response['Buckets']

    all_bucket_info = []

    s3_resource = boto3.resource('s3')

    for bucket in buckets:
        bucket_name = bucket['Name']
        
        bucket1 = s3_resource.Bucket(bucket_name)
        print("Bucket Creation Date:", bucket1.creation_date)

        bucket_info, private_public_info = get_bucket_data(s3_client, bucket_name)
        bucket_info["CreatedDate"] = str(bucket1.creation_date)
        print(bucket1.objects.all())
        bucket_info.update(private_public_info)
        all_bucket_info.append(bucket_info)

    # Print the information in JSON format
        # Print the information in JSON format
    with open('hello1.json','w+') as f:
        data = {
            "Buckets" :all_bucket_info
        }
        (json.dump(data,f, indent=2))

if __name__ == "__main__":
    main()
