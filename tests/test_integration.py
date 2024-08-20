import unittest
import asyncio
from unittest.mock import patch
from app import app, get_aws_resources, get_azure_resources

class TestIntegration(unittest.TestCase):
    @patch('app.get_aws_resources')
    @patch('app.get_azure_resources')
    async def test_multi_cloud_resources(self, mock_get_azure_resources, mock_get_aws_resources):
        mock_get_aws_resources.return_value = {
            'EC2_Instances': [{'InstanceId': 'i-1234', 'InstanceType': 't2.micro', 'State': 'running'}],
            'Lambda_Functions': [{'FunctionName': 'test-function', 'MemorySize': 128, 'Runtime': 'python3.8'}],
            'S3_Buckets': ['test-bucket']
        }
        mock_get_azure_resources.return_value = {
            'ResourceGroups': ['test-resource-group'],
            'VirtualMachines': [{'name': 'test-vm', 'location': 'eastus', 'type': 'Microsoft.Compute/virtualMachines'}]
        }

        test_client = app.test_client()
        response = await test_client.get('/multi-cloud-resources')

        self.assertEqual(response.status_code, 200)
        data = await response.get_json()
        
        self.assertIn('AWS', data)
        self.assertIn('Azure', data)
        self.assertEqual(len(data['AWS']['EC2_Instances']), 1)
        self.assertEqual(len(data['Azure']['ResourceGroups']), 1)

    def test_multi_cloud_resources_sync(self):
        asyncio.run(self.test_multi_cloud_resources())

if __name__ == '__main__':
    unittest.main()