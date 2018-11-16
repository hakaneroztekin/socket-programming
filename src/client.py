import socket
import sys
import random
import queue
import datetime
from socket import *
from threading import Thread

buffer_capacity = 10240

def receive():
    while True:
        message = client_socket.recv(buffer_capacity).decode("utf8")
        print(message)
        if message == "exit":
            client_socket.close()
            break
        if not message:
            break




if __name__ == "__main__":
    serverHost = "127.0.0.1"
    serverPort = 1024
    address = (serverHost, serverPort)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(address)

    receive_thread = Thread(target=receive)
    send_thread = Thread(target=send)
    receive_thread.start()
    send_thread.start()
    receive_thread.join()
    send_thread.join()

