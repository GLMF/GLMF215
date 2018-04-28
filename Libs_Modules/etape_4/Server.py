import socket
import sys
from threading import Thread



class Server:

    def __init__(self, verb=True, host='', port=8888):
        self._host = host
        self._port = port
        self._previous_connexions = 0
        self._connexions = 0
        self._soc = None
        self._stop = False
        self._verb = verb


    def _add_new_connexion(self):
        self._previous_connexions = self._connexions
        self._connexions += 1


    def _remove_connexion(self):
        self._previous_connexions = self._connexions
        self._connexions -= 1


    def start(self):
        self._soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self._soc.bind((self._host, self._port))
        except:
            if self._verb:
                print('Bind failed')
            exit(1)

        self._soc.listen(5)
        if self._verb:
            print(f'Serveur actif sur {self._host}:{self._port}')
  
        Thread(target=self._shutdown_server).start()

        while True:
            try:
                connection, address = self._soc.accept()
            except:
                if self._verb:
                    print('BYE')
                exit(0)
            ip, port = str(address[0]), str(address[1])
            if self._verb:
                print(f'Connexion du client {ip}:{port}')
            self._add_new_connexion()
  
            try:
                Thread(target=self._client_thread, args=(connection, ip, port)).start()
            except:
                if self._verb:
                    print('Impossible to start thread')
            

    def _shutdown_server(self):
        while True:
            if self._connexions == 0 and self._previous_connexions != 0:
                self._stop = True
                self._soc.shutdown(socket.SHUT_RDWR)
                break


    def _client_thread(self, connection, ip, port, max_buffer_size = 5120):
        is_active = True

        while is_active:
            client_input = self._receive_input(connection, max_buffer_size)

            is_active = self._process_input(client_input, connection, ip, port)


    def _process_input(self, client_input, connection, ip, port):
        is_active = True

        if '--quit--' in client_input:
            connection.close()
            if self._verb:
                print(f'Fermeture de la connexion {ip}:{port}')
            is_active = False
            self._remove_connexion()
        else:
            if self._verb:
                print(f'Recu de {ip}:{port} : {client_input}')
            connection.sendall('-'.encode('utf8'))

        return is_active


    def _receive_input(self, connection, max_buffer_size):
        client_input = connection.recv(max_buffer_size)
        client_input_size = sys.getsizeof(client_input)

        if client_input_size > max_buffer_size:
            if self._verb:
                print('Max buffer size of input reached : {client_input_size} > {max_buffer_size}')

        return str(client_input.decode('utf8').rstrip())



if __name__ == '__main__':
    server_port = 8888
    if len(sys.argv) == 2:
       server_port = int(sys.argv[1])
    s = Server(port=server_port)
    s.start()
