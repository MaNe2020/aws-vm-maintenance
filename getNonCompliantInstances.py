import boto3
from botocore.config import Config

client = boto3.client('ec2')
print("------- Get Non Complaint Ec2 Instances ---------------")
for region in client.describe_regions()['Regions']:
    print("\nChecking in "+region['RegionName'])
    instanceIdList=[]
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
        ConfigRuleName='TestRequiredTagsForEC2Instances',
        ComplianceTypes=['NON_COMPLIANT'],
    )

    for results in response['EvaluationResults']:
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
                for tag in instance['Tags']:
                    if (tag['Key'] == "Owner"):
                        print("Owner: "+tag['Value'] + " - " + instance['InstanceId'] + " - " + instance['State']['Name'] + " - " + region['RegionName'])
                        continue
                    print("Owner: NA" + " - " + instance['InstanceId'] + " - " + instance['State']['Name'] + " - " + region['RegionName'])