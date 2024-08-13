import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # AWS Configuration
    AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    # Azure Configuration
    AZURE_SUBSCRIPTION_ID = os.getenv('AZURE_SUBSCRIPTION_ID')
    AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')
    AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
    AZURE_CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')

    # Application Configuration
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    @staticmethod
    def get_aws_config():
        return {
            'region_name': Config.AWS_DEFAULT_REGION,
            'aws_access_key_id': Config.AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': Config.AWS_SECRET_ACCESS_KEY
        }

    @staticmethod
    def get_azure_config():
        if not Config.AZURE_SUBSCRIPTION_ID:
            raise ValueError("AZURE_SUBSCRIPTION_ID is not set in the environment variables")
        return {
            'subscription_id': Config.AZURE_SUBSCRIPTION_ID,
            'tenant_id': Config.AZURE_TENANT_ID,
            'client_id': Config.AZURE_CLIENT_ID,
            'client_secret': Config.AZURE_CLIENT_SECRET
        }