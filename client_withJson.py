import socket
import threading
import json

from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.shortcuts import message_dialog

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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


def send_message(nickname):
    connected = True
    while connected:
        message = f'{nickname}:{input("")}'
        if message == f'{nickname}:!EXIT':
            connected = False
            client.close()
        else:
            client.send(message.encode(FORMAT))


def send_nickname():
    nickname = input_dialog(
        title='My nickname',
        text='Enter your nickname:').run()

    client.send(nickname.encode(FORMAT))
    return nickname


def connection_succeed():
    nickname = send_nickname()

    receive_message_thread = threading.Thread(target=receive_message)
    receive_message_thread.start()

    send_message_thread = threading.Thread(target=send_message, args=(nickname,))
    send_message_thread.start()


def validate_user_credentials(user, password):
    try:
        if password == users[user]:
            print("nice")
        else:
            print("incorrect")
    except KeyError:
        print("incorrect")


def sign_in():
    try:
        username = input_dialog(
            title='Username',
            text='Enter the username of the room:').run()
        password = input_dialog(
            title='Password',
            text='Enter the password of the room:').run()
        if password != users[username]:
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


def get_users_from_db():
    with open('db.json', 'r') as file:
        return json.load(file)


users = get_users_from_db()
sign_in()
