import asyncio


async def pixel_processing_coroutine(loop, framebuffer):
    new_vals = [
        bytearray(b'\x00\x00\x00\xFF\xFF\xFF' * 320),
        bytearray(b'\xFF\xFF\xFF\x00\x00\x00' * 320),

        bytearray(b'\x00\x00\x00\xFF\x00\x00' * 320),
        bytearray(b'\xFF\x00\x00\x00\x00\x00' * 320),
        bytearray(b'\x00\x00\x00\x00\xFF\x00' * 320),
        bytearray(b'\x00\xFF\x00\x00\x00\x00' * 320),
        bytearray(b'\x00\x00\x00\x00\x00\xFF' * 320),
        bytearray(b'\x00\x00\xFF\x00\x00\x00' * 320)
    ]
    selected = 0
    await asyncio.sleep(1.0)
    while loop.is_running():
        # This is the only way to overwrite
        for index, value in enumerate(framebuffer):
            framebuffer[index] = new_vals[selected][index]
        # Toggle through the available values
        selected = (selected + 1) % len(new_vals)
        await asyncio.sleep(1.0)

