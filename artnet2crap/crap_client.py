import asyncio
import logging

log = logging.getLogger(__name__)


GAMMA = 1.0
BRIGHTNESS = 1.0


def prepare_message(data: bytearray, unpack: bool=False, 
                    gamma: float=GAMMA, brightness: float=BRIGHTNESS) -> bytearray:
    """
    Prepares the pixel data for transmission over UDP
    """
    # 4 bytes for future use as a crc32 checksum in network byte order.
    checksum = bytearray([0,0,0,0])
    data_as_bytes = bytearray()
    if unpack:
        for r, g, b, a in data:
            r = int(((r/255.0) ** gamma) * 255 * brightness)
            g = int(((g/255.0) ** gamma) * 255 * brightness)
            b = int(((b/255.0) ** gamma) * 255 * brightness)
            data_as_bytes += bytearray([r,g,b])
    else:
        data_as_bytes = bytearray(data)
        
    while len(data_as_bytes) < 1920:
        data_as_bytes += bytearray([0,0,0])
    
    message = data_as_bytes + checksum
    return message


class CrapClientProtocol(asyncio.DatagramProtocol):
    def __init__(self, loop):
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        log.debug('CRAP connection made')
        self.transport = transport
       
    def datagram_received(self, data, addr):
        log.debug("Received: %s" % repr(data))

    def error_received(self, exc):
        log.error('Error received: %s' % exc)

    def connection_lost(self, exc):
        log.error("CRAP UDP connection lost.")


async def crap_client_coroutine(loop, framebuffer: bytearray):
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: CrapClientProtocol(loop),
        remote_addr=('10.0.1.39', 1337)
    )
    # res = await connect()
    while loop.is_running():
        # wwlog.debug('Send:', framebuffer)
        transport.sendto(framebuffer)
        await asyncio.sleep(1.0 / 12.5)
    
    transport.close()
