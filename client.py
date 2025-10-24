import socket
import os

BUFFER_SIZE = 4096
HOST = '127.0.0.1'
PORT = 9999
METADATA_SIZE = 1024


def get_file_name(archive_path):
    file_name = os.path.basename(archive_path)
    return file_name


def request_file(archive_path, s):
    file_name = get_file_name(archive_path)
    s.sendall(file_name.encode('utf-8').ljust(METADATA_SIZE))

    response = s.recv(10).decode('utf-8').strip().upper()

    if response == 'OK':
        return True
    elif response == 'EXISTS':
        print('O arquivo já existe no diretório de destino.')
        return False
    else:
        print('Erro na solicitação do envio do arquivo.')
        return False


def send_file(archive_path, s):
    file_name = get_file_name(archive_path)

    try:
        file_size = os.path.getsize(archive_path)
    except FileNotFoundError:
        print(f'Arquivo {file_name} não encontrado.')
        exit()

    metadata = f'{file_name}:{file_size}'
    s.sendall(metadata.encode('utf-8').ljust(METADATA_SIZE))

    print(f'O arquivo {file_name} será enviado.')

    try:
        with open(archive_path, 'rb') as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)

                if not bytes_read:
                    break

                s.sendall(bytes_read)
        print(f'Arquivo {file_name} enviado com sucesso.')

        s.shutdown(socket.SHUT_WR)

    except FileNotFoundError:
        print(f'Arquivo {file_name} não encontrado.')


def start_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        print('Não foi possível conectar ao servidor.')
        exit()
    except Exception as e:
        s.close()
        raise e
    return s