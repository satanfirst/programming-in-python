import socket
import time


class ClientError(Exception):
    pass


def format_data(data):
    result_dict = {}
    raw_data = data.decode().split(sep='\n')
    if data.decode() == "ok\n\n":
        return {}
    elif data.decode()[3:] != 'ok\n' and data.decode()[-2:] != '\n\n':
        raise ClientError
    else:
        try:
            for raw_item in raw_data[1:-2]:
                item = raw_item.split(sep=' ')
                key, timestamp, value = item[0], int(item[2]), float(item[1])
                if result_dict.get(item[0]):
                    result_dict[key].append((timestamp, value))
                    result_dict[key].sort(key=lambda i: i[0])
                else:
                    result_dict[key] = [(timestamp, value)]

            return result_dict
        except:
            raise ClientError


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.conn = socket.create_connection((self.host, self.port), self.timeout)

    def get(self, metric):
        try:
            self.conn.sendall(('get ' + metric + '\n').encode())
            data = self.conn.recv(1024)
            return format_data(data)
        except ClientError:
            raise ClientError

    def put(self, metric, metric_value, timestamp=None):
        try:
            if timestamp is None:
                timestamp = int(time.time())
            data = 'put ' + metric + ' ' + str(metric_value) + ' ' + str(timestamp) + '\n'
            self.conn.sendall(data.encode())
            answer = self.conn.recv(1024)
            if answer.decode() != 'ok\n\n':
                raise ClientError
        except ClientError:
            raise ClientError


def main():
    pass
    #client = Client("127.0.0.1", 8888, timeout=15)
    # client.put("palm.cpu", 10, timestamp=1150864248)
    # client.put("palm.cpu", 1, timestamp=1150864247)
    # client.put("palm.cpu", 0.5, timestamp=1150864248)
    # client.put("eardrum.cpu", 4, timestamp=1150864251)
    # client.put("eardrum.cpu", 3, timestamp=1150864250)
    # client.put("palm.cpu", 0.5, timestamp=1000864000)
    # client.put("eardrum.cpu", 4, timestamp=1000864251)
    # client.put("palm.cpu", 0.5, timestamp=5000864240)
    # client.put("eardrum.memory", 2, timestamp=1000004251)
    #print(client.get("*"))


if __name__ == '__main__':
    main()
