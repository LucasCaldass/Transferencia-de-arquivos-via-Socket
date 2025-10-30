import sys
from server import start_server
from client import start_client, send_file, request_file

#TO DO: Fazer o servidor rodar mesmo após a transferência acontecer FEITO
#TO DO: Verificar se o arquivo já existe no diretório; Falta implementar a lógica no lado do servidor FEITO
#TO DO: Implementar o uso de Threads FEITO

if __name__ == '__main__':

    #A entrada será feita da forma indicada, para utilizar o servidor passa-se como parâmetro main.py server;
    #já para transferir um arquivo (cliente), passa-se main.py client e o caminho do arquivo na máquina de origem
    if len(sys.argv) < 2:
        print("Uso:")
        print("  Modo Servidor: python main.py server")
        print("  Modo Cliente:  python main.py client <caminho_do_arquivo>")
        sys.exit(1)

    mode = sys.argv[1].lower()

    #Inicia o servidor
    if mode == 'server':
        start_server()

    #Inicia o envio do arquivo como cliente
    elif mode == 'client':
        if len(sys.argv) < 3:
            print("Erro: O modo cliente requer o caminho do arquivo.")
            print("  Uso: python main.py client <caminho_do_arquivo>")
            sys.exit(1)

        socket = start_client()

        archive_path = sys.argv[2]

        if request_file(archive_path, socket):
            send_file(archive_path, socket)
            socket.close()
        else:
            print('O arquivo já existe no diretório de destino.')


    else:
        print(f"Modo '{mode}' desconhecido. Use 'server' ou 'client'.")
        sys.exit(1)
