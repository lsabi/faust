"""Producer.

The Producer is responsible for:

   - Holds reference to the transport that created it
   - ... and the app via ``self.transport.app``.
   - Sending messages.
"""
import asyncio
from typing import Any, Awaitable, Optional
from mode import Service
from faust.types.tuples import RecordMetadata, TP
from faust.types.transports import ProducerT, TransportT

__all__ = ['Producer']


class Producer(Service, ProducerT):
    """Base Producer."""

    def __init__(self, transport: TransportT,
                 loop: asyncio.AbstractEventLoop = None,
                 **kwargs: Any) -> None:
        self.transport = transport
        conf = self.transport.app.conf
        self.linger_ms = conf.producer_linger_ms
        self.max_batch_size = conf.producer_max_batch_size
        self.acks = conf.producer_acks
        self.max_request_size = conf.producer_max_request_size
        super().__init__(loop=loop or self.transport.loop, **kwargs)

    async def send(self, topic: str, key: Optional[bytes],
                   value: Optional[bytes],
                   partition: Optional[int]) -> Awaitable[RecordMetadata]:
        raise NotImplementedError()

    async def send_and_wait(self, topic: str, key: Optional[bytes],
                            value: Optional[bytes],
                            partition: Optional[int]) -> RecordMetadata:
        raise NotImplementedError()

    def key_partition(self, topic: str, key: bytes) -> TP:
        raise NotImplementedError()