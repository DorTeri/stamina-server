import boto3
from botocore.exceptions import ClientError
import logging
import json

def get_secret():

    secret_name = "prod/firebaseAdmin"
    region_name = "eu-central-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    secret = secret.replace('\r', '').replace('\n', '').replace('\t', '')
    json_data = json.loads(secret)
    firebase_admin_sdk_credentials = json_data['FIREBASE_ADMIN_SDK_CREDENTIALS']
    return firebase_admin_sdk_credentials