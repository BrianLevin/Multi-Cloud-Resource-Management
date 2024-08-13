from flask import Flask, jsonify
import boto3
from botocore.exceptions import ClientError
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import AzureError
import logging
import traceback
from config import Config

app = Flask(__name__)
logging.basicConfig(level=Config.LOG_LEVEL)

# Existing AWS functions

def get_s3_buckets():
    try:
        s3 = boto3.client('s3', **Config.get_aws_config())
        response = s3.list_buckets()
        return [bucket['Name'] for bucket in response['Buckets']]
    except ClientError as e:
        logging.error(f"AWS S3 Error: {e}")
        return []

def get_ec2_instances():
    try:
        ec2 = boto3.client('ec2', **Config.get_aws_config())
        response = ec2.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    'InstanceId': instance['InstanceId'],
                    'InstanceType': instance['InstanceType'],
                    'State': instance['State']['Name']
                })
        return instances
    except ClientError as e:
        logging.error(f"AWS EC2 Error: {e}")
        return []

# New AWS Lambda function

def get_lambda_functions():
    try:
        lambda_client = boto3.client('lambda', **Config.get_aws_config())
        response = lambda_client.list_functions()
        return [{
            'FunctionName': function['FunctionName'],
            'Runtime': function['Runtime'],
            'MemorySize': function['MemorySize']
        } for function in response['Functions']]
    except ClientError as e:
        logging.error(f"AWS Lambda Error: {e}")
        return []

# Existing Azure function

def get_azure_resource_groups():
    try:
        azure_config = Config.get_azure_config()
        credential = DefaultAzureCredential()
        resource_client = ResourceManagementClient(credential, azure_config['subscription_id'])
        groups = list(resource_client.resource_groups.list())
        return [group.name for group in groups]
    except AzureError as e:
        logging.error(f"Azure Error: {e}")
        return []

# New Azure VM function

def get_azure_vms():
    try:
        azure_config = Config.get_azure_config()
        credential = DefaultAzureCredential()
        compute_client = ComputeManagementClient(credential, azure_config['subscription_id'])
        vms = list(compute_client.virtual_machines.list_all())
        return [{
            'name': vm.name,
            'location': vm.location,
            'vm_size': vm.hardware_profile.vm_size
        } for vm in vms]
    except AzureError as e:
        logging.error(f"Azure VM Error: {e}")
        return []

@app.route('/')
def hello():
    return "Hello from Multi-Cloud DevOps Demo!"

@app.route('/aws-regions')
def aws_regions():
    try:
        ec2 = boto3.client('ec2', **Config.get_aws_config())
        regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
        return jsonify({"AWS Regions": regions})
    except ClientError as e:
        logging.error(f"Error fetching AWS regions: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/aws-resources')
def aws_resources():
    return jsonify({
        'S3_Buckets': get_s3_buckets(),
        'EC2_Instances': get_ec2_instances(),
        'Lambda_Functions': get_lambda_functions(),
        'Regions': [region['RegionName'] for region in boto3.client('ec2', **Config.get_aws_config()).describe_regions()['Regions']]
    })

@app.route('/azure-resources')
def azure_resources():
    return jsonify({
        'Resource_Groups': get_azure_resource_groups(),
        'Virtual_Machines': get_azure_vms()
    })

@app.route('/multi-cloud-resources')
def multi_cloud_resources():
    try:
        aws_resources = {
            'S3_Buckets': get_s3_buckets(),
            'EC2_Instances': get_ec2_instances(),
            'Lambda_Functions': get_lambda_functions()
        }
        azure_resources = {
            'Resource_Groups': get_azure_resource_groups(),
            'Virtual_Machines': get_azure_vms()
        }
        return jsonify({
            'AWS': aws_resources,
            'Azure': azure_resources
        })
    except Exception as e:
        logging.error(f"Error in multi_cloud_resources: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/env')
def env():
    return jsonify({
        'AZURE_TENANT_ID': Config.AZURE_TENANT_ID,
        'AZURE_CLIENT_ID': Config.AZURE_CLIENT_ID,
        'AZURE_CLIENT_SECRET': Config.AZURE_CLIENT_SECRET[:5] + '...' if Config.AZURE_CLIENT_SECRET else None,
        'AWS_DEFAULT_REGION': Config.AWS_DEFAULT_REGION,
        'AWS_ACCESS_KEY_ID': Config.AWS_ACCESS_KEY_ID,
        'AWS_SECRET_ACCESS_KEY': Config.AWS_SECRET_ACCESS_KEY[:5] + '...' if Config.AWS_SECRET_ACCESS_KEY else None
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)
