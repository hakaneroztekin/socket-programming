# Computer Communications Homework I
# Hakan Eröztekin
# 150130113
# 3.10.18

import socket
import sys
import asyncore
from _thread import start_new_thread
from threading import Thread
import datetime
import collections
import logging
import socket

class Server():
    is_first_connection = True
    clients = {}
    addresses = {}

    def __init__(self, serverPort):
        try:
            # Creating a socket
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # An IPv4 TCP socket
            print("Socket created")
        except:
            print("Socket is failed to create")
            exit(1)

        try:
            self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except:
            print("Socket is already in use")
            exit(1)

        try:
            # Bind the socket to the serverPort
            self.serverSocket.bind((serverHost, serverPort))
            print("Socked binded to host: ", serverHost, " port:", serverPort)
        except:
            print("Binding failed")
            exit(1)

        try:
            # Listen the incoming connections
            self.serverSocket.listen(100)  # listen up to 100 requests
            print("Socket is listening")
        except:
            print("Server is failed to listen")
            exit(1)

        print("Server is ready")
        self.listen()

    def listen(self):
        ACCEPT_THREAD = Thread(target=self.accept_new_connections())
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()

    def accept_new_connections(self):
        while True:
            client, address = self.serverSocket.accept()
            print("A new connection established", address)
            client.send(bytes("Welcome! What's your username?", "utf8"))
            self.addresses[client] = address
            Thread(target=self.listen_to_client, args=(client, address)).start()

    def listen_to_client(self, client, address, buffer_capacity = 10240):
        if self.is_first_connection:
            username = self.get_message(client)
            print("Client with address", address, "picked a new username: ", username)

        message = "%s joined the chat" % username


        self.clients[client] = username
        self.broadcast(address, bytes(message, "utf8"))

        while True:
            try:
                message = self.get_message(client)
            except:
                print("Message decode failed")
                exit(1)


#            try:
            if message == "exit":
                client.close()
                print("Connection to ", username, " is closed at ", datetime.datetime.now())
                del self.clients[client]
                break

            else:
                user_message = username + " at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") \
                               + " says: " + message
                print(user_message)
                self.broadcast(address, bytes(user_message, "utf8"))

    def broadcast(self, clientaddr, message, prefix=""):
        for sock in self.clients:
            if sock.getpeername() != clientaddr: # broadcast except the sender
                sock.send(bytes(prefix, "utf8") + message)

    def get_message(self, connection, buffer_capacity = 10240):
        received_message = connection.recv(buffer_capacity)
        received_message_size = sys.getsizeof(received_message)

        if received_message_size > buffer_capacity:
            print("The message is too large {}".format(received_message_size))

        decoded_message = received_message.decode("utf8").rstrip()

        return decoded_message

if __name__ == "__main__":
    serverHost = "127.0.0.1"
    serverPort = 1024
    Server(serverPort)