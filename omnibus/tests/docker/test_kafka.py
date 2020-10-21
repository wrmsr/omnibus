"""
evaluate:
 - https://github.com/edenhill/librdkafka
 - https://www.confluent.io/blog/getting-started-with-rust-and-kafka/
 - https://github.com/Parsely/pykafka
"""
import pytest

from ...docker.dev.pytest import DockerManager
from ...inject.dev import pytest as ptinj


SCHEMA = {
    'type': 'record',
    'name': 'test_block_iteration',
    'fields': [
        {
            'name': 'nullable_str',
            'type': ['string', 'null']
        }, {
            'name': 'str_field',
            'type': 'string'
        }, {
            'name': 'int_field',
            'type': 'int'
        }
    ]
}


def make_records(num_records=2000):
    return [
        {
            'nullable_str': None if i % 3 == 0 else '%d-%d' % (i, i),
            'str_field': '%d %d %d' % (i, i, i),
            'int_field': i * 10
        }
        for i in range(num_records)
    ]


@pytest.mark.xfail()
def test_kafka(harness: ptinj.Harness):
    import logging
    from .. import logs
    logs.configure_standard_logging(logging.INFO)

    # import io
    # import fastavro
    # records = make_records()
    # buf = io.BytesIO()
    # fastavro.writer(buf, SCHEMA, records)
    # print(buf)

    [(host, port)] = harness[DockerManager].get_container_tcp_endpoints([('redis', 22214)]).values()

    import kafka

    producer = kafka.KafkaProducer(
        # security_protocol='SSL',
        bootstrap_servers=f'{host}:{port}',
    )
    for _ in range(80):
        producer.send('foobar', b'some_message_bytes')
    producer.flush()
    print('flushed')

    consumer = kafka.KafkaConsumer(
        'foobar',
        group_id='xg0',
        bootstrap_servers=f'localhost:{port}',
    )
    # consumer.assign([kafka.TopicPartition('foobar', 2)])
    for i, msg in enumerate(consumer):
        print(msg)
        if i > 10:
            break
