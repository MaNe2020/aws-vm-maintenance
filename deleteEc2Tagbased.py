import boto3
from botocore.config import Config

client = boto3.client('ec2')

print("------- To be terminated Instances ---------------")
for region in client.describe_regions()['Regions']:
    print("\nChecking resources in "+region['RegionName'])
    ec2Config = Config(
        region_name=region['RegionName'],
        signature_version='v4',
        retries={
            'max_attempts': 10,
            'mode': 'standard'
        }
    )

    client = boto3.client('ec2', config=ec2Config)
    custom_filter = [{
        'Name': 'tag:Delete',
        'Values': ['Yes']}]

    toboDeletedInstances = client.describe_instances(Filters=custom_filter)
    instanceIdList=[]
    for instanceReservations in toboDeletedInstances['Reservations']:
        for instance in instanceReservations['Instances']:
            instanceIdList.append(instance['InstanceId'])
            for tag in instance['Tags']:
                if (tag['Key'] == "Owner"):
                    print("Owner: "+tag['Value'] + " - " + instance['InstanceId'] + " - " + instance['State']['Name'] + " - " +region['RegionName'])
                    continue
                print("Owner: NA" + " - " + instance['InstanceId'] + " - " + instance['State']['Name'] + " - " + region['RegionName'])
    if(len(instanceIdList) > 0):
        print("Terminating Instances: "+ str(instanceIdList))
        #client.terminate_instances(InstanceIds=instanceIdList)