import socket
import os

BUFFER_SIZE = 4096
HOST = '127.0.0.1'
PORT = 9999
METADATA_SIZE = 1024


def start_client(archive):
    with (socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s):
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print('Não foi possível conectar ao servidor.')
            exit()

        file_name = os.path.basename(archive)

        try:
            file_size = os.path.getsize(archive)
        except FileNotFoundError:
            print(f'Arquivo {file_name} não encontrado.')
            exit()

        metadata = f'{file_name}:{file_size}'
        s.sendall(metadata.encode('utf-8').ljust(METADATA_SIZE))

        print(f'O arquivo {file_name} será enviado.')

        try:
            with open(archive, 'rb') as f:
                while True:
                    bytes_read = f.read(BUFFER_SIZE)

                    if not bytes_read:
                        break

                    s.sendall(bytes_read)
            print(f'Arquivo {file_name} enviado com sucesso.')

            s.shutdown(socket.SHUT_WR)

        except FileNotFoundError:
            print(f'Arquivo {file_name} não encontrado.')
