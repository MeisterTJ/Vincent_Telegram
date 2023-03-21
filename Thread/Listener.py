import threading
import asyncio
import struct
from Protocol import *

class Listener(threading.Thread):
    def __init__(self):
        super().__init__()
        self.host = 'localhost'
        self.port = 1215

    def run(self):
        asyncio.run(self.listen(), debug=True)

    async def listen(self):
        server = await asyncio.start_server(self.handler, host=self.host, port=self.port)

        print("serve forever1")
        async with server:
            print("serve forever2")
            await server.serve_forever()

    async def handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        url: str
        while True:
            data: bytes = await reader.read(1024)
            protocol, body = struct.unpack('bs', data)
            print("Protocol: %d" % protocol)
            print("Body: %s" % repr(body))

            if protocol == EProtocol.INFO:
                print("INFO")
            elif protocol == EProtocol.URL:
                print("URL")
