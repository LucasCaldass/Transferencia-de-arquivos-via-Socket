import sys
from server import start_server
from client import start_client


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Uso:")
        print("  Modo Servidor: python app.py server")
        print("  Modo Cliente:  python app.py client <caminho_do_arquivo>")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == 'server':
        start_server()

    elif mode == 'client':
        if len(sys.argv) < 3:
            print("Erro: O modo cliente requer o caminho do arquivo.")
            print("  Uso: python app.py client <caminho_do_arquivo>")
            sys.exit(1)

        archive_path = sys.argv[2]
        start_client(archive_path)

    else:
        print(f"Modo '{mode}' desconhecido. Use 'server' ou 'client'.")
        sys.exit(1)