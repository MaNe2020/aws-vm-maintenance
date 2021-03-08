import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

client = boto3.client('ec2')
for region in client.describe_regions()['Regions']:
    print("Deploying config rules in "+region['RegionName'])
    if (region['RegionName'] in ['ap-northeast-3']):
        print("Current Issue. Skipping...")
        continue
    
    botoConfig = Config(
        region_name=region['RegionName'],
        signature_version='v4',
        retries={
            'max_attempts': 10,
            'mode': 'standard'
        }
    )

    config = boto3.client('config', config=botoConfig)

    try:
        response = config.put_configuration_recorder(
            ConfigurationRecorder={
                'name': 'default',
                'roleARN': 'arn:aws:iam::785217600689:role/aws-service-role/config.amazonaws.com/AWSServiceRoleForConfig',
                'recordingGroup': {
                    'allSupported': False,
                    'includeGlobalResourceTypes': False,
                    'resourceTypes': [
                        'AWS::EC2::Instance',
                        'AWS::EC2::SecurityGroup'
                    ]
                }
            }
        )
        response = config.put_delivery_channel(
            DeliveryChannel={
                'name': 'default',
                's3BucketName': 'config-ec2-poc',
                'configSnapshotDeliveryProperties': {
                    'deliveryFrequency': 'TwentyFour_Hours'
                }
            }
        )
        response = config.put_retention_configuration(
            RetentionPeriodInDays=30
        )

        response = config.start_configuration_recorder(
            ConfigurationRecorderName='default'
        )
        response = config.put_config_rule(
            ConfigRule={
                "ConfigRuleName": "RequiredTagsForEC2Instances",
                "Description": "Checks whether the required tags are applied to EC2 instances.",
                "Scope": {
                    "ComplianceResourceTypes": [
                        "AWS::EC2::Instance"
                    ]
                },
                "Source": {
                    "Owner": "CUSTOM_LAMBDA",
                    "SourceIdentifier": "arn:aws:lambda:"+region['RegionName']+":785217600689:function:ec2ConfigEvaluator",
                    'SourceDetails': [
                        {
                            'EventSource': 'aws.config',
                            'MessageType': 'ConfigurationItemChangeNotification' ,
                        },
                    ]
                },
                "InputParameters": "{\"Owner\":\"*\",\"Team\":\"*\",\"Name\":\"*\",\"Scope\":\"*\",\"Delete\":\"Yes,No\"}"
            }
        )
        response = config.put_remediation_configurations(
            RemediationConfigurations=[
                {
                    'ConfigRuleName': 'RequiredTagsForEC2Instances',
                    'TargetType': 'SSM_DOCUMENT',
                    'TargetId': 'AWS-StopEC2Instance',
                    'TargetVersion': '1',
                    'Parameters': {
                        'InstanceId': {
                            'ResourceValue': {
                                'Value': 'RESOURCE_ID'
                            }
                        }
                    },
                    'ResourceType': 'AWS::EC2::Instance',
                    'Automatic': False,
                    'ExecutionControls': {
                        'SsmControls': {
                            'ConcurrentExecutionRatePercentage': 10,
                            'ErrorPercentage': 50
                        }
                    },
                    'MaximumAutomaticAttempts': 5,
                    'RetryAttemptSeconds': 60,
                }
            ]
        )
        response = config.start_config_rules_evaluation(
        ConfigRuleNames=[
                'RequiredTagsForEC2Instances',
            ]
        )

    except ClientError as e:
        print(e)
        exit(1)
