import socket
import threading

from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.shortcuts import message_dialog

# Defining the chat server settings so the client can connect to the server
# and make a format I would like to use for encoding/decoding.
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# Defining TCP and IP for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Defining the chatroom username and password so only
# those who know them can join the chat server
chatroom_username = 'chatroom'
chatroom_password = '12345678'


# Function that responsible to print message that the rest of the server is sending
# and if something unexpected happens the client will close connection with the server.
def receive_message():
    connected = True
    while connected:
        try:
            message = client.recv(1024).decode(FORMAT)
            print(message)
        except:
            print("Exiting...")
            client.close()
            break


# Function that responsible to send message that the client would like to send
# to the rest of the server and letting the client option to exit the chat by typing !EXIT.
# If the user cant send message probably the chat closed so we will print "Server closed"
# and break the loop.
def send_message(nickname):
    connected = True
    while connected:
        try:
            message = f'{nickname}:{input("")}'
            if message == f'{nickname}:!EXIT':
                connected = False
                client.close()
            else:
                client.send(message.encode(FORMAT))
        except:
            print("Server closed")
            break


# Function that responsible to send the nickname that the server is asking for
# so everybody will know who sending the message.
def send_nickname():
    nickname = input_dialog(
        title='My nickname',
        text='Enter your nickname:').run()

    client.send(nickname.encode(FORMAT))
    return nickname


# If connection succeeded we will send the nickname from send_nickname function
# and then start 2 threads that will work at the same time, one responsible to
# receive message from the chat and one responsible to send message to the chat.
def connection_succeed():
    nickname = send_nickname()

    receive_message_thread = threading.Thread(target=receive_message)
    receive_message_thread.start()

    send_message_thread = threading.Thread(target=send_message, args=(nickname,))
    send_message_thread.start()


# Sign in function will ensure that the one who wants to connect to the chat
# is allowed by check username and password of the chat.
def sign_in():
    try:
        username = input_dialog(
            title='Username',
            text='Enter the username of the room:').run()
        password = input_dialog(
            title='Password',
            text='Enter the password of the room:').run()
        if username.lower() != chatroom_username or password != chatroom_password:
            message_dialog(
                title='Connection failed',
                text='Sorry, the username or the password is incorrect').run()
            sign_in()
        else:
            try:
                client.connect(ADDR)
                connection_succeed()
            except:
                print("Connection failed")
    except:
        print("Canceled")


# starting by sign in.
sign_in()
