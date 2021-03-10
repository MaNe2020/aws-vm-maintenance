import boto3
from botocore.config import Config
#import json, requests

def lambda_handler(event, context):
    client = boto3.client('ec2')
    output = "------- Non Complaint Ec2 Instances ---------------"
    for region in client.describe_regions()['Regions']:
        #output+= "\n____Checking in "+region['RegionName']+"____"
        if (region['RegionName'] in ['ap-northeast-3']):
            print("Current Issue. Skipping...")
            continue
        instanceIdList=[]
        nonComplainceReason={}
        configServiceConfig = Config(
            region_name=region['RegionName'],
            signature_version='v4',
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
        configClient = boto3.client('config',config=configServiceConfig)
        response = configClient.get_compliance_details_by_config_rule(
            ConfigRuleName='RequiredTagsForEC2Instances',
            ComplianceTypes=['NON_COMPLIANT'],
                Limit=100
        )
    
        for results in response['EvaluationResults']:
                nonComplainceReason[results['EvaluationResultIdentifier']['EvaluationResultQualifier'].get('ResourceId')] = results['Annotation']
                instanceIdList.append(results['EvaluationResultIdentifier']['EvaluationResultQualifier'].get('ResourceId'))
        ec2Config = Config(
            region_name=region['RegionName'],
            signature_version='v4',
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
        if len(instanceIdList) > 0:
            ec2client = boto3.client('ec2',config=ec2Config)
            toboDeletedInstances = ec2client.describe_instances( Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    'pending', 'running', 'shutting-down', 'stopping' , 'stopped'
                ]
            },
            ],InstanceIds=instanceIdList)
            for instanceReservations in toboDeletedInstances['Reservations']:
                for instance in instanceReservations['Instances']:
                    ownerFound =False
                    if 'Tags' in instance:
                        for tag in instance['Tags']:
                            if(ownerFound):
                                break
                            if (tag['Key'] == "Owner"):
                                output+="\nOwner: "+tag['Value'] + " - " + instance['InstanceId'] + " - " + instance['State']['Name'] + " - " + region['RegionName']# + " - "+ nonComplainceReason[instance['InstanceId']].replace('\n', ' ')
                                ownerFound=True
                    if not ownerFound:
                        ownerName = "NA"
                        trailConfig = Config(
                            region_name=region['RegionName'],
                            signature_version='v4',
                            retries={
                                'max_attempts': 10,
                                'mode': 'standard'
                            }
                        )
                        client = boto3.client('cloudtrail',config=trailConfig)
                        response = client.lookup_events(
                            LookupAttributes=[
                                {
                                    'AttributeKey': 'ResourceName',
                                    'AttributeValue': instance['InstanceId']
                                },
                            ],
                        )
                        for events in response['Events']:
                            if(events['EventName'] == 'RunInstances'):
                                print(events['Username'] +" - "+ events['EventName'] , " - "+instance['InstanceId'])
                                ownerName= events['Username']
                        output+= "\nOwner: " +ownerName+ " - " + instance['InstanceId'] + " - " + instance['State']['Name'] + " - " + region['RegionName']# + " - "+ nonComplainceReason[instance['InstanceId']].replace('\n', ' ')
    # awsData = {'text': output}
    
    # response = requests.post(
    #     slackUrl, data=json.dumps(awsData),
    #     headers={'Content-Type': 'application/json'}
    # )
    
    
    print(output)