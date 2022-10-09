import asyncio
from logging import getLogger

log = getLogger(__name__)


async def pixel_processing_coroutine(loop, framebuffer, packet_queue: asyncio.Queue):
    while loop.is_running():
        try:
            
        except asyncio.TimeoutError:
            log.debug('packet-queue timeout ignored')
        
