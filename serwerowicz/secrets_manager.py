"""
Utility module for retrieving secrets from AWS Secrets Manager.
"""
import json
import logging
import os

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def get_secret(secret_name: str, region_name: str = 'eu-north-1') -> dict:
    """
    Retrieve a secret from AWS Secrets Manager.

    Args:
        secret_name: Name or ARN of the secret
        region_name: AWS region (default: eu-north-1)

    Returns:
        dict: Secret value as a dictionary

    Raises:
        Exception: If secret cannot be retrieved
    """
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        logger.info(f"Retrieving secret: {secret_name}")
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

        # Parse the secret string (can be JSON or plain text)
        secret_string = get_secret_value_response['SecretString']

        try:
            # Try to parse as JSON first
            secret_dict = json.loads(secret_string)
            logger.info(f"Successfully retrieved secret: {secret_name}")
            return secret_dict
        except json.JSONDecodeError:
            # If not JSON, return as plain string in a dict
            logger.info(f"Secret is not JSON, returning as plain string")
            return {'value': secret_string}

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"Error retrieving secret {secret_name}: {error_code} - {error_message}")
        raise Exception(f"Failed to retrieve secret {secret_name}: {error_message}") from e
    except Exception as e:
        logger.error(f"Unexpected error retrieving secret {secret_name}: {str(e)}", exc_info=True)
        raise


def get_database_secrets(secret_name: str = None) -> dict:
    """
    Get database credentials from Secrets Manager.

    Expected secret structure:
    {
        "username": "db_user",
        "password": "db_password",
        "host": "db_host",
        "port": "3306",
        "dbname": "db_name"
    }

    Args:
        secret_name: Name of the secret (defaults to DB_SECRET_NAME env var)

    Returns:
        dict with keys: username, password, host, port, dbname
    """
    if secret_name is None:
        secret_name = os.environ.get('DB_SECRET_NAME')
        if not secret_name:
            raise ValueError("DB_SECRET_NAME environment variable must be set")

    secrets = get_secret(secret_name)

    # Map to expected keys
    return {
        'username': secrets.get('username') or secrets.get('user'),
        'password': secrets.get('password'),
        'host': secrets.get('host') or secrets.get('hostname'),
        'port': secrets.get('port', '5432'),
        'dbname': secrets.get('dbname') or secrets.get('database') or secrets.get('db_name'),
    }


def get_s3_secrets(secret_name: str = None) -> dict:
    """
    Get S3 credentials from Secrets Manager.

    Expected secret structure:
    {
        "aws_access_key_id": "access_key",
        "aws_secret_access_key": "secret_key"
    }

    Args:
        secret_name: Name of the secret (defaults to S3_SECRET_NAME env var)

    Returns:
        dict with keys: aws_access_key_id, aws_secret_access_key
    """
    if secret_name is None:
        secret_name = os.environ.get('S3_SECRET_NAME')
        if not secret_name:
            raise ValueError("S3_SECRET_NAME environment variable must be set")

    return get_secret(secret_name)
