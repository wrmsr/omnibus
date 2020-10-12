import pymongo
import pytest

from ..docker.dev.pytest import DockerManager
from ..inject.dev import pytest as ptinj


@pytest.mark.xfail()
def test_docker_mongo(harness: ptinj.Harness):
    [(host, port)] = harness[DockerManager].get_container_tcp_endpoints([('mongo', 9200)]).values()

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
