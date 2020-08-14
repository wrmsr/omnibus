import pymongo
import pytest

from .. import docker


@pytest.mark.xfail()
def test_docker_mongo():
    if docker.is_in_docker():
        (host, port) = 'omnibus-mongo', 27017

    else:
        with docker.client_context() as client:
            eps = docker.get_container_tcp_endpoints(
                client,
                [('docker_omnibus-mongo_1', 27017)])

        [(host, port)] = eps.values()

    client = pymongo.MongoClient(f'mongodb://root:omnibus@{host}:{port}')
    db = client['test-database']

    post = {
        'author': 'Mike',
        'text': 'My first blog post!',
        'tags': ['mongodb', 'python', 'pymongo'],
    }

    posts = db['posts']
    post_id = posts.insert_one(post).inserted_id
    print(post_id)
    db.list_collection_names()
    print(posts.find_one())
