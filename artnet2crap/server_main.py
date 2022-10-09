import asyncio
import logging
import sys

from artnet2crap.artnet_server import ArtNetServerProtocol
from artnet2crap.crap_client import crap_client_coroutine
from artnet2crap.framebuffer import framebuffer
# from artnet2crap.pixel_processing import pixel_processing_coroutine


# fmt = "{time} - {name} - {level} - {message}"
# logger.add("spam.log", level="DEBUG")   #, format=fmt)
# logger.add(sys.stderr, level="DEBUG")   #, format=fmt)

log = logging.getLogger()
log.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

packet_queue = asyncio.Queue()

async def create_art_net_coro(frame_buffer):
    loop = asyncio.get_event_loop()
    protocol = ArtNetServerProtocol(frame_buffer=frame_buffer)
    coro = await loop.create_datagram_endpoint(
        lambda: protocol,
        local_addr=(
            '0.0.0.0',   # Bind to IP
            6454   # Port number (default for Art-Net is 6454)
        )
    )
    return coro


def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_event_loop()
    coro = create_art_net_coro(frame_buffer=framebuffer)
    transport, _ = loop.run_until_complete(coro)
    asyncio.ensure_future(crap_client_coroutine(loop, framebuffer))
    # asyncio.ensure_future(pixel_processing_coroutine(loop, framebuffer, packet_queue))
    loop.run_forever()


if __name__ == '__main__':
    main()