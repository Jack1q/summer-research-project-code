import socket
import sys
import threading

RECIEVE_SIZE = 4096
IP = sys.argv[1]
PORT = int(sys.argv[2])

class ThreadSocketClient(object):

    # Create a socket
    # socket.AF_INET - using IPv4
    # socket.SOCK_STREAM - uses TCP sockets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.client_socket.connect((IP, PORT))
        print("connected and listening to server.")

    def sendToServer(self, msg):
        self.client_socket.send(msg.encode('utf-8'))

    def listenToServer(self):
        while True:
            messageToGet = self.client_socket.recv(RECIEVE_SIZE)
            if messageToGet == b'':
                self.client_socket.close()
                print("Server closed")
                sys.exit()
            else:
                print("Server said: " + messageToGet.decode('utf-8'), flush=True)

if __name__ == "__main__":
    client = ThreadSocketClient()
    listen_thread = threading.Thread(target=client.listenToServer,args=(),daemon=True).start()
    while True:
        msg = input('Client >')
        client.sendToServer(msg)


