from Server import Server
import sys


class PyServer(Server):

    def __init__(self, verb=True, host='', port=8888):
        super().__init__(verb, host, port)
        self._pymagotchis = []


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
                if client_input.startswith('hello:'):
                    print(f'Hello !')
                    print(f'Réponse : ' + ':'.join(self._pymagotchis))
                    connection.sendall(':'.join(self._pymagotchis).encode('utf8'))
                    self._pymagotchis.append(client_input.split(':')[1])

        return is_active


if __name__ == '__main__':
    server_port = 8888
    if len(sys.argv) == 2:
       server_port = int(sys.argv[1])
    s = PyServer(port=server_port)
    s.start()
