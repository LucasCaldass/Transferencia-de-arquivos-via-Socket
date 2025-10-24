import socket
import os
#import threading

BUFFER_SIZE = 4096
HOST = '0.0.0.0'
PORT = 9999
METADATA_SIZE = 1024
RECEIVE_DIR = 'Arquivos Recebidos'


def file_exists_on_folder(archive_path):
    return os.path.exists(archive_path)

def transfer_file(conn):
    if not os.path.exists(RECEIVE_DIR):
        os.makedirs(RECEIVE_DIR)

    with conn:
        metadata_raw = conn.recv(METADATA_SIZE).decode('utf-8').strip()

        if not metadata_raw:
            print('Nenhum arquivo encontrado.')
            return

        try:
            file_name, file_size = metadata_raw.split(':', 1)
            file_size = int(file_size)
        except ValueError:
            print('Metadados inválidos')
            return



        file_path = os.path.join(RECEIVE_DIR, os.path.basename(file_name))

        print(f'O arquivo {file_name} de tamanho {file_size} será recebido!')

        bytes_received = 0
        try:
            with open(file_path, 'wb') as file:
                while bytes_received < file_size:
                    remaining_bytes = file_size - bytes_received
                    data = conn.recv(min(BUFFER_SIZE, remaining_bytes))

                    if not data:
                        print('Fim da transferência de dados. Encerrando conexão...')
                        break

                    file.write(data)
                    bytes_received += len(data)

            if bytes_received == file_size:
                print('Arquivo recebido com sucesso!')

            else:
                print(f'Arquivo incompleto! Somente foram recebidos {bytes_received} de {file_size} bytes.')

        except IOError as e:
            print(f'Erro de I/O ao tentar salvar o arquivo {file_name}: {e}')
        except EOFError as e:
            print(f'Um erro ocorreu {e}')


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Aguardando conexão ao servidor...')
        s.bind((HOST, PORT))
        s.listen(5)

        while True:
            conn, addr = s.accept()
            print('Conectado ao servidor com sucesso!')

            transfer_file(conn)
