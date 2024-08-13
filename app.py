# Application code (app.py)
from flask import Flask
import boto3

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Multi-Cloud DevOps Demo!"

@app.route('/aws-regions')
def aws_regions():
    ec2 = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    return f"AWS Regions: {', '.join(regions)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)