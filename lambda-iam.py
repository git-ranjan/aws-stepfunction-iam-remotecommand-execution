import boto3
from botocore.exceptions import ClientError
import json

def lambda_handler(event, context):
    instance_id = event['instance_id']
    region_name = event.get('region_name', 'us-east-1')
    command = event.get('command', 'uptime')
    
    ssm_client = boto3.client('ssm', region_name=region_name)
    
    try:
        response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': [command]}
        )
        
        command_id = response['Command']['CommandId']
        
        # Wait for command to complete and get output
        output = ssm_client.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )
        
        return {
            'statusCode': 200,
            'output': output['StandardOutputContent'],
            'errors': output['StandardErrorContent']
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'error': str(e)
        }