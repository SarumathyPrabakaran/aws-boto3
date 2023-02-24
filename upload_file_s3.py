import boto3


s3 = boto3.client('s3')

s3.upload_file('/home/saru/Desktop/hello.txt', 'my-first-bucket', 'text-files-object')


