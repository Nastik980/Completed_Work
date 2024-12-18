import socket
import threading

# --- Echo Server (easy) --- #
def echo_server(host="127.0.0.1", port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Echo server running on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)

# --- Multi-client Echo Server (medium) --- #
def handle_client(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Connection closed by {addr}")
                break
            conn.sendall(data)

def multi_client_echo_server(host="127.0.0.1", port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Multi-client echo server running on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

# --- File Server (medium/hard) --- #
def file_server(host="127.0.0.1", port=65433):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"File server running on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                with open("received_file.txt", "wb") as f:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        f.write(data)
                print("File received and saved as 'received_file.txt'")

# --- Echo Client (easy) --- #
def echo_client(host="127.0.0.1", port=65432, message="Hello, Server!"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode()}")

# --- File Client (medium) --- #
def file_client(host="127.0.0.1", port=65433, file_path="test_file.txt"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        with open(file_path, "rb") as f:
            while (data := f.read(1024)):
                client_socket.sendall(data)
    print(f"File '{file_path}' sent to the server")

# --- Main Application --- #
def main():
    print("Select mode:")
    print("1. Echo Server")
    print("2. Echo Client")
    print("3. Multi-client Echo Server")
    print("4. File Server")
    print("5. File Client")

    choice = input("Enter your choice: ")

    if choice == "1":
        echo_server()
    elif choice == "2":
        message = input("Enter message to send to the server: ")
        echo_client(message=message)
    elif choice == "3":
        multi_client_echo_server()
    elif choice == "4":
        file_server()
    elif choice == "5":
        file_path = input("Enter the path of the file to send: ")
        file_client(file_path=file_path)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
