import socket
import threading
import psutil
import time

def handle_status(client_socket):
    try:
        data = client_socket.recv(1024).decode()
        if data == 'LOAD':
            # Obtém a carga atual da CPU
            cpu_load = psutil.cpu_percent(interval=1)
            client_socket.sendall(str(cpu_load).encode())
    finally:
        client_socket.close()

def handle_calculation(client_socket):
    try:
        operation = client_socket.recv(1024).decode()
        # Processa a operação matemática
        result = str(eval(operation))
        client_socket.sendall(result.encode())
    except Exception as e:
        client_socket.sendall(f"Erro: {e}".encode())
    finally:
        client_socket.close()

def start_status_server(host, port):
    status_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status_socket.bind((host, port))
    status_socket.listen(5)
    print(f"Servidor de Status escutando em {host}:{port}")
    while True:
        client_socket, addr = status_socket.accept()
        threading.Thread(target=handle_status, args=(client_socket,)).start()

def start_calculator_server(host, port):
    calc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    calc_socket.bind((host, port))
    calc_socket.listen(5)
    print(f"Servidor de Calculadora escutando em {host}:{port}")
    while True:
        client_socket, addr = calc_socket.accept()
        threading.Thread(target=handle_calculation, args=(client_socket,)).start()

def main():
    host = 'localhost'
    status_port = 6002  # Porta de Status
    calc_port = 6003    # Porta de Serviço de Calculadora

    # Cria as threads dos servidores
    status_thread = threading.Thread(target=start_status_server, args=(host, status_port))
    calc_thread = threading.Thread(target=start_calculator_server, args=(host, calc_port))

    # Inicia as threads
    status_thread.start()
    calc_thread.start()

    # Aguarda as threads terminarem
    status_thread.join()
    calc_thread.join()

if __name__ == "__main__":
    main()