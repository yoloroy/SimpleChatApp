""" Script for TCP chat server - relays messages to all clients """

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

import ux_utils

clients = {}
addresses = {}

HOST = ux_utils.read_until_parsed_successfully("HOST: ", lambda ip: ip if ux_utils.is_ip(ip) else None)
PORT = ux_utils.read_until_parsed_successfully("PORT: ", int)
BUFSIZ = ux_utils.read_until_parsed_successfully("BUFSIZE: ", int)
ADDR = (HOST, PORT)
SOCK = socket(AF_INET, SOCK_STREAM)
SOCK.bind(ADDR)


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SOCK.accept()
        print(f"{client_address}:{client_address} has connected.")
        client.send("Greetings from the ChatRoom! ".encode("utf8"))
        client.send("Now type your name and press enter!".encode("utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client, client_address)).start()


def handle_client(conn, addr):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = conn.recv(BUFSIZ).decode("utf8")
    welcome = f'Welcome {name}! If you ever want to quit, type #quit to exit.'
    conn.send(bytes(welcome, "utf8"))
    msg = f"{name} from [{f'{addr[0]}:{addr[1]}'}] has joined the chat!"
    broadcast(bytes(msg, "utf8"))
    clients[conn] = name
    while True:
        msg = conn.recv(BUFSIZ)
        if msg != bytes("#quit", "utf8"):
            broadcast(msg, name + ": ")
        else:
            conn.send(bytes("#quit", "utf8"))
            conn.close()
            del clients[conn]
            broadcast(bytes(f"{name} has left the chat.", "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    SOCK.listen(5)  # Listens for 5 connections at max.
    print("Chat Server has Started !!")
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SOCK.close()
