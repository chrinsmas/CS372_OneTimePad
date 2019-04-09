################################################################################
#CS 372 - Project 1
#file name: chatserver.py
#sources:
#	1. http://beej.us/guide/bgnet/output/html/singlepage/bgnet.html
#	2. http://www.linuxhowtos.org/C_C++/socket.htm
#	3. https://www.tutorialspoint.com/unix_sockets/client_server_model.htm
#	4. https://docs.python.org/2/howto/sockets.html
################################################################################

#!/bin/python
from socket import *
import sys

################################################################################
#def chat:
#Initiates a chart session with the client
#Lets them send the first messages
################################################################################
def chat(connection_socket, clientname, username):
    to_send = ""
    while 1:
        # continue chat until we break
        # get all of the characters from the user
        received = connection_socket.recv(501)[0:-1]
        # if we received nothing, print connection closed and close connection
        if received == "":
            print "Connection closed"
            print "Waiting for new connection"
            break
        # print the clients name with their message
        print "{}> {}".format(clientname, received)
        # grab input on our side to send to user
        to_send = ""
        while len(to_send) == 0 or len(to_send) > 500:
            to_send = raw_input("{}> ".format(username))
            # send it to the client if the message is not \quit
        if to_send == "\quit":
            print "Connection closed"
            print "Waiting for new connection"
            break
        connection_socket.send(to_send)

################################################################################
#def handshake:
#Exchanges usernames with the incoming connection
################################################################################

def handshake(connection_socket, username):
    # get the username
    clientname = connection_socket.recv(1024)
    # send username to the client
    connection_socket.send(username)
    return clientname

if __name__ == "__main__":
    # If the number of arguments is wrong, exit
    if len(sys.argv) != 2:
        print "You must specify the port number for the server to run"
        exit(1)
    # get the port number from the user and create a TCP socket
    serverport = sys.argv[1]
    serversocket = socket(AF_INET, SOCK_STREAM)
    # bind the socket to the port specified by the user
    serversocket.bind(('', int(serverport)))
    # listen on the port for incoming messages
    serversocket.listen(1)
    # ask the user for their name, must be less than 11 characters
    username = ""
    while len(username) == 0 or len(username) > 10:
        username = raw_input("Please enter a username of 10 characters or less: ")
        print "The server is ready to receive incoming messages"
    while 1:
        # keep doing this until signal interup
        # create a new socket if there is an incoming connection
        connection_socket, address = serversocket.accept()
        # print that we have received a connection
        print "received connection on address {}".format(address)
        # chat with the incoming connection, handshake with them first
        chat(connection_socket, handshake(connection_socket, username), username)
        # close the connection when we are done chatting
        connection_socket.close()
