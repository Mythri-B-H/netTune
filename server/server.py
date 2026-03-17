import socket
import threading
import os

# Server configuration
HOST = "0.0.0.0"   # Accept connections from any device
PORT = 5000

# Folder where songs are stored
SONG_FOLDER = "./songs"


# Function to handle each client
def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")

    try:
        # Get list of songs
        songs = os.listdir(SONG_FOLDER)

        if not songs:
            conn.send("No songs available".encode())
            conn.close()
            return

        # Send song list to client
        song_list = "\n".join([f"{i+1}. {song}" for i, song in enumerate(songs)])
        conn.send(song_list.encode())

        # Receive client choice
        choice = conn.recv(1024).decode()
        choice = int(choice) - 1

        if choice < 0 or choice >= len(songs):
            conn.send("Invalid choice".encode())
            conn.close()
            return

        selected_song = songs[choice]
        file_path = os.path.join(SONG_FOLDER, selected_song)

        print(f"[STREAMING] {selected_song} to {addr}")

        # Open and stream file
        with open(file_path, "rb") as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                conn.sendall(data)

        print(f"[DONE] {selected_song} sent to {addr}")

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr}")


# Start server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[STARTED] Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()

        # Create new thread for each client
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()