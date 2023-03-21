import sys
import atexit
import asyncio
import struct
from Protocol import *

host = 'localhost'
port = 1215


async def start_server():
    server = await asyncio.start_server(handler, host=host, port=port)

    async with server:
        await server.serve_forever()


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    url: str
    while True:
        data: bytes = await reader.read(1024)

        if not data:
            print("connection closed")
            break

        print("size %d" % len(data))
        # protocol, body의 길이
        (protocol, body_length), data = struct.unpack('ii', data[:8]), data[8:]
        print("Protocol: %d" % protocol)
        body = data[:body_length]
        body.decode('utf-8')
        print("Body: %s" % repr(body))

        if protocol == EProtocol.INFO:
            print("INFO")
        elif protocol == EProtocol.URL:
            print("URL")


if __name__ == "__main__":
    asyncio.run(start_server(), debug=True)
    print("End Telegram Interface")
