from flask import Flask, jsonify
import boto3
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from dotenv import load_dotenv
import os
import logging

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Existing AWS functions
def get_s3_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    return [bucket['Name'] for bucket in response['Buckets']]

def get_ec2_instances():
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

# New Azure function
def get_azure_resource_groups():
    try:
        logging.debug("Initializing DefaultAzureCredential")
        credential = DefaultAzureCredential()
        subscription_id = "7cb6c26c-7f4c-4bca-a7b8-24edc30707be"  # Your subscription ID
        logging.debug(f"Using subscription ID: {subscription_id}")
        logging.debug("Initializing ResourceManagementClient")
        resource_client = ResourceManagementClient(credential, subscription_id)
        logging.debug("Listing resource groups")
        groups = list(resource_client.resource_groups.list())
        logging.debug(f"Found {len(groups)} resource groups")
        return [group.name for group in groups]
    except Exception as e:
        logging.error(f"Error in get_azure_resource_groups: {str(e)}", exc_info=True)
        raise

@app.route('/')
def hello():
    return "Hello from Multi-Cloud DevOps Demo!"


@app.route('/test-azure')
def test_azure():
    try:
        credential = DefaultAzureCredential()
        subscription_id = "7cb6c26c-7f4c-4bca-a7b8-24edc30707be"  # Your subscription ID
        resource_client = ResourceManagementClient(credential, subscription_id)
        groups = list(resource_client.resource_groups.list())
        return jsonify({
            'Azure': {
                'Resource_Groups': [group.name for group in groups],
                'Subscription_ID': subscription_id
            }
        })
    except Exception as e:
        logging.error(f"Error in test_azure: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500



@app.route('/aws-regions')
def aws_regions():
    ec2 = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    return f"AWS Regions: {', '.join(regions)}"

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
        logging.debug("Fetching AWS resources")
        aws_resources = {
            'S3_Buckets': get_s3_buckets(),
            'EC2_Instances': get_ec2_instances(),
        }
        logging.debug("Fetching Azure resources")
        azure_resources = {
            'Resource_Groups': get_azure_resource_groups()
        }
        logging.debug("Returning multi-cloud resources")
        return jsonify({
            'AWS': aws_resources,
            'Azure': azure_resources
        })
    except Exception as e:
        logging.error(f"Error in multi_cloud_resources: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/env')
def env():
    return jsonify({
        'AZURE_TENANT_ID': os.getenv('AZURE_TENANT_ID'),
        'AZURE_CLIENT_ID': os.getenv('AZURE_CLIENT_ID'),
        'AZURE_CLIENT_SECRET': os.getenv('AZURE_CLIENT_SECRET')[:5] + '...',
        'AWS_DEFAULT_REGION': os.getenv('AWS_DEFAULT_REGION'),
        'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
        'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY')[:5] + '...'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)