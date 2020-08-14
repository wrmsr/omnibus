import os.path

import boto3
import botocore.client
import pytest
import yaml

from .. import docker


@pytest.mark.xfail()
def test_docker_s3():
    if docker.is_in_docker():
        (host, port) = 'omnibus-minio', 9000

    else:
        with docker.client_context() as client:
            eps = docker.get_container_tcp_endpoints(
                client,
                [('docker_omnibus-minio_1', 9000)])

        [(host, port)] = eps.values()

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
