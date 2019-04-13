from src.server import Server
from random import choice
from src.utils import *

IDENTIFIER_LENGTH = 6
LETTERS_FOR_ID = [i for i in 'qwertyuiopasdfghjklzxcvbnmQWETYUIOPASDFGHJKLZXCVBNM1234567890']

class DataServer(Server):

    def __init__(self, ip, port):
        super().__init__(ip, port)
        self.sensors = {}

    @staticmethod
    def generate_identifier(len):
        return ''.join([choice(LETTERS_FOR_ID) for i in range(len)])

    def delete_sensor(self, key):
        if key in self.sensors:
            self.sensors.pop(key)
            print('Sensor with id {} deleted'.format(key))
        else:
            print('Undefined sensor')

    def add_sensor(self, sock):
        key = self.generate_identifier(IDENTIFIER_LENGTH)
        sock.send(key.encode())
        # print(*client_socket)
        # self.send(client_socket[0], client_socket[1], key)
        self.sensors[key] = {
            'value': 200
        }
        print('Sensor with id {} added'.format(key))

    def update_sensor(self, key, value):
        with connectDB() as con:
            with con.cursor() as cur:
                cur.execute("select count(*) from sensor where id='{id}'".format(
                    id=str(key)
                ))
                count = cur.fetchone()
                print(count)
                if count[0] == 0:
                    cur.execute("insert into sensor(id) values ('{id}')".format(
                        id=str(key)
                    ))
                    con.commit()
                cur.execute("insert into sensor_value(value, sensor) values({val}, '{sensor}')".format(
                    val=value,
                    sensor=key
                ))
                con.commit()
        print(self.sensors)
        self.sensors[key] = value

    def handle(self, message):
        try:
            data = message[0].decode()
            # client_socket = message[1]
            print("Got: {}".format(data))
            if data == 'NS':
                self.add_sensor(message[1])
            else:
                try:
                    identificator, value = data.split(':')
                    self.update_sensor(identificator, value)
                except ValueError:
                    print('Incorrect format "<id>:<value>"')
        except Exception as e:
            print("Error (handle): {}".format(e))


if __name__ == '__main__':
    server = DataServer('192.168.1.72', 8887)
    server.start_server()
    server.loop()
    server.stop_server()