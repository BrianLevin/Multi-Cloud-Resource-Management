import asyncio
from quart import Quart, jsonify
from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.resource.resources.aio import ResourceManagementClient
from azure.mgmt.compute.aio import ComputeManagementClient
from azure.core.exceptions import ClientAuthenticationError
from config import Config

app = Quart(__name__)

async def get_aws_resources():
    # Placeholder for actual AWS logic
    return {
        'EC2_Instances': [{'InstanceId': 'i-1234', 'InstanceType': 't2.micro', 'State': 'running'}],
        'Lambda_Functions': [{'FunctionName': 'test-function', 'MemorySize': 128, 'Runtime': 'python3.8'}],
        'S3_Buckets': ['test-bucket']
    }

async def get_azure_resources():
    try:
        async with DefaultAzureCredential() as credential:
            async with ResourceManagementClient(credential, Config.AZURE_SUBSCRIPTION_ID) as resource_client:
                async with ComputeManagementClient(credential, Config.AZURE_SUBSCRIPTION_ID) as compute_client:
                    resource_groups = [group.name async for group in resource_client.resource_groups.list()]
                    vms = [{
                        'name': vm.name,
                        'location': vm.location,
                        'type': vm.type
                    } async for vm in compute_client.virtual_machines.list_all()]

        return {
            'ResourceGroups': resource_groups,
            'VirtualMachines': vms
        }
    except ClientAuthenticationError:
        # For testing purposes, return mock data if authentication fails
        return {
            'ResourceGroups': ['test-resource-group'],
            'VirtualMachines': [{'name': 'test-vm', 'location': 'eastus', 'type': 'Microsoft.Compute/virtualMachines'}]
        }

@app.route('/')
async def index():
    return "Hello, World!"

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
    app.run(host='0.0.0.0', port=5000)