import asyncio
import logging
import traceback
from flask import Flask, jsonify
from aiobotocore.session import get_session
from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.resource.resources.aio import ResourceManagementClient
from azure.mgmt.compute.aio import ComputeManagementClient
from azure.core.exceptions import AzureError
from config import Config
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
logging.basicConfig(level=logging.DEBUG)

# AWS functions (unchanged)

async def get_s3_buckets():
    try:
        session = get_session()
        async with session.create_client('s3', **Config.get_aws_config()) as client:
            response = await client.list_buckets()
            return [bucket['Name'] for bucket in response['Buckets']]
    except Exception as e:
        logging.error(f"AWS S3 Error: {e}")
        logging.error(traceback.format_exc())
        return []

async def get_ec2_instances():
    try:
        session = get_session()
        async with session.create_client('ec2', **Config.get_aws_config()) as client:
            response = await client.describe_instances()
            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append({
                        'InstanceId': instance['InstanceId'],
                        'InstanceType': instance['InstanceType'],
                        'State': instance['State']['Name']
                    })
            return instances
    except Exception as e:
        logging.error(f"AWS EC2 Error: {e}")
        logging.error(traceback.format_exc())
        return []

async def get_lambda_functions():
    try:
        session = get_session()
        async with session.create_client('lambda', **Config.get_aws_config()) as client:
            response = await client.list_functions()
            return [{
                'FunctionName': function['FunctionName'],
                'Runtime': function['Runtime'],
                'MemorySize': function['MemorySize']
            } for function in response['Functions']]
    except Exception as e:
        logging.error(f"AWS Lambda Error: {e}")
        logging.error(traceback.format_exc())
        return []

# Azure functions

async def get_azure_resource_groups():
    try:
        azure_config = Config.get_azure_config()
        async with DefaultAzureCredential() as credential:
            async with ResourceManagementClient(credential, azure_config['subscription_id']) as client:
                groups = [group.name async for group in client.resource_groups.list()]
                return groups
    except AzureError as e:
        logging.error(f"Azure Resource Groups Error: {e}")
        logging.error(traceback.format_exc())
        return []

async def get_azure_vms():
    try:
        azure_config = Config.get_azure_config()
        async with DefaultAzureCredential() as credential:
            async with ComputeManagementClient(credential, azure_config['subscription_id']) as compute_client:
                vms = [
                    {
                        'name': vm.name,
                        'location': vm.location,
                        'vm_size': vm.hardware_profile.vm_size
                    } 
                    async for vm in compute_client.virtual_machines.list_all()
                ]
                return vms
    except AzureError as e:
        logging.error(f"Azure VM Error: {e}")
        logging.error(traceback.format_exc())
        return []

# Routes

@app.route('/')
def hello():
    return "Hello from Async Multi-Cloud DevOps Demo!"

@app.route('/aws-regions')
async def aws_regions():
    try:
        session = get_session()
        async with session.create_client('ec2', **Config.get_aws_config()) as client:
            response = await client.describe_regions()
            regions = [region['RegionName'] for region in response['Regions']]
            return jsonify({"AWS Regions": regions})
    except Exception as e:
        logging.error(f"Error fetching AWS regions: {e}")
        logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/aws-resources')
async def aws_resources():
    try:
        s3_buckets, ec2_instances, lambda_functions = await asyncio.gather(
            get_s3_buckets(),
            get_ec2_instances(),
            get_lambda_functions()
        )
        return jsonify({
            'S3_Buckets': s3_buckets,
            'EC2_Instances': ec2_instances,
            'Lambda_Functions': lambda_functions
        })
    except Exception as e:
        logging.error(f"Error in aws_resources: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/azure-resources')
async def azure_resources():
    try:
        resource_groups, vms = await asyncio.gather(
            get_azure_resource_groups(),
            get_azure_vms()
        )
        return jsonify({
            'Resource_Groups': resource_groups,
            'Virtual_Machines': vms
        })
    except Exception as e:
        logging.error(f"Error in azure_resources: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/multi-cloud-resources')
async def multi_cloud_resources():
    try:
        aws_s3, aws_ec2, aws_lambda, azure_groups, azure_vms = await asyncio.gather(
            get_s3_buckets(),
            get_ec2_instances(),
            get_lambda_functions(),
            get_azure_resource_groups(),
            get_azure_vms()
        )
        
        return jsonify({
            'AWS': {
                'S3_Buckets': aws_s3,
                'EC2_Instances': aws_ec2,
                'Lambda_Functions': aws_lambda
            },
            'Azure': {
                'Resource_Groups': azure_groups,
                'Virtual_Machines': azure_vms
            }
        })
    except Exception as e:
        logging.error(f"Error in multi_cloud_resources: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)
