import sys
from server import start_server
from client import start_client, send_file, request_file

#TO DO: Fazer o servidor rodar mesmo após a transferência acontecer FEITO
#TO DO: Verificar se o arquivo já existe no diretório; Falta implementar a lógica no lado do servidor
#TO DO: Implementar o uso de Threads
#TO DO: Revisar a arquitetura e o funcionamento do software

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Uso:")
        print("  Modo Servidor: python main.py server")
        print("  Modo Cliente:  python main.py client <caminho_do_arquivo>")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == 'server':
        start_server()

    elif mode == 'client':
        if len(sys.argv) < 3:
            print("Erro: O modo cliente requer o caminho do arquivo.")
            print("  Uso: python main.py client <caminho_do_arquivo>")
            sys.exit(1)

        socket = start_client()

        archive_path = sys.argv[2]

        if request_file(archive_path, socket):
            send_file(archive_path, socket)
        else:
            print('O arquivo já existe no diretório de destino.')

    else:
        print(f"Modo '{mode}' desconhecido. Use 'server' ou 'client'.")
        sys.exit(1)
