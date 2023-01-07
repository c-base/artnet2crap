# -*- coding: utf-8 -*-
import asyncio
import logging

log = logging.getLogger(__name__)


class ArtNetPollReceived(Exception):
    pass


class ArtNetDecodeError(Exception):
    pass


class ArtNetLengthMismatchError(ArtNetDecodeError):
    pass


class ArtNetPacket(object):
    def __init__(self, universe, length, dmx, sequence=0x00, opcode=0x5000, version=14, physical=0x00):
        self.sequence = sequence
        self.physical = physical
        self.universe = universe
        self.length = length
        self.dmx = dmx
        self.opcode = opcode
        self.version = version


def decode_artnet_packet(data:bytearray) -> ArtNetPacket:
    # A DMX packet contains 512 bytes of DMX data every time.
    header = data[:8]
    # id
    artnet_magic = bytearray(b'Art-Net')
    artnet_magic.append(0x0)
    if data[:8] != artnet_magic:
        raise ArtNetDecodeError()

    # OP-Code low byte first
    opcode = (data[8] & 0x00FF) | ((data[9] << 8) & 0xFF00)

    if opcode == 0x2000:
        raise ArtNetPollReceived()

    # proto ver high byte first
    version = ((data[10] << 8) & 0xFF00) | (data[11] & 0x00FF)

    # sequence number (0x00 means disable)
    sequence = data[12]

    # physical port
    physical = data[13]

    # universe, low byte first
    try:
        universe = (data[14] & 0x00FF) | ((data[15] << 8) & 0xFF00)
    except:
        log.info("got udp %s" % repr(data))

    # length, high byte first
    length = ((data[16] << 8) & 0xFF00) | (data[17] & 0x00FF)

    raw_dmx = data[18:]
    if len(raw_dmx) != length:
        raise ArtNetLengthMismatchError()


    #header.append(512 & 0xFF)

    packet = ArtNetPacket(
        sequence=sequence,
        physical=physical,
        universe=universe,
        length=length,
        dmx=raw_dmx,
        opcode=opcode,
        version=version
    )
    return packet


class ArtNetServerProtocol(asyncio.Protocol):

    def __init__(self, frame_buffer, last_received):
        log.info('Art-Net server protocol __init__() ...')
        self.frame_buffer = frame_buffer
        self.last_received = last_received
        super().__init__()

    def connection_made(self, transport):
        log.debug("Art-Net connection made")
        self.transport = transport

    async def process_packet(self, artnet_packet):
        new_vals = artnet_packet.dmx
        start_index = 480 * artnet_packet.universe
        log.debug('start-index: %d, dmx: %s' % (start_index, len(new_vals)))
        for index, value in enumerate(new_vals):
            if index >= 480:
                break
            self.frame_buffer[start_index + index] = value
        return

    def datagram_received(self, data, addr):
        # A datagram has been received, set the the last_received timestamp to now.
        self.last_received = asyncio.get_event_loop().time()
        try:
            artnet_packet = decode_artnet_packet(data)
            log.debug('Art-Net DMX received: lenght: %d, universe: %s, opcode: %x' % (artnet_packet.length, artnet_packet.universe, artnet_packet.opcode))
            asyncio.ensure_future(self.process_packet(artnet_packet))
        except ArtNetPollReceived:
            log.debug("Art-Net poll (opcode 0x2000) received.")
            return
        except asyncio.queues.QueueFull:
            log.debug('Queue full')
            return

        dmx = artnet_packet.dmx

        # TODO: Blit DMX data into framebuffer
        # channel_state.update_dmx(dmx)
