from multiprocessing.connection import Listener

def getmessageinformation(msg):
    """
    summary: separates the message
    and the sender and return in a 
    tuple
    """
    msg = msg.lstrip().rstrip()
    if msg[:4] != "send":
        print("send keyword isn't found\nusage: send <message> to:<name>")
        return (None, None)
    content = msg[4:].lstrip().rstrip()
    to_index = content.rfind("to:") 
    if to_index == -1:
        print("to keyword isn't found\nusage: send <message> to:<name>")
        return (None, None)
    username = content[to_index:].split('to:')[1]
    return (content[:to_index].rstrip(), username)

if __name__ == "__main__":
    address = ('localhost', 6000)
    listener = Listener(address, authkey=b'secretkey')
    conn = listener.accept()
    while True:
        msg = conn.recv()
        if msg == 'close':
            conn.close()
            break
        (message, username) = getmessageinformation(msg)
        print(f"user: {username} message: {message}")
    conn.close()
