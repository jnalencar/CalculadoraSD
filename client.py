import socket

def main():
    # Configurações do servidor proxy reverso
    proxy_host = 'localhost'
    proxy_port = 5000

    # Criação do socket do cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((proxy_host, proxy_port))

    try:
        while True:
            # Solicita ao usuário a operação matemática
            operation = input("Digite a operação (ex: 2 + 2): ")

            # Envia a operação para o proxy reverso
            client_socket.sendall(operation.encode())

            # Recebe o resultado do proxy reverso
            result = client_socket.recv(1024).decode()
            print(f"Resultado: {result}")

    except KeyboardInterrupt:
        print("\nCliente desconectado.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()