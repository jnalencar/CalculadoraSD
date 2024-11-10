import socket
import threading
import json

# Lista de servidores de cálculo
# Lista de servidores de cálculo com portas de status e cálculo
servers = [
    {'status': ('localhost', 6000), 'calc': ('localhost', 6001)},
    {'status': ('localhost', 6002), 'calc': ('localhost', 6003)},
    {'status': ('localhost', 6004), 'calc': ('localhost', 6005)}
]

def get_server_load(server):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server['status'])  # Conecta à porta de status
        s.sendall(b'LOAD')
        load = s.recv(1024).decode()
        s.close()
        return float(load)
    except:
        return float('inf')

def handle_client(client_socket):
    try:
        while True:
            # Recebe a operação do cliente
            operation = client_socket.recv(1024).decode()
            if not operation:
                break  # Cliente fechou a conexão

            # Seleciona o servidor com menor carga
            server_loads = [(server, get_server_load(server)) for server in servers]
            selected_server = min(server_loads, key=lambda x: x[1])[0]

            # Conecta ao servidor na porta de cálculo
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect(selected_server['calc'])  # Conecta à porta de cálculo
            server_socket.sendall(operation.encode())

            # Recebe o resultado do servidor
            result = server_socket.recv(1024).decode()
            server_socket.close()

            # Envia o resultado de volta para o cliente
            client_socket.sendall(result.encode())
    except Exception as e:
        print(f"Erro ao processar a requisição: {e}")
    finally:
        client_socket.close()

def main():
    # Configurações do proxy reverso
    proxy_host = 'localhost'
    proxy_port = 5000

    # Criação do socket do proxy reverso
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((proxy_host, proxy_port))
    proxy_socket.listen(5)
    print(f"Proxy reverso escutando em {proxy_host}:{proxy_port}")

    try:
        while True:
            # Aceita uma nova conexão do cliente
            client_socket, addr = proxy_socket.accept()
            print(f"Conexão aceita de {addr}")

            # Cria uma nova thread para lidar com a requisição do cliente
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nProxy reverso desligado.")
    finally:
        proxy_socket.close()

if __name__ == "__main__":
    main()