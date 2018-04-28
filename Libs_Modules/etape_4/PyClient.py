from Client import Client
import socket
import os
from time import sleep



class PyClient(Client):

    def __init__(self, verb=True, host='', port=8888):
        super().__init__(verb, host, port)
        self._message = ''
        self._result = ''
        self._end = False


    def start(self):
        self._soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self._soc.connect((self._host, self._port))
        except:
            if self._verb:
                print('On doit créer le serveur')
            os.system(f'python3.6 ./PyServer.py {self._port} &')
            try:
                sleep(1)
                self._soc.connect((self._host, self._port))
            except Exception as e:
                if self._verb:
                    print('Connection error :', e)
                exit(1)

        self._process_input()


    def get_result(self):
        result = self._result
        self._result = ''
        return result    
    

    def hello(self, name):
        self._message = f'hello:{name}'

    
    def quit(self):
        print('On appelle QUIT')
        self._soc.send(b'--quit--')
        self._end = True


    def _process_input(self):
        while not self._end:
            if self._message != '':
                self._soc.sendall(self._message.encode('utf8'))
                self._result = self._soc.recv(5120).decode('utf8')
                self._message = ''
