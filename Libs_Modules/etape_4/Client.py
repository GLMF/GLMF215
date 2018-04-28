import socket
import os
from time import sleep



class Client:

    def __init__(self, verb=True, host='', port=8888):
        self._host = host
        self._port = port
        self._verb = verb


    def start(self):
        self._soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self._soc.connect((self._host, self._port))
        except:
            if self._verb:
                print('On doit créer le serveur')
            os.system(f'python3.6 ./Server.py {self._port} &')
            try:
                sleep(1)
                self._soc.connect((self._host, self._port))
            except Exception as e:
                if self._verb:
                    print('Connection error :', e)
                exit(1)

        self._process_input()


    def _process_input(self):
        print('Tapez <q> pour quitter')
        message = input(' -> ')

        while message != 'q':
            self._soc.sendall(message.encode('utf8'))
            if self._soc.recv(5120).decode('utf8') == '-':
                print('Message reçu par le serveur')

            message = input(' -> ')

        self._soc.send(b'--quit--')



if __name__ == '__main__':
    client = Client(port=15131)
    client.start()
