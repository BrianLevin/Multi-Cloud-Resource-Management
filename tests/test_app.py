import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

@pytest.mark.asyncio
async def test_serve_react_app(client):
    response = await client.get('/')
    assert response.status_code == 200
    assert await response.get_data(as_text=True) == "Hello, World!"

@pytest.mark.asyncio
async def test_multi_cloud_resources(client, mocker):
    mock_aws = mocker.patch('app.get_aws_resources')
    mock_azure = mocker.patch('app.get_azure_resources')
    
    mock_aws.return_value = {'EC2_Instances': [], 'Lambda_Functions': [], 'S3_Buckets': []}
    mock_azure.return_value = {'ResourceGroups': [], 'VirtualMachines': []}

    response = await client.get('/multi-cloud-resources')
    assert response.status_code == 200
    data = await response.get_json()
    assert 'AWS' in data
    assert 'Azure' in data