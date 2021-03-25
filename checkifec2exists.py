import boto3
from botocore.config import Config
import requests

def lambda_handler(event, context):
    
    prodInstancesList = []
    instanceTxt = 'https://raw.githubusercontent.com/k8-proxy/aws-vm-maintenance/main/instances.txt'
    r = requests.get(instanceTxt)
    with open('instances.txt', 'wb') as f:
        f.write(r.content)
    with open('instances.txt') as f:
        instanceList = f.read().splitlines()
    for instanceId in instanceList:
        prodInstancesList.append(instanceId.split(":")[0])
    client = boto3.client('ec2')
    
    for region in client.describe_regions()['Regions']:
        ec2Config = Config(
            region_name=region['RegionName'],
            signature_version='v4',
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
        ec2client = boto3.client('ec2',config=ec2Config)
        instanceIdList = ec2client.describe_instances( Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'running','stopped'
            ]
        },
        ])
        for instanceReservations in instanceIdList['Reservations']:
            for instance in instanceReservations['Instances']:
                if (instance['InstanceId'] in prodInstancesList):
                    print (instance['InstanceId'] + " - Found")

if __name__ == "__main__":
    lambda_handler("test","test")