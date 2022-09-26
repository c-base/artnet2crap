import logging

log = logging.getLogger(__name__)

# create a checker board of black and white pixels
framebuffer = bytearray(b'\x00\x00\x00' * 640)
log.info('Setting up framebuffer with %d bytes.' % len(framebuffer))
