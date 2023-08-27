import boto3

#client = boto3.client('macie2')

s3 = boto3.client('s3')

bucket_list = s3.list_buckets()
count = 0
# print(bucket_list)
for i in bucket_list["Buckets"]:
#     response = s3.get_bucket_metrics_configuration(
#     Bucket=i["Name"],
#     Id='fba41ad4c9d65b3bdbc58ce62298dd10566973253263c55da929168a313bb2',
#     ExpectedBucketOwner='548979342906'
# )
    head_response = s3.head_bucket(Bucket=i["Name"])
    print(head_response)

#print(client.describe_buckets())


    
    #     count+=1
    # #print(bucket_list)
    # print(count)
    
    