import boto3

s3 = boto3.client('s3')

bucket_list = s3.list_buckets()
count = 0
for i in bucket_list['Buckets']:
    #print(i)
    count+=1
#print(bucket_list)
print(count)
    
    