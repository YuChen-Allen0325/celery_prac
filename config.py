import os
from dotenv import load_dotenv

load_dotenv()


class AwsS3Config(object):
    AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
    AWS_S3_REGION_NAME = os.environ["AWS_S3_REGION_NAME"]
    DEFAULT_FILE_STORAGE = os.environ["DEFAULT_FILE_STORAGE"]
