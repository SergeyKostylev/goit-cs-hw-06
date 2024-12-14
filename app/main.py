import json
from datetime import datetime
from multiprocessing import Process
from pymongo import MongoClient
import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import asyncio
import logging
import websockets
from websockets.exceptions import ConnectionClosedOK

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    def __init__(self):
        self.__client = MongoClient('mongodb://mongodb:27017/')
        self.db = self.__client['chat']
        self.collection = self.db['messages']

    async def register(self, ws):
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws):

        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws):
        async for message in ws:
            data = json.loads(message)
            print(data)
            name = data['name'] if 'name' in data and data['name'] else 'Anonim'
            message = data['message'] if 'name' in data and data['message'] else ''
            self.collection.insert_one(
                {
                    "name": name,
                    "message": message,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                }
            )
            logging.info(f">> {name} <<:   {message}")
            await self.send_to_clients(f">> {name} <<:   {message}")


async def main():
    try:
        server = Server()
        async with websockets.serve(server.ws_handler, "0.0.0.0", 5099):
            await asyncio.get_running_loop().create_future()  # run forever
    except KeyboardInterrupt:
        print("Server stopped by user")
    except Exception as e:
        print(f"Error: {e}")


def run_async():
    asyncio.run(main())


PORT = 3000


async def main_site():
    os.chdir("src")

    class Handler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if not os.path.exists(self.translate_path(self.path)):
                self.send_response(301)
                self.send_header('Location', 'error.html')
                self.end_headers()
            else:
                super().do_GET()

    Handler = Handler

    with TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()


def run_async_site():
    asyncio.run(main_site())


if __name__ == "__main__":
    process1 = Process(target=run_async)
    process2 = Process(target=run_async_site)

    process1.start()
    process2.start()
    process1.join()
    process2.join()
