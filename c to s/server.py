import socket
import threading
import asyncio
import sys
import select

RECEIVE_SIZE = 4096
IPADDR = sys.argv[1]
IPPORT = int(sys.argv[2])

print("socket now listening for connections.")

class ThreadSocketServer(object):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientConnections = {} # Key = port number, Val = socket object

    def __init__(self):
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((IPADDR, IPPORT))
        self.serverSocket.listen(5)

    def listenForConnections(self):
        while True:
            client, address = self.serverSocket.accept()
            client.settimeout(120)
            port = address[1]
            self.clientConnections[str(port)] = client
            print("\nadded connection " + str(address) + "\nServer >", flush=True)
            # upon connection, start listening for messages from client
            msgListenerThread = threading.Thread(target=self.listenForMessagesFromClient,args=(client,),daemon=True).start()

    def listenForMessagesFromClient(self, client):
        while True:
            message_received = client.recv(RECEIVE_SIZE)
            if message_received != b'':
                print(f'{client.getpeername()[1]} says {message_received.decode("utf-8")}', flush=True)

    def sendToClients(self, string):
        if string.startswith('@all'):
            for cl in self.clientConnections.values():
                cl.send(string.encode('utf-8'))
        else:
            try:
                port = string[1:string.index(' ')]
                try:
                    self.clientConnections[port].send(string.encode('utf-8'))
                except:
                    print(f'port {port} could not be found.')
            except:
                print("Enter '@all {message}' to address all clients.")
                print("Enter '@{port} {message}' to address a single client")
                print("Enter 'connections' to see all current clients.")
                print("Enter 'exitserver' to end this session.")

if __name__ == "__main__":
    server = ThreadSocketServer()
    connectionListenerThread = threading.Thread(target=server.listenForConnections, args=(), daemon=True).start()
    while True:
        messageToSend = input(f"Server >")
        if messageToSend == "exitserver":
            sys.exit()
        elif messageToSend == 'connections':
            for x, connection in enumerate(server.clientConnections):
                print(f'Connection #{x+1}:')
                print(server.clientConnections[connection].getpeername())
        else:
            server.sendToClients(messageToSend)
