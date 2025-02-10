# ruff: noqa
import boto3
from config import settings

s3_client = boto3.client('s3', aws_access_key_id=settings.AWS, aws_secret_access_key=settings.)
