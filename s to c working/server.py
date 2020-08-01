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
    clientConnections = {} 
    # I changed this list to a dict so I could directly access the socket objects by their ports

    def __init__(self):
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((IPADDR, IPPORT))
        self.serverSocket.listen(5)

    def listen(self):
        while True:
            client, address = self.serverSocket.accept()
            client.settimeout(120)
            port = address[1]
            self.clientConnections[str(port)] = client
            # self.clientConnections.append(client)
            print("\nadded connection " + str(address) + "\nServer >", flush=True)

            # for client in self.clientConnections.values():
            #     message_received = self.serverSocket.recv(RECEIVE_SIZE)
            #     print(f'{client.getpeername()[1]} says {message_received.decode("utf-8")}')
                


    # To send to all clients: '@all {message}
    # To send to one client '@{port} {message}'
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
                    print(f'port {port} could not be found...')
            except:
                print("Enter '@all {message}' to address all clients.")
                print("Enter '@{port} {message}' to address a single client")
                print("Enter 'connections' to see all current clients.")
                print("Enter 'exitserver' to end this session.")

if __name__ == "__main__":
    server = ThreadSocketServer()
    listenThread = threading.Thread(target=server.listen, args=(), daemon=True).start()
    while True:
        messageToSend = input(f"Server >")
        if messageToSend == "exitserver":
            sys.exit()
        elif messageToSend == 'connections':# for debugging purposes
            for x, connection in enumerate(server.clientConnections):
                print(f'Connection #{x+1}:')
                print(server.clientConnections[connection].getpeername())
        else:
            server.sendToClients(messageToSend)