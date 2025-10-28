import socket
import os
import threading

BUFFER_SIZE = 4096
HOST = '0.0.0.0'
PORT = 9999
METADATA_SIZE = 1024
RECEIVE_DIR = 'Arquivos Recebidos'


def file_exists_on_folder(archive_path):
    return os.path.exists(archive_path)


def handle_client(conn, addr):
    try:
        if not os.path.exists(RECEIVE_DIR):
            os.makedirs(RECEIVE_DIR)

        # handshake aqui
        initial = conn.recv(METADATA_SIZE).decode('utf-8').strip()
        if not initial:
            print(f'[{addr}] Request vazia. Fechando.')
            return

        
        req_filename = os.path.basename(initial)
        target_path = os.path.join(RECEIVE_DIR, req_filename)

        if file_exists_on_folder(target_path):
            conn.sendall('EXISTS'.encode('utf-8'))
            print(f'[{addr}] Client solicitou {req_filename} -> EXISTS')
            return
        else:
            conn.sendall('OK'.encode('utf-8'))
            print(f'[{addr}] Client solicitou {req_filename} -> OK, esperando pela metadata do arquivo')

        
        metadata_raw = conn.recv(METADATA_SIZE).decode('utf-8').strip()
        if not metadata_raw:
            print(f'[{addr}] Metadata não recebida depois do OK. Fechando.')
            return

        try:
            file_name, file_size = metadata_raw.split(':', 1)
            file_size = int(file_size)
        except ValueError:
            print(f'[{addr}] Metadata invalida: {metadata_raw}')
            return

        
        file_name = os.path.basename(file_name)
        file_path = os.path.join(RECEIVE_DIR, file_name)

        print(f'[{addr}] Recebendo {file_name} ({file_size} bytes)')

        bytes_received = 0
        with open(file_path, 'wb') as f:
            while bytes_received < file_size:
                remaining = file_size - bytes_received
                chunk = conn.recv(min(BUFFER_SIZE, remaining))
                if not chunk:
                    break
                f.write(chunk)
                bytes_received += len(chunk)

        if bytes_received == file_size:
            print(f'[{addr}] Arquivo recebido com sucesso: {file_name}')
        else:
            print(f'[{addr}] Arquivo incompleto: recebido {bytes_received} of {file_size} bytes')

    except Exception as e:
        print(f'[{addr}] Erro no client: {e}')
    finally:
        conn.close()


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f'Server listening em {HOST}:{PORT}')
        while True:
            conn, addr = s.accept()
            print(f'Conexao aceita de {addr}')
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
