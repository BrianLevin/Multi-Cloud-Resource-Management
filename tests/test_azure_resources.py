import pytest
from unittest.mock import AsyncMock, patch
from azure.core.exceptions import ClientAuthenticationError
from app import get_azure_resources

@pytest.mark.asyncio
async def test_get_azure_resources_structure():
    with patch('azure.identity.aio.DefaultAzureCredential') as mock_credential:
        mock_credential.side_effect = ClientAuthenticationError("Test error")
        
        result = await get_azure_resources()
        
        assert 'ResourceGroups' in result
        assert 'VirtualMachines' in result
        assert isinstance(result['ResourceGroups'], list)
        assert isinstance(result['VirtualMachines'], list)
        assert len(result['ResourceGroups']) == 1
        assert result['ResourceGroups'][0] == 'test-resource-group'
        assert len(result['VirtualMachines']) == 1
        vm = result['VirtualMachines'][0]
        assert vm['name'] == 'test-vm'
        assert vm['location'] == 'eastus'
        assert vm['type'] == 'Microsoft.Compute/virtualMachines'