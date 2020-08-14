import pytest

from .. import docker


@pytest.mark.xfail()
def test_elasticsearch():
    if docker.is_in_docker():
        (host, port) = 'omnibus-elasticsearch', 9200

    else:
        with docker.client_context() as client:
            eps = docker.get_container_tcp_endpoints(
                client,
                [('docker_omnibus-elasticsearch_1', 9200)])

        [(host, port)] = eps.values()

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
