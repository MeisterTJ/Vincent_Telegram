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
    bots = {}  #: telegram.ext.ExtBot = None
    buffer: bytes = b''
    while True:
        try:
            data: bytes = await reader.read(2048)
            if not data:
                print("connection closed")
                writer.close()
                await writer.wait_closed()
                break
        except Exception as e:
            print(e)
            print("exception connection closed")
            break

        #print("data size %d" % len(data))
        buffer += data
        # 데이터가 버퍼에 연속적으로 쌓이기 때문에 이 루프에서 버퍼에 있는 데이터를 전부 처리해서 비워야한다.
        while True:
            #print("buffer size %d" % len(buffer))
            # protocol, body의 길이
            (protocol, body_length), buffer = struct.unpack('ii', buffer[:8]), buffer[8:]
            #print("Protocol: %d" % protocol)

            # 남은 버퍼의 크기가 읽어야할 바디 크기보다 작다면 다음 read를 기다린다.
            if len(buffer) < body_length:
                break

            body = buffer[:body_length].decode('utf-8')
            #print("Body: %s" % body)

            if protocol == EProtocol.INFO.value:
                print("INFO")
            # 봇 정보
            elif protocol == EProtocol.BOT_INFO.value:
                try:
                    splits: list = body.split(";")
                    name = splits[0]
                    token = splits[1]
                    bots.update({name: telegram.Bot(token=token)})
                    print("bot = %s, token = %s" % (name, token))
                    await bots[name].send_message(chat_id=chat_id, text="클라이언트 연결 성공")
                except Exception as e:
                    print(e)
            # 메시지 날림
            elif protocol == EProtocol.CHAT.value:
                splits: list = body.split(";")
                name = splits[0]
                message = splits[1]
                if bots.__contains__(name):
                    try:
                        await bots[name].send_message(chat_id=chat_id, text=message)
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

    # 클라이언트 연결 종료 후 처리
    for bot in bots.values():
        await bot.send_message(chat_id=chat_id, text="클라이언트 연결 끊김")

if __name__ == "__main__":
    global chat_id
    with open("telegram.txt") as f:
        print("Telegram ID file open")
        chat_id = f.readline().strip()

    asyncio.run(start_server(), debug=True)
    print("End Telegram Interface")
