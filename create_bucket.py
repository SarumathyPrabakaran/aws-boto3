import logging
import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
def create_bucket(bucket_name, region=None):
    try:
        if region is None:
            
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
        s3_client.put_bucket_acl(
            Bucket=bucket_name,
            ACL='public-read'
        )

    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_file(bucket_name, file_path,object_name,public= None):
    s3_client.upload_file(file_path, bucket_name, object_name)
    if public==1:
        s3_client.put_object_acl(Bucket=bucket_name, Key=object_name, ACL='public-read')


# create_bucket(bucket_name='sarubucket1',region='ap-south-1')
# create_bucket(bucket_name='sarubucket2',region='ap-south-1')
create_bucket(bucket_name='sarubucket3-third',region='ap-south-1')
# create_bucket(bucket_name='sarubucket4',region='ap-south-1')
# create_bucket(bucket_name='sarubucket5',region='ap-south-1')

upload_file('sarubucket3-third',"/home/saru/Desktop/saru/image-gallery/static/dog1.jpg","Object1",1)

# upload_file('sarubucket2',"/home/saru/Desktop/saru/image-gallery/dog2.jpg","Object2")
# upload_file('sarubucket3',"/home/saru/Desktop/saru/image-gallery/dog3.jpg","Object3")
# upload_file('sarubucket4',"/home/saru/Desktop/saru/image-gallery/dog4.jpg","Object4",1)
# upload_file('sarubucket5',"/home/saru/Desktop/saru/image-gallery/dog5.jpg","Object5")
# upload_file('sarubucket1',"/home/saru/Desktop/saru/image-gallery/dog6.jpg","Object6")
# upload_file('sarubucket3',"/home/saru/Desktop/saru/image-gallery/dog7.jpg","Object7")






