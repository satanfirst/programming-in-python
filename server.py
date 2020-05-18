import asyncio



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
        self.storage = {}

    def data_received(self, data):
        resp = self.process_data(data.decode('utf-8'), self.storage)
        print(self.storage)
        print(f'Data received: {data}')
        self.transport.write(b'ok')
        print(f'Send: {resp}')

    @staticmethod
    def process_data(data, storage):
        if data.startswith('put ') and data.endswith('\n'):
            try:
                raw_data = data.split(sep=' ')
                name = raw_data[1]
                value = float(raw_data[2])
                timestamp = int(raw_data[3].split(sep='\n')[0])
                if type(name) is str and type(value) is float \
                        and type(timestamp) is int:
                    if storage.get(raw_data[1]):
                        storage[raw_data[1]].append([value, timestamp])
                    else:
                        storage[raw_data[1]] = [[value, timestamp]]
                    return 'ok\n\n'
            except:
                return 'error1\nwrong command\n\n'
        if data.startswith('get ') and data.endswith('\n'):
            try:
                raw_data = data.split(sep=' ')
                req = raw_data[1][:-1]
                return _read(storage, req)
            except:
                return 'error\nwrong command\n\n'
        return 'error\nwrong command\n\n'


def _read(d, val):
    result = 'ok\n'
    if val == '*':
        for k, v in d.items():
            for item in v:
                result += f'{k} {item[0]} {item[1]}\n'
    elif not d.get(val):
        return 'ok\n\n'
    else:
        for item in d.get(val):
            result += f'{val} {item[0]} {item[1]}\n'
    result += '\n'
    return result


run_server('127.0.0.1', 8888)
