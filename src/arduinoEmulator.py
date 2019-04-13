from time import sleep
import socket
import random

class ArduinoEmulator:
    def __init__(self):
        self.identifier = 'a23sdv1'
        self.value = 200
        #self.sock = socket.socket()

    def start(self):
        self.setup()
        self.loop()

    def parse_data(self):
        return '{}:{}'.format(self.identifier,
                              self.value)

    def send(self, ip, port, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        try:
            sock.sendall(bytes(message, 'ascii'))
            print('"{}" send to {}:{} successfully'.format(message,
                                                            ip,
                                                            port))
            if message == 'NS':
                # local_adress = sock.getsockname()
                # sock.close()
                # sock = socket.socket()
                # sock.bind(local_adress)
                # sock.listen(1)
                # response = b''
                while True:
                    response = sock.recv(1024)
                    # print(response)
                    if not response:
                        break
                    self.identifier = response

                if len(response):
                    print('Response from {}:{} {}'.format(ip, port, response.decode()))
                self.identifier = response.decode()
            sock.close()
        except Exception as ex:
            print('Error while sending "{}" to {}:{}: {}'.format(message, ip, port, ex))
        finally:
            pass
            sock.close()

    def setup(self):
        #self.send('localhost', 8887, 'NS')
        pass


    def loop(self):
        while True:
            self.value = 200 + random.randrange(-10, 10)

            if self.identifier != '':
                self.send('localhost', 8887, self.parse_data())
            sleep(1)


if __name__ == '__main__':
    arduino = ArduinoEmulator()
    arduino.start()
