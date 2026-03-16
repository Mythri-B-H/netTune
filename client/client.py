import socket

HOST = "127.0.0.1"   # server IP
PORT = 5000

BUFFER_SIZE = 4096


def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("Connected to music server")
    return client


def list_songs(client):
    client.send("LIST\n".encode())

    data = client.recv(4096).decode()
    print("\nAvailable Songs:")
    print(data)


def play_song(client):

    song = input("Enter song name: ")

    command = f"PLAY {song}\n"
    client.send(command.encode())

    file = open("received_song.mp3", "wb")

    print("Receiving stream...")

    while True:

        data = client.recv(BUFFER_SIZE)

        if b"STREAM_END" in data:
            break

        file.write(data)

    file.close()

    print("Song saved as received_song.mp3")


def main():

    client = connect_to_server()

    while True:

        print("\n------ MENU ------")
        print("1. List songs")
        print("2. Play song")
        print("3. Quit")

        choice = input("Enter choice: ")

        if choice == "1":
            list_songs(client)

        elif choice == "2":
            play_song(client)

        elif choice == "3":
            client.send("QUIT\n".encode())
            break

        else:
            print("Invalid choice")

    client.close()


if __name__ == "__main__":
    main()