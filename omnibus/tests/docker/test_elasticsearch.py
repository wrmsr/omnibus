import pytest

from ...docker.dev.pytest import DockerManager
from ...inject.dev import pytest as ptinj


@pytest.mark.xfail()
def test_elasticsearch(harness: ptinj.Harness):
    [(host, port)] = harness[DockerManager].get_container_tcp_endpoints([('elasticsearch', 9200)]).values()

    from datetime import datetime
    from elasticsearch import Elasticsearch
    es = Elasticsearch([{'host': host, 'port': port}])

    doc = {
        'author': 'kimchy',
        'text': 'Elasticsearch: cool. bonsai cool.',
        'timestamp': datetime.now(),
    }
    res = es.index(index='test-index', id=1, body=doc)
    print(res['result'])

    res = es.get(index='test-index', id=1)
    print(res['_source'])

    es.indices.refresh(index='test-index')

    res = es.search(index='test-index', body={'query': {'match_all': {}}})
    print('Got %d Hits:' % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print('%(timestamp)s %(author)s: %(text)s' % hit['_source'])
