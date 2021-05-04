import boto3
from botocore.config import Config
import urllib3

def lambda_handler(event, context):
    
    prodInstancesList = []
    instanceTxt = 'https://raw.githubusercontent.com/k8-proxy/aws-vm-maintenance/main/instances.txt'
    http = urllib3.PoolManager()
    response = http.request('GET',instanceTxt) 
    with open('/tmp/instances.txt', 'wb') as f:
        f.write(response.data)
    with open('/tmp/instances.txt') as f:
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
                'running'
            ]
        },
        ])
        tobeStoppedInstances= []
        for instanceReservations in instanceIdList['Reservations']:
            for instance in instanceReservations['Instances']:
                if (instance['InstanceId'] not in prodInstancesList):
                    if("InstanceLifecycle" in instance):
                        if(instance['InstanceLifecycle'] == "spot"):
                            print("Encountered Spot Instance: "+str(instance['InstanceId']))
                    else:
                        tobeStoppedInstances.append(instance['InstanceId'])
                    #print (instance['InstanceId'] + " - To be stopped")
                else:
                    print (instance['InstanceId'] + " - NOT To be stopped")
        if(len(tobeStoppedInstances) > 0):
            print("tobeStopped Instances: "+ str(tobeStoppedInstances))
            try:
                ec2client.stop_instances(InstanceIds=tobeStoppedInstances)
                print("Dry run")
            except Exception as e:
                print("Error in stopping Instance: "+str(e))
                continue
