import os.path

import boto3
import botocore.client
import pytest
import yaml

from ...docker.dev.pytest import DockerManager
from ...inject.dev import pytest as ptinj


@pytest.mark.xfail()
def test_docker_s3(harness: ptinj.Harness):
    [(host, port)] = harness[DockerManager].get_container_tcp_endpoints([('minio', 9000)]).values()

    with open(os.path.join(os.path.dirname(__file__), '../../docker/docker-compose.yml'), 'r') as f:
        dct = yaml.safe_load(f.read())
    cfg = {
        k: dct['services']['omnibus-minio']['environment']['MINIO_' + k.upper()]
        for k in ['access_key', 'secret_key']
    }

    s3 = boto3.client(
        's3',
        endpoint_url=f'http://{host}:{port}',
        aws_access_key_id=cfg['access_key'],
        aws_secret_access_key=cfg['secret_key'],
        config=botocore.client.Config(signature_version='s3v4'),
        region_name='us-east-1',
    )

    bucket = 'abucket'
    try:
        s3.head_bucket(Bucket=bucket)
    except botocore.client.ClientError:
        s3.create_bucket(Bucket=bucket)
    s3.put_object(Bucket=bucket, Key='afile', Body=b'hi')
    print(s3.get_object(Bucket=bucket, Key='afile')['Body'].read())


@pytest.mark.xfail()
def test_docker_sqs(harness: ptinj.Harness):
    [(host, port)] = harness[DockerManager].get_container_tcp_endpoints([('elasticmq', 9324)]).values()

    sqs = boto3.client(
        'sqs',
        endpoint_url=f'http://{host}:{port}',
        # aws_access_key_id=cfg['access_key'],
        # aws_secret_access_key=cfg['secret_key'],
        config=botocore.client.Config(signature_version='s3v4'),
        region_name='us-east-1',
    )

    response = sqs.create_queue(
        QueueName='SQS_QUEUE_NAME',
        Attributes={
            'DelaySeconds': '60',
            'MessageRetentionPeriod': '86400',
        },
    )

    queue_url = response['QueueUrl']

    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'The Whistler',
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'John Grisham',
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6',
            },
        },
        MessageBody=(
            'Information about current NY Times fiction bestseller for week of 12/11/2016.'
        ),
    )

    print(response['MessageId'])
