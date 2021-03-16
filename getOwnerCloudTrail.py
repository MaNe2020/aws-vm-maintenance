import boto3
from botocore.config import Config

client = boto3.client('cloudtrail')
response = client.lookup_events(
    LookupAttributes=[
        {
            'AttributeKey': 'ResourceName',
            'AttributeValue': 'i-05e97bb7e39d0a1e3'
        },
    ],
)

print (response['Events'][0]['Username'])