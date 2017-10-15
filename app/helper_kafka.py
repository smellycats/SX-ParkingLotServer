import time

from . import my_logger
from confluent_kafka import Producer, KafkaError, KafkaException, libversion


logger = my_logger.logging.getLogger('root')

def error_cb(err):
    #print('error_cb', err)
    logger.error(err)


class KafkaData(object):
    def __init__(self, **kwargs):
        try:
            p = Producer()
        except TypeError as e:
            assert str(e) == "expected configuration dict"
        self.p = Producer({'bootstrap.servers': '{0}'.format(kwargs['services']),
                           'socket.timeout.ms': 1000, 'error_cb': error_cb,
                           'retries': 3, 'retry.backoff.ms': 2000, 'batch.num.messages': 400,
                           'default.topic.config': {'message.timeout.ms': 1000, 'acks': 'all'}})
        self.topic = kwargs['topic']
        self.lost_msg = {}

    def produce_info(self, key='', value='', cb=None):
        self.p.produce(self.topic, value, key, callback=cb)

    def flush(self):
        self.p.poll(0.1)
        self.p.flush()
