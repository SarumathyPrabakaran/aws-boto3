import boto3

ec2 = boto3.resource('ec2')

# instance id should be specified here
instance = ec2.Instance('i-0b902d')

for tag in instance.tags:
    if tag['Key'] == 'Name':
        name = tag['Value']
        break
else:
    name = 'Unnamed'

print(name)