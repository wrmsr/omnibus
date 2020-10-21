import boto3.dynamodb.conditions
import pytest

from ...docker.dev.pytest import DockerManager
from ...inject.dev import pytest as ptinj


@pytest.mark.xfail()
def test_docker_dynamo(harness: ptinj.Harness):
    [(host, port)] = harness[DockerManager].get_container_tcp_endpoints([('dynamodb', 8000)]).values()

    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=f'http://{host}:{port}',
        region_name='us-east-1',
        aws_access_key_id='00000000000000000000',
        aws_secret_access_key='0000000000000000000000000000000000000000',
    )

    try:
        dynamodb.Table('Movies').delete()
    except Exception:
        pass

    table = dynamodb.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH',  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE',  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N',
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S',
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10,
        }
    )

    movies = [
        {
            'year': 2013,
            'title': 'Turn It Down, Or Else!',
            'info': {
                'directors': [
                    'Alice Smith',
                    'Bob Jones',
                ],
                'release_date': '2013-01-18T00:00:00Z',
                'genres': [
                    'Comedy',
                    'Drama',
                ],
                'plot': 'A rock band plays their music at high volumes, annoying the neighbors.',
                'rank': 11,
                'running_time_secs': 5215,
                'actors': [
                    'David Matthewman',
                    'Ann Thomas',
                    'Jonathan G. Neff',
                ],
            }
        }
    ]

    for movie in movies:
        year = int(movie['year'])
        title = movie['title']
        print('Adding movie:', year, title)
        table.put_item(Item=movie)

    table = dynamodb.Table('Movies')
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('year').eq(2013)
    )
    print(response['Items'])
