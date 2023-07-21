import json
import os
import urllib.parse

import boto3

s3 = boto3.client('s3')
sqs = boto3.client('sqs')


def lambda1(event, context):
    try:
        body = event.get('body')
        print(f"Received message: {body}")
        if not body:
            raise ValueError("Error: No body in the event")
        sqs.send_message(
            QueueUrl=os.environ['SQS_QUEUE_URL'], MessageBody=body)
        return {
            'statusCode': 200,
            'body': json.dumps('Message sent to SQS queue!')
        }
    except Exception as e:
        print(f"Error in lambda1: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error in lambda1: {str(e)}")
        }


def lambda2(event, context):
    try:
        for record in event.get('Records', []):
            body = record.get('body')
            if not body:
                raise ValueError("Error: No body in the record")
            bucket_name = os.environ['BUCKET_NAME']
            s3.put_object(
                Bucket=bucket_name, Key=body, Body=body)
            print(
                f"Message put into S3 bucket: {bucket_name}, object key: {body}")
        return {
            'statusCode': 200,
            'body': json.dumps('Message put into S3 bucket!')
        }
    except Exception as e:
        print(f"Error in lambda2: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error in lambda2: {str(e)}")
        }


def lambda3(event, context):
    try:
        for record in event.get('Records', []):
            bucket = record['s3']['bucket']['name']
            key = urllib.parse.unquote(record['s3']['object']['key'])
            print(
                f'New object has been created in bucket {bucket} with key {key}')
        return {
            'statusCode': 200,
            'body': json.dumps('S3 event logged!')
        }
    except Exception as e:
        print(f"Error in lambda3: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error in lambda3: {str(e)}")
        }
