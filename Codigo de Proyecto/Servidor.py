import socket
import threading

clients = []

def handle_client(client_socket, client_address):
    print(f"[+] Nueva conexión de {client_address}")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"[{client_address}] {message}")
                broadcast(message, client_socket)
            else:
                break
        except:
            break

    print(f"[-] {client_address} se ha desconectado.")
    clients.remove(client_socket)
    client_socket.close()

def broadcast(message, current_client):
    for client in clients:
        if client != current_client:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5555))
    server.listen(2)
    print("[*] Esperando conexiones...")

    while True:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    start_server()