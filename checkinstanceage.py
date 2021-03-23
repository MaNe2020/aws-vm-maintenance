import boto3
from datetime import datetime as dt, timezone, timedelta
from botocore.config import Config


def lambda_handler(event, context):
    
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
                'stopped'
            ]
        },
        ])
        for instanceReservations in instanceIdList['Reservations']:
            for instance in instanceReservations['Instances']:
                response = ec2client.get_console_output(InstanceId=instance["InstanceId"])
                if((dt.now(timezone.utc) - timedelta(days=7)) > response['Timestamp']):
                    ownerFound = False
                    if 'Tags' in instance:
                        for tag in instance['Tags']:
                            if(ownerFound):
                                break
                            if (tag['Key'] == "Owner"):
                                ownerFound = True
                                ownerName= tag['Value']
                    if not ownerFound:
                        trailConfig = Config(
                            region_name=region['RegionName'],
                            signature_version='v4',
                            retries={
                                'max_attempts': 10,
                                'mode': 'standard'
                            }
                        )
                        client = boto3.client('cloudtrail',config=trailConfig)
                        trailResponse = client.lookup_events(
                            LookupAttributes=[
                                {
                                    'AttributeKey': 'ResourceName',
                                    'AttributeValue': instance['InstanceId']
                                },
                            ],
                        )
                        for events in trailResponse['Events']:
                            if(events['EventName'] == 'RunInstances'):
                                ownerName= events['Username']
                    print("Owner: "+ownerName+":"+instance['InstanceId']+":"+region['RegionName']+" Created Time: "+str(instance["LaunchTime"].strftime("%B %d, %Y"))+" Last active Time: "+str(response['Timestamp'].strftime("%B %d, %Y")))
                

if __name__ == "__main__":
    lambda_handler("test","test")
