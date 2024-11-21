import socket

if __name__ == "__main__":
    address = ('localhost', 8000)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)

    while True:
        msg = input("Enter message: ")
        client.send(msg.encode("utf-8")[:1024])

        if msg.lower() == "close":
            break

    client.close()
    print("Connection to server closed")
