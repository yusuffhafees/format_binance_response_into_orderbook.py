import boto3
import json
from app.tools.encoding_helper import file2str
lambda_client = boto3.client('lambda')

def send_email(filename, file, address, subject):
    event = {
        "subject": subject,
        "recipients": [{"name": "Hafees", "address": address}],
        "body": {"content": "my Content", "type": "plain"},
        "attachments": [{"file_name": filename, "file": file}]
    }

    response = lambda_client.invoke(
      FunctionName='SESController',
      Payload=json.dumps(event))
    return response