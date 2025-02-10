# ruff: noqa
import sys
import os

sys.path.append(os.getcwd())
import boto3
from config import settings
from core.boto3_client import s3_client
