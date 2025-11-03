# 📁 Gerenciador de Transferência de Arquivos TCP

Este projeto implementa um sistema simples de transferência de arquivos entre um cliente e um servidor utilizando sockets TCP em Python, com suporte a **multithreading** para o servidor e verificação de **existência de arquivo** antes da transferência.

## ✨ Funcionalidades

  * **Transferência de Arquivos Confiável:** Utiliza o protocolo TCP.
  * **Servidor Multithreaded:** Capaz de lidar com múltiplas conexões de clientes simultaneamente.
  * **Verificação de Existência:** O servidor verifica se o arquivo já existe no diretório de destino (`Arquivos Recebidos`) antes de iniciar a transferência.
  * **Controle de Fluxo:** Envia e recebe arquivos em partes (`BUFFER_SIZE`).

## ⚙️ Pré-requisitos

Para executar este projeto, você precisa ter instalado:

  * **Python 3.x**

Não são necessárias bibliotecas externas além das nativas do Python (`socket`, `os`, `sys`, `threading`).

## 🚀 Como Executar

O projeto pode ser executado em dois modos: **Servidor** e **Cliente**.

### 1\. Iniciar o Servidor

O servidor deve ser iniciado primeiro e ficará escutando por conexões na porta e endereço configurados (`0.0.0.0:9999`).

1.  **Abra um terminal.**

2.  **Execute o comando:**

    ```bash
    python main.py server
    ```

3.  **Saída esperada:**

    ```
    Server listening em 0.0.0.0:9999
    ```

O servidor agora está pronto para receber conexões de clientes. Os arquivos recebidos serão salvos no diretório **`Arquivos Recebidos/`** (que será criado automaticamente).

### 2\. Enviar um Arquivo (Modo Cliente)

O cliente é usado para se conectar ao servidor e iniciar a transferência de um arquivo.

1.  **Abra um SEGUNDO terminal** (ou use outra máquina que possa se conectar ao servidor).

2.  **Execute o comando,** substituindo `<caminho_do_arquivo>` pelo caminho completo ou relativo do arquivo que você deseja enviar:

    ```bash
    python main.py client <caminho_do_arquivo>
    ```

    **Exemplo:**

    ```bash
    python main.py client ./documentos/foto_perfil.jpg
    ```

#### 📌 Notas de Execução do Cliente:

  * **Arquivo Inexistente no Servidor:** Se o arquivo *não* existir no diretório `Arquivos Recebidos/` do servidor, a transferência começará:
    ```
    O arquivo <nome_do_arquivo> será enviado.
    Arquivo <nome_do_arquivo> enviado com sucesso.
    ```
  * **Arquivo Existente no Servidor:** Se o arquivo *já* existir no diretório `Arquivos Recebidos/` do servidor, a transferência será abortada, e uma mensagem será exibida:
    ```
    O arquivo já existe no diretório de destino.
    ```
  * **Servidor Desligado:** Se o servidor não estiver rodando, a conexão falhará:
    ```
    Não foi possível conectar ao servidor.
    ```

-----
