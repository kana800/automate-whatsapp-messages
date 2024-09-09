from multiprocessing.connection import Client

if __name__ == "__main__":
    address = ('localhost', 6000)
    conn = Client(address, authkey=b'secretkey')

    while True:
        raw_input = input("type message: ")
        conn.send(raw_input)
        if raw_input == "quit":
            break
    conn.close()
