import boto3
import json


client = boto3.client("lambda")


def bytewrite_to_s3(bucket_name: str,
                    file_path: str,
                    content: str,
                    action: str = "bytewrite"):
    response = client.invoke(
        FunctionName="arn:aws:lambda:eu-central-1:363589960244:function:S3Controller",
        InvocationType="RequestResponse",
        Payload=json.dumps({
            "bucket_name": bucket_name,
            "file_name": file_path,
            "content": content,
            "action": action
        })
    )
    print(json.load(response["Payload"]))