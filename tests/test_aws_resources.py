import pytest
from app import get_aws_resources

@pytest.mark.asyncio
async def test_get_aws_resources_structure():
    result = await get_aws_resources()
    
    assert 'EC2_Instances' in result
    assert 'Lambda_Functions' in result
    assert 'S3_Buckets' in result
    
    assert isinstance(result['EC2_Instances'], list)
    assert isinstance(result['Lambda_Functions'], list)
    assert isinstance(result['S3_Buckets'], list)
    
    if result['EC2_Instances']:
        instance = result['EC2_Instances'][0]
        assert 'InstanceId' in instance
        assert 'InstanceType' in instance
        assert 'State' in instance
    
    if result['Lambda_Functions']:
        function = result['Lambda_Functions'][0]
        assert 'FunctionName' in function
        assert 'MemorySize' in function
        assert 'Runtime' in function
    
    if result['S3_Buckets']:
        assert isinstance(result['S3_Buckets'][0], str)