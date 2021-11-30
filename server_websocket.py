import asyncio
import websockets
from datetime import datetime
import queue
class Websocket:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.path = None
        self.CLIENTS_info_ticks = set()
        self.CLIENTS_info_accounts = set()
        self.workQueue = queue.Queue(10)

    def startServer(self):
        loop = asyncio.get_event_loop()
        # loop.create_task(self.mt5InfoTickStream())
        # loop.create_task(self.mt5AccountInfo())

        start_server = websockets.serve(self.router, self.host, self.port)
        loop.run_until_complete(start_server)
        loop.run_forever()

    async def messageSend(self, ws, message):
        try:
            await ws.send(message)
            return True
        except Exception as error:
            print(error)
            return False

    async def router(self, websocket, path):
        index = path.find('/') + len('/')
        variable = path[index:].split('/')

        if variable[0] != "v1":
            await self.messageSend(websocket, "unsupported version")
        else:
            if len(variable) < 2:
                await self.messageSend(websocket, "Ne istiyorsun amcık")
            else:
                if variable[1] == "info_ticks":
                    self.CLIENTS_info_ticks.add(websocket)
                    print(
                        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | New Client -> info_ticks {websocket.remote_address[0]}")
                    try:
                        async for msg in websocket:
                            pass
                    except websockets.ConnectionClosedError:
                        pass
                    finally:
                        self.CLIENTS_info_ticks.remove(websocket)
                elif variable[1] == "accounts_info":
                    self.CLIENTS_info_accounts.add(websocket)
                    print(
                        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | New Client -> accounts_info {websocket.remote_address[0]}")
                    try:
                        async for msg in websocket:
                            pass
                    except websockets.ConnectionClosedError:
                        pass
                    finally:
                        self.CLIENTS_info_accounts.remove(websocket)
                else:
                    await self.messageSend(websocket, "unsupported event")

    async def örnek_döngü(self):
        while True:
            df_accounf_info = []
            await asyncio.gather(
                *[self.messageSend(ws, str(df_accounf_info.to_json(orient="index"))) for ws in self.CLIENTS_info_accounts],
                return_exceptions=False,
            )
            await asyncio.sleep(1)


if __name__ == "__main__":
    websocket = Websocket("127.0.0.1", 3131)
    websocket.startServer()