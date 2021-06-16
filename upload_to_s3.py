import logging
import os
import boto3
from botocore.exceptions import ClientError
import settings

# for security purpose can use environmental variables
#SECRET_KEY = os.environ.get('SECRET_KEY')
#ACCESS_KEY = os.environ.get('ACCESS_KEY')

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    if settings.ACCESS_KEY == "" or settings.SECRET_KEY == "":
        logging.error("Please set SECRET_KEY and ACCESS_KEY in settings.py")
        exit(1)
    
    # Upload the file
    s3_client = boto3.client('s3', aws_access_key_id =settings.ACCESS_KEY,
    aws_secret_access_key=settings.SECRET_KEY)

    try:
        s3_client.upload_file(file_name, bucket, object_name)

    except ClientError as err:
        logging.error(err)
        return False
    return True
