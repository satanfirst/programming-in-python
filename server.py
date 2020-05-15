import asyncio
import re


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print(f'Connection from {peername}')
        self.transport = transport

    def data_received(self, data):
        storage = {'key': 'value'}
        resp = self.process_data(data.decode(), storage)
        print(f'Data received: {resp}')
        self.transport.write(b'ok')
        print('Send: ok')
        print(f'Send: {resp}')

    @staticmethod
    def process_data(data, storage):
        if re.match(r'get ', data):
            return storage['key']
        return 'error\nwrong command\n\n'

run_server('127.0.0.1', 3000)
