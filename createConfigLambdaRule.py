import zipfile
import boto3
from botocore.config import Config
import os

os.system("zip function.zip lambdaConfigRule.py")

# archive = zipfile.ZipFile('function.zip', 'w')
# archive.write('lambdaConfigRule.py', 'lambdaConfigRule.py')

client = boto3.resource('s3')
client.Bucket('aws-vm-maintainance-lambda').upload_file('function.zip','function.zip')

client = boto3.client('ec2')
for region in client.describe_regions()['Regions']:
    lambdaConfig = Config(
            region_name = region['RegionName'],
            signature_version = 'v4',
            retries = {
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
    lambda_Client = boto3.client('lambda',config=lambdaConfig)
    response = lambda_Client.create_function(
                Code={'ZipFile': open('./function.zip', 'rb').read()},
                Description='Config rule evaluator for EC2 Tags',
                FunctionName='ec2ConfigEvaluator',
                Handler='lambdaConfigRule.lambda_handler',
                Publish=True,
                Role='arn:aws:iam::785217600689:role/service-role/LambdaConfigRole',
                Runtime='python3.6',
            )

    # response = lambda_Client.update_function_code(
    #     FunctionName='ec2ConfigEvaluator',
    #     S3Bucket='aws-vm-maintainance-lambda',
    #     S3Key='function.zip',
    # )

    print(response)