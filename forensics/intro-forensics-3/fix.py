#!/usr/bin/env python3
"""
reorder_png_chunks.py

Read a PNG file whose chunk CRC fields have been repurposed to store
an 4-byte sequential order value (starting at 0). Validate that each
chunk type is one of: IHDR, bKGD, cHRM, IDAT, IEND. Then reorder the
chunks according to that stored order integer, recalculate proper
CRC-32 for each chunk, and write a valid PNG.

Usage:
    python reorder_png_chunks.py input.png output.png
"""

import struct
import sys
import zlib

# Allowed chunk types
ALLOWED_TYPES = {"IHDR", "bKGD", "cHRM", "IDAT", "IEND"}


class PNGChunk:
    def __init__(self, length, ctype, data, order):
        self.length = length  # data length
        self.ctype = ctype  # 4-char ASCII
        self.data = data  # raw bytes of data
        self.order = order  # integer extracted from original CRC field

    def write(self, f):
        # Write length
        f.write(struct.pack(">I", self.length))
        # Write type and data
        type_bytes = self.ctype.encode("ascii")
        f.write(type_bytes)
        f.write(self.data)
        # Recalculate CRC over type and data
        crc = zlib.crc32(type_bytes)
        crc = zlib.crc32(self.data, crc)
        f.write(struct.pack(">I", crc & 0xFFFFFFFF))


def read_chunks(f):
    chunks = []
    while True:
        # Read length (4 bytes)
        length_bytes = f.read(4)
        if len(length_bytes) < 4:
            break
        length = struct.unpack(">I", length_bytes)[0]
        # Read type
        ctype = f.read(4).decode("ascii")
        if ctype not in ALLOWED_TYPES:
            sys.exit(f"Error: unsupported chunk type {ctype}")
        print(f"Reading a {ctype} chunk")
        # Read data
        data = f.read(length)
        # Read original CRC, treat as order
        crc_bytes = f.read(4)
        order = int.from_bytes(crc_bytes, "big")
        chunks.append(PNGChunk(length, ctype, data, order))
    return chunks


def reorder_chunks(chunks):
    # Sort by stored order field
    return sorted(chunks, key=lambda c: c.order)


def main(in_path, out_path):
    with open(in_path, "rb") as fin:
        sig = fin.read(8)
        if sig != b"\x89PNG\r\n\x1a\n":
            sys.exit("Error: not a PNG file")
        chunks = read_chunks(fin)

    # Reorder according to embedded order
    reordered = reorder_chunks(chunks)

    # Write out new PNG with correct CRCs
    with open(out_path, "wb") as fout:
        fout.write(sig)
        for chunk in reordered:
            chunk.write(fout)

    print(f"Wrote reordered PNG to {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.png> <output.png>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
