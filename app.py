import asyncio
from flask import Flask, jsonify, send_from_directory
from aiobotocore.session import get_session
from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.resource.resources.aio import ResourceManagementClient
from azure.mgmt.compute.aio import ComputeManagementClient
from config import Config

app = Flask(__name__, static_folder='../build', static_url_path='/')

async def get_aws_resources():
    session = get_session()
    async with session.create_client('ec2', region_name=Config.AWS_DEFAULT_REGION) as ec2_client, \
               session.create_client('lambda', region_name=Config.AWS_DEFAULT_REGION) as lambda_client, \
               session.create_client('s3', region_name=Config.AWS_DEFAULT_REGION) as s3_client:
        
        ec2_response = await ec2_client.describe_instances()
        lambda_response = await lambda_client.list_functions()
        s3_response = await s3_client.list_buckets()

        ec2_instances = [
            {
                'InstanceId': instance['InstanceId'],
                'InstanceType': instance['InstanceType'],
                'State': instance['State']['Name']
            }
            for reservation in ec2_response['Reservations']
            for instance in reservation['Instances']
        ]

        lambda_functions = [
            {
                'FunctionName': function['FunctionName'],
                'MemorySize': function['MemorySize'],
                'Runtime': function['Runtime']
            }
            for function in lambda_response['Functions']
        ]

        s3_buckets = [bucket['Name'] for bucket in s3_response['Buckets']]

    return {
        'EC2_Instances': ec2_instances,
        'Lambda_Functions': lambda_functions,
        'S3_Buckets': s3_buckets
    }

async def get_azure_resources():
    async with DefaultAzureCredential() as credential:
        async with ResourceManagementClient(credential, Config.AZURE_SUBSCRIPTION_ID) as resource_client, \
                   ComputeManagementClient(credential, Config.AZURE_SUBSCRIPTION_ID) as compute_client:
            
            resource_groups = [group.name async for group in resource_client.resource_groups.list()]
            
            vms = [
                {
                    'name': vm.name,
                    'location': vm.location,
                    'type': vm.type
                }
                async for vm in compute_client.virtual_machines.list_all()
            ]

    return {
        'ResourceGroups': resource_groups,
        'VirtualMachines': vms
    }

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/multi-cloud-resources')
async def multi_cloud_resources():
    aws_resources, azure_resources = await asyncio.gather(
        get_aws_resources(),
        get_azure_resources()
    )
    return jsonify({
        'AWS': aws_resources,
        'Azure': azure_resources
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)