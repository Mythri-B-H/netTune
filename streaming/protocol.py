import struct

HEADER_SIZE = 4

def pack_chunk(data):
    size = len(data)
    header = struct.pack("!I", size)
    return header + data

def unpack_header(header_bytes):
    return struct.unpack("!I", header_bytes)[0]

