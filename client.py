import socket
import os

BUFFER_SIZE = 4096
HOST = '127.0.0.1'
PORT = 9999
METADATA_SIZE = 1024


#Retorna o nome do arquivo
def get_file_name(archive_path):
    file_name = os.path.basename(archive_path)
    return file_name


#Parte do handshake de verificação da existência do arquivo do lado do cliente
def request_file(archive_path, s):
    file_name = get_file_name(archive_path)
    s.sendall(file_name.encode('utf-8').ljust(METADATA_SIZE))

    #Recebe a resposta do servidor a respeito da existência do arquivo
    response = s.recv(10).decode('utf-8').strip().upper()

    if response == 'OK':
        return True
    elif response == 'EXISTS':
        print('O arquivo já existe no diretório de destino.')
        return False
    else:
        print('Erro na solicitação do envio do arquivo.')
        return False


#Função para enviar o arquivo para o servidor
def send_file(archive_path, s):
    file_name = get_file_name(archive_path)

    #Recebe o tamanho do arquivo
    try:
        file_size = os.path.getsize(archive_path)
    except FileNotFoundError:
        print(f'Arquivo {file_name} não encontrado.')
        exit()

    #Cria os metadados do arquivo e envia para o servidor
    metadata = f'{file_name}:{file_size}'
    s.sendall(metadata.encode('utf-8').ljust(METADATA_SIZE))

    print(f'O arquivo {file_name} será enviado.')

    #Aqui o cliente abre o arquivo a ser enviado e os envia por partes
    # até que o tamanho total do arquivo seja enviado ao servidor
    try:
        with open(archive_path, 'rb') as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)

                if not bytes_read:
                    break

                #Função que envia os bytes para o servidor
                s.sendall(bytes_read)
        print(f'Arquivo {file_name} enviado com sucesso.')

        #Encerra o socket cliente
        s.shutdown(socket.SHUT_WR)

    #Lança a exceção caso o arquivo não exista
    except FileNotFoundError:
        print(f'Arquivo {file_name} não encontrado.')


#Inicia o client
def start_client():
    #Inicializa o objeto Socket com endereço IPv4 e rodando sob o protocolo TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conecta o socket do client utilizando o ip local e a porta do servidor
    try:
        s.connect((HOST, PORT))
    #Lança a exceção caso não seja possível se conectar ao server
    except ConnectionRefusedError:
        print('Não foi possível conectar ao servidor.')
        exit()
    #Lança alguma outra possível exceção que possa ocorrer durante a tentativa de conexão
    except Exception as e:
        s.close()
        raise e
    return s