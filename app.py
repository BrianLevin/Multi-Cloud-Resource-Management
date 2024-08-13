from flask import Flask, jsonify
import boto3
from botocore.exceptions import ClientError
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import AzureError
from dotenv import load_dotenv
import os
import logging

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

def get_s3_buckets():
    try:
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        return [bucket['Name'] for bucket in response['Buckets']]
    except ClientError as e:
        logging.error(f"AWS S3 Error: {e}")
        return []

def get_ec2_instances():
    try:
        ec2 = boto3.client('ec2')
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

def get_azure_resource_groups():
    try:
        credential = DefaultAzureCredential()
        subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
        if not subscription_id:
            raise ValueError("AZURE_SUBSCRIPTION_ID environment variable is not set")
        resource_client = ResourceManagementClient(credential, subscription_id)
        groups = list(resource_client.resource_groups.list())
        return [group.name for group in groups]
    except AzureError as e:
        logging.error(f"Azure Error: {e}")
        return []
    except ValueError as e:
        logging.error(str(e))
        return []

@app.route('/')
def hello():
    return "Hello from Multi-Cloud DevOps Demo!"

@app.route('/aws-regions')
def aws_regions():
    try:
        ec2 = boto3.client('ec2')
        regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
        return jsonify({"AWS Regions": regions})
    except ClientError as e:
        logging.error(f"Error fetching AWS regions: {e}")
        return jsonify({"error": "Failed to fetch AWS regions"}), 500

@app.route('/aws-resources')
def aws_resources():
    return jsonify({
        'S3_Buckets': get_s3_buckets(),
        'EC2_Instances': get_ec2_instances(),
        'Regions': [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]
    })

@app.route('/multi-cloud-resources')
def multi_cloud_resources():
    try:
        aws_resources = {
            'S3_Buckets': get_s3_buckets(),
            'EC2_Instances': get_ec2_instances(),
        }
        azure_resources = {
            'Resource_Groups': get_azure_resource_groups()
        }
        return jsonify({
            'AWS': aws_resources,
            'Azure': azure_resources
        })
    except Exception as e:
        logging.error(f"Error in multi_cloud_resources: {str(e)}", exc_info=True)
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/env')
def env():
    return jsonify({
        'AZURE_TENANT_ID': os.getenv('AZURE_TENANT_ID'),
        'AZURE_CLIENT_ID': os.getenv('AZURE_CLIENT_ID'),
        'AZURE_CLIENT_SECRET': os.getenv('AZURE_CLIENT_SECRET')[:5] + '...' if os.getenv('AZURE_CLIENT_SECRET') else None,
        'AWS_DEFAULT_REGION': os.getenv('AWS_DEFAULT_REGION'),
        'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
        'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY')[:5] + '...' if os.getenv('AWS_SECRET_ACCESS_KEY') else None
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
