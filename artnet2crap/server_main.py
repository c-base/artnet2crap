import asyncio
import logging
import sys

from artnet2crap.artnet_server import ArtNetServerProtocol
from artnet2crap.crap_client import crap_client_coroutine
from artnet2crap.framebuffer import framebuffer
from artnet2crap.pixel_processing import pixel_processing_coroutine


# fmt = "{time} - {name} - {level} - {message}"
# logger.add("spam.log", level="DEBUG")   #, format=fmt)
# logger.add(sys.stderr, level="DEBUG")   #, format=fmt)

log = logging.getLogger()
log.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: ArtNetServerProtocol(),
        '0.0.0.0',   # Bind to IP
        6454   # Port number (default for Art-Net is 6454)
    )

    log.info('Starting server...')
    async with server:
        asyncio.ensure_future(crap_client_coroutine(loop, framebuffer))
        asyncio.ensure_future(pixel_processing_coroutine(loop, framebuffer))
        await server.serve_forever()


asyncio.run(main())