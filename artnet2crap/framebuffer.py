import logging
import time

log = logging.getLogger(__name__)

# create framebuffer and fill it with black pixels
framebuffer = bytearray(b'\x00\x00\x00' * 640)
log.info('Setting up framebuffer with %d bytes.' % len(framebuffer))

# create a timestame variable of the last received Art-Net UPD datagram
# crap_client_coroutine will only send the framebuffer to the Mate-Light 
# when the one UDP datagram was received within the last 5 seconds.
class LastReceived(object):
    # This needs to be wrapped inside an object because raw float variables
    # get a new reference when updated, e.g. 
    # >>> a = 1.0
    # >>> b = a
    # >>> b += 1.0
    # a = 1.0, b = 2.0
    def __init__(self, timestamp: float):
        self.timestamp = timestamp

    def get(self) -> float:
        return self.timestamp

    def set(self, value: float) -> None:
        self.timestamp = value

last_received = LastReceived(time.monotonic() - 1.0)   # initialize with a time 5 s in the past
