import socket
import threading

# Defining the server settings and format I would like to use for encoding/decoding.
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'


# Defining that the server is using IPv4 and TCP packets and
# binding it with the port and server.
# then listening on this server and port.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()


# Defining the clients list and nicknames list
clients = []
nicknames = []


# Function that handling the client who has connected to the server which
# means to receive every message he sent and send it to the rest of the chat.
# if something unexpected happened with the client we will remove him from
# the list of clients and the list of nicknames, and let everybody know that he left.
def handle(client):
    connected = True
    while connected:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast(f"{nickname} has left the chat!".encode(FORMAT))
            nicknames.remove(nickname)
            break


# Broadcasting the message that we receive from client to the
# server and to the rest of the chat.
def broadcast(message):
    print(message.decode(FORMAT))
    for client in clients:
        client.send(message)


# Getting the nickname of the client that just joined the chat.
# Adding the nickname to the nicknames list, and letting to the
# rest of the chat know that new client has joined.
def getNick(client):
    nickname = client.recv(1024).decode(FORMAT)
    nicknames.append(nickname)
    broadcast(f"{nickname} joined the chat!".encode(FORMAT))


# Receiving a new client that just succeeded to join the chat and print his
# address to the server, we will add him to the client list and make a thread
# that will send the client to handle function.
def receive_client():
    listening = True
    while listening:
        client, address = server.accept()
        print(f"{address} is connected to the server")

        clients.append(client)
        getNick(client)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# after server starts continue with receiving client loop to the chat
print("[SERVER IS LISTENING]")
receive_client()
