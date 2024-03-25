import os

import boto3

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def upload_backup(*args, **kwargs):
    """
    Upload backup of the database to s3
    """
    # Import AWS credentials from environment variables
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
    S3_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")
    S3_BACKUP_BUCKET = os.getenv("S3_BACKUP_BUCKET")

    client = boto3.client(
        "s3",
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_ACCESS_KEY,
        region_name="eu-central-1",
    )

    backup_file = kwargs["backup_file"]
    object_name = os.path.basename(backup_file)
    client.upload_file(backup_file, S3_BACKUP_BUCKET, object_name)

    return True
