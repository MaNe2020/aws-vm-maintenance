import boto3
from botocore.config import Config

def lambda_handler(event, context):
    
    prodInstancesList = ['i-00e661ddf9010ab9f', 'i-07d1cbb592c26b8b7', 'i-07098cdaf17dda77b',
    'i-04820952d73b4e222','i-09a02b16dd9e20952','i-014cd65aec4e3ed48','i-0badf3228c7723217',
    'i-0d72ceba0317145d7']
        
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
                'running'
            ]
        },
        ])
        tobeStoppedInstances= []
        for instanceReservations in instanceIdList['Reservations']:
            for instance in instanceReservations['Instances']:
                if (instance['InstanceId'] not in prodInstancesList):
                    tobeStoppedInstances.append(instance['InstanceId'])
                    #print (instance['InstanceId'] + " - To be stopped")
                else:
                    print (instance['InstanceId'] + " - NOT To be stopped")
        if(len(tobeStoppedInstances) > 0):
            print("tobeStopped Instances: "+ str(tobeStoppedInstances))
            #ec2client.stop_instances(InstanceIds=instances)