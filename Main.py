import sys
import atexit
import telegram
import asyncio
import struct
import telegram.ext
from Protocol import *

host = 'localhost'
port = 1215
global chat_id

async def start_server():
    server = await asyncio.start_server(handler, host=host, port=port)
    async with server:
        await server.serve_forever()


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    global chat_id
    token: str
    bot: telegram.ext.ExtBot = None
    buffer: bytes = b''
    while True:
        try:
            data: bytes = await reader.read(1024)
            if not data:
                print("connection closed")
                writer.close()
                await writer.wait_closed()
                break
        except Exception as e:
            print(e)
            print("exception connection closed")
            break

        print("data size %d" % len(data))
        buffer += data
        # 데이터가 버퍼에 연속적으로 쌓이기 때문에 이 루프에서 버퍼에 있는 데이터를 전부 처리해서 비워야한다.
        while True:
            print("buffer size %d" % len(buffer))
            # protocol, body의 길이
            (protocol, body_length), buffer = struct.unpack('ii', buffer[:8]), buffer[8:]
            print("Protocol: %d" % protocol)

            # 남은 버퍼의 크기가 읽어야할 바디 크기보다 작다면 다음 read를 기다린다.
            if len(buffer) < body_length:
                break

            body = buffer[:body_length].decode('utf-8')
            print("Body: %s" % body)

            if protocol == EProtocol.INFO.value:
                print("INFO")
            elif protocol == EProtocol.TOKEN.value:
                try:
                    print("token = %s" % body)
                    bot = telegram.Bot(token=body)
                except Exception as e:
                    print(e)
                print("Bot Connected : %s" % body)
            elif protocol == EProtocol.CHAT.value:
                if bot is not None:
                    try:
                        result = await bot.send_message(chat_id=chat_id, text=body)
                        print(result)
                    except Exception as e:
                        print(e)
                else:
                    print("Bot is None!")
            else:
                print("None Protocol")

            # 남은 데이터 처리
            buffer = buffer[body_length:]
            if len(buffer) <= 8:
                break

if __name__ == "__main__":
    global chat_id
    with open("telegram.txt") as f:
        print("Telegram ID file open")
        chat_id = f.readline().strip()

    asyncio.run(start_server(), debug=True)
    print("End Telegram Interface")
