import socket
import os
import threading

BUFFER_SIZE = 4096
HOST = '0.0.0.0'
PORT = 9999
METADATA_SIZE = 1024
RECEIVE_DIR = 'Arquivos Recebidos'


#Verifica se o arquivo que será enviado já existe no diretório de destino
def file_exists_on_folder(archive_path):
    return os.path.exists(archive_path)


#Inicia a verificação da existência do arquivo e se for o caso, inicia a transferência
def handle_client(conn, addr):
    try:
        #Cria o diretório onde os arquivos recebidos ficarão
        if not os.path.exists(RECEIVE_DIR):
            os.makedirs(RECEIVE_DIR)

        #Recebe o nome do arquivo que se deseja verificar
        requested_filename = conn.recv(METADATA_SIZE).decode('utf-8').strip()
        if not requested_filename:
            print(f'[{addr}] Request vazia. Fechando.')
            return

        req_filename = os.path.basename(requested_filename)
        target_path = os.path.join(RECEIVE_DIR, req_filename)

        #Verifica se o arquivo existe e retorna uma mensagem para o cliente permitindo ou não o envio do arquivo
        if file_exists_on_folder(target_path):
            conn.sendall('EXISTS'.encode('utf-8'))
            print(f'[{addr}] Client solicitou {req_filename} -> EXISTS')
            return
        else:
            conn.sendall('OK'.encode('utf-8'))
            print(f'[{addr}] Client solicitou {req_filename} -> OK, esperando pela metadata do arquivo')

        #Recebe os metadados do arquivo, nome e tamanho
        metadata_raw = conn.recv(METADATA_SIZE).decode('utf-8').strip()
        if not metadata_raw:
            print(f'[{addr}] Metadata não recebida depois do OK. Fechando.')
            return

        #Extrai as informações do arquivo dos metadados
        try:
            file_name, file_size = metadata_raw.split(':', 1)
            file_size = int(file_size)
        except ValueError:
            print(f'[{addr}] Metadata invalida: {metadata_raw}')
            return

        
        file_name = os.path.basename(file_name)
        file_path = os.path.join(RECEIVE_DIR, file_name)

        print(f'[{addr}] Recebendo {file_name} ({file_size} bytes)')

        #Controle do recebimento dos bytes do arquivo
        bytes_received = 0
        with open(file_path, 'wb') as f:
            while bytes_received < file_size:
                remaining = file_size - bytes_received
                #Recebe o arquivo de acordo com o tamanho do buffer
                chunk = conn.recv(min(BUFFER_SIZE, remaining))
                if not chunk:
                    break
                f.write(chunk)
                bytes_received += len(chunk)
        #Se o arquivo for recebido com sucesso
        if bytes_received == file_size:
            print(f'[{addr}] Arquivo recebido com sucesso: {file_name}')
        #Se houver algum problema ele indicará quantos bytes foram recebidos
        else:
            print(f'[{addr}] Arquivo incompleto: recebido {bytes_received} of {file_size} bytes')

    #Se houver algum erro ele lançará uma exceção
    except Exception as e:
        print(f'[{addr}] Erro no client: {e}')
    #Fecha o socket do lado do client
    finally:
        conn.close()


#Inicializa o servidor
def start_server():
    #Cria um objeto do tipo Socket
    #AF_INET = Endereços IPv4
    #SOCK_STREAM = Utiliza o protocolo TCP para o envio do arquivo
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #Liga o socket criado à porta e endereço do local host
        s.bind((HOST, PORT))
        #Escuta por conexões
        s.listen(5)
        print(f'Server listening em {HOST}:{PORT}')
        #Inicia a conexão relativa ao cliente
        while True:
            conn, addr = s.accept()
            print(f'Conexao aceita de {addr}')
            #Cria uma thread com o endereço referente ao cliente para haver a paralelização do serviço
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
