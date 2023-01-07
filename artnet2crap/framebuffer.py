import logging
import time

log = logging.getLogger(__name__)

# create a checker board of black and white pixels
framebuffer = bytearray(b'\x00\x00\x00' * 640)
log.info('Setting up framebuffer with %d bytes.' % len(framebuffer))

# create a timestame variable of the last received Art-Net UPD datagram
# crap_client_coroutine will only send the framebuffer to the Mate-Light 
# when the one UDP datagram was received within the last 5 seconds.
last_received = time.monotonic() - 5.0   # initialize with a time 5 s in the past
