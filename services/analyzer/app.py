from faststream import FastStream

from shared.kafka import broker

if True:
    from . import handlers

app = FastStream(broker)
