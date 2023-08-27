import boto3

# Initialize S3 resource
s3_resource = boto3.resource('s3')

# Replace 'your-bucket-name' with the actual name of the bucket
bucket_name = 'sarubucket2-second'

# Get the bucket as an object
bucket = s3_resource.Bucket(bucket_name)

# Get bucket location
# bucket_location = s3_resource.meta.client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']

# # Get bucket details
# bucket_details = {
#     "location": bucket_location,
#     "name": bucket.name,
#     "bucket": bucket
# }

# List to hold object details
s3_object_details = []

# Iterate through all objects in the bucket
for obj in bucket.objects.all():
    object_key = obj.key
    object_last_modified = obj.last_modified
    object_etag = obj.e_tag
    object_size = obj.size
    object_storage_class = obj.storage_class

    # Additional information about the object
    object_info = {
        "key": object_key,
        "last_modified": object_last_modified,
        "etag": object_etag,
        "size": object_size,
        "storage_class": object_storage_class,
        "public": False  # You can set this to True if the object is public
        # Add more details as needed
    }
    
    # Append object details to the list
    s3_object_details.append(object_info)

# Combine bucket details and object details
bucket_info = {
    
    "creation_date": bucket.creation_date,
    "ISPUBLIC": False,  # Set to True if the bucket is public
    "s3_objects": s3_object_details
}

# Print the collected information
print(bucket_info)
