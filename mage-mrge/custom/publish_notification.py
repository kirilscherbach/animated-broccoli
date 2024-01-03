import os

import boto3

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def publish_sns(email_body, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Import AWS credentials from environment variables
    SNS_ACCESS_KEY_ID = os.getenv("SNS_ACCESS_KEY_ID")
    SNS_SECRET_ACCESS_KEY = os.getenv("SNS_SECRET_ACCESS_KEY")
    SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

    sns = boto3.client(
        "sns",
        aws_access_key_id=SNS_ACCESS_KEY_ID,
        aws_secret_access_key=SNS_SECRET_ACCESS_KEY,
        region_name="eu-central-1",
    )

    response = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=email_body,
        Subject=f"Daily Job Digest for {kwargs['execution_date'].strftime('%Y-%m-%d')}",
    )

    return True
