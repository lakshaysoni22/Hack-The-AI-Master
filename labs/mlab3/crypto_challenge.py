import socket
import threading
import base64

FLAG = "flag{b4s364_1s_n0t_3ncrypt10n}"

def handle_client(client_socket):
    try:
        client_socket.send(b"Welcome to the Crypto Challenge!\n")
        client_socket.send(b"Can you decode this secret message?\n\n")
        
        encoded_flag = base64.b64encode(FLAG.encode()).decode()
        client_socket.send(f"Secret: {encoded_flag}\n\n".encode())
        
        client_socket.send(b"Enter the decoded flag: ")
        response = client_socket.recv(1024).decode().strip()
        
        if response == FLAG:
            client_socket.send(b"\nCongratulations! You have captured the flag!\n")
        else:
            client_socket.send(b"\nIncorrect. Try again.\n")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Crypto challenge server listening on port 9999...")
    
    while True:
        client, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == '__main__':
    main()
