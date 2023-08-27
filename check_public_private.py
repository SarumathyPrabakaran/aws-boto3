import boto3
import json
from dotenv import load_dotenv
from pymongo import MongoClient
import os
load_dotenv()



# cluster = MongoClient(os.environ.get('MONGO_URI'))

# db = cluster[os.environ.get('MONGO_DBNAME')]

# collection = db["Buckets"]

def get_object_info(s3_client, bucket_name, object_key):
    object_metadata_response = s3_client.get_object_attributes(Bucket=bucket_name, Key=object_key,ObjectAttributes=[
       'ETag','Checksum','ObjectParts','StorageClass','ObjectSize',
    ])



    for key,val in object_metadata_response.items():
        if key=='last-modified' or key=="date" or key=='LastModified':
            object_metadata_response[key]  = str(val)
            print("yes")
    return object_metadata_response


def get_object_data(s3_client,bucket_name, obj):

            object_key = obj["Key"]
            
            acl = s3_client.get_object_acl(Bucket=bucket_name, Key=object_key)
            is_public = any(grant["Grantee"]["Type"] == "Group" and grant["Grantee"]["URI"] == "http://acs.amazonaws.com/groups/global/AllUsers" and grant["Permission"] == "READ" for grant in acl["Grants"])

            object_metadata = get_object_info(s3_client,bucket_name,object_key)
            object_info = {
                "Key": object_key,
                "Public": is_public,
            
            }

            httpheaders = object_metadata["ResponseMetadata"]["HTTPHeaders"]
            object_metadata.pop("ResponseMetadata")
            object_metadata.update(httpheaders)

            object_info.update(object_metadata)
            return object_info,is_public


def get_bucket_data(s3_client, bucket_name):
        objects = s3_client.list_objects_v2(Bucket=bucket_name)["Contents"]

        location_response = s3_client.get_bucket_location(Bucket=bucket_name)

        bucket_region = location_response.get('LocationConstraint', 'us-east-1')
        

        
        
        object_info_list = []
        public_obj = 0
        for obj in objects:
            obj_data, is_public = get_object_data(s3_client,bucket_name,obj)
            object_info_list.append(obj_data)
            if is_public:
                public_obj+=1

        objects_num = len(objects)

        bucket_info = {
            "BucketName": bucket_name,
            "Bucket Region" : bucket_region,
            "Objects": object_info_list

        }

        private_public_info = {
            "ObjectCount": objects_num,
            "PublicObjectsCount": public_obj,
            "PrivateObjectsCount":objects_num-public_obj
        }
        #object_info_list.append(bucket_info)
    
        return bucket_info,private_public_info

def get_buckets_info(s3_client):
    buckets = s3_client.list_buckets()["Buckets"]
    bucket_info_list = []

    for bucket in buckets:
        public_obj=0
        bucket_name = bucket["Name"]
        
        objects = s3_client.list_objects_v2(Bucket=bucket_name)["Contents"]
        
        object_info_list = []
        
        for obj in objects:
            object_key = obj["Key"]
            
            acl = s3_client.get_object_acl(Bucket=bucket_name, Key=object_key)
            is_public = any(grant["Grantee"]["Type"] == "Group" and grant["Grantee"]["URI"] == "http://acs.amazonaws.com/groups/global/AllUsers" and grant["Permission"] == "READ" for grant in acl["Grants"])
            if is_public:
                public_obj+=1
            object_metadata = get_object_info(s3_client,bucket_name,object_key)
            object_info = {
                "Key": object_key,
                "Public": is_public,
                "Meta data" : object_metadata 
            }
            
            object_info_list.append(object_info)
        objects_num = len(objects)
        bucket_info = {
            "BucketName": bucket_name,
            "Objects": object_info_list

        }


        #collection.insert_one(bucket_info)
        bucket_info_list.append(bucket_info)
    
    return bucket_info_list

if __name__ == "__main__":
    s3 = boto3.client("s3")
    
    bucket_info_list = get_buckets_info(s3)

    # data = {}
    # with open('buckets-data.json','a') as fp:
    #     data["Buckets"] = bucket_info_list
    #     json.dump(data,fp,indent=4)

    for bucket_info in bucket_info_list:
        print(f"Bucket Name: {bucket_info['BucketName']}")
        print("Objects:")
        for obj in bucket_info["Objects"]:
            privacy = "Public" if obj["Public"] else "Private"
            print(f"  Object Key: {obj['Key']} - {privacy}")
        print("=" * 50)
