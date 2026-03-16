import socket
import threading

HOST = "0.0.0.0"
PORT = 5000


def handle_client(conn, addr):
    print(f"Client connected: {addr}")

    while True:
        try:
            data = conn.recv(1024).decode()

            if not data:
                break

            print("Received:", data)

            conn.send("Server received command\n".encode())

        except:
            break

    conn.close()
    print("Client disconnected")


def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print("🎵 Music Streaming Server Started on port", PORT)

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()