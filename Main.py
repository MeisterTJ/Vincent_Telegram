from Thread.Listener import *

if __name__ == "__main__":
    threads = []
    listen_worker = Listener()

    # 메인이 종료될때 같이 종료
    listen_worker.daemon = True
    listen_worker.start()
    threads.append(listen_worker)

    for t in threads:
        t.join()

    print("End Telegram Interface")


