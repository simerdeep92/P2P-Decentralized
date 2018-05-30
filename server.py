#!/usr/bin/env python
import socket

import threading
from time import gmtime, strftime
import os.path, time

status_phrases = {200: 'OK', 400: 'Bad Request', 404: 'Not Found', 505: 'P2P-CI Version Not Supported'}
# List that contains the active peers (hostname,portnumber)
active_peers = {}
# List to index RFCs available at each peer(RFC number,title of RFC,hostname of peer)
rfc_peers = []

# default settings for RFC text files directory and contect type for easy understanding
peer_directory = {'peer1': 'peer 1', 'peer2': 'peer 2'}
content_type = 'text/text'
version = 'P2P-CI/1.0'

## Handles Active clients by spawing new client into separate thread
class Peer(threading.Thread):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        while 1:
            data = self.client.recv(2000000)
            if not data: break
            # print "Response:\n", str(data)
            rfc_response_list,status_code = self.decode_message(str(data), self.client)
            server_response = self.format_message(rfc_response_list, status_code)
            self.client.send(server_response)  # echo

    # Parse the message request received by the server
    def decode_message(self, message, peer_socket):
        split_message = message.split()
        peer_version = split_message[2]
        if peer_version == version:
            print split_message
            peer_host_name = split_message[4]
            rfc_response_list = []
            status_code = 0
            # ADD
            if split_message[0][0:3] == 'ADD':
                peer_port = split_message[6]
                rfc_number = split_message[1]
                rfc_title = ' '.join(split_message[8:])
                # if the peer is new or inactive add to new peers
                # Add new peer to the active peer list
                active_peers[peer_host_name] = peer_port
                    #newpeer.join()
                # if peer to rfc record is not available
                if [rfc_number, peer_host_name] not in [[rfc[0],rfc[2]] for rfc in rfc_peers]:
                    rfc_peers.append([rfc_number, rfc_title, peer_host_name])
                    rfc_response_list.append([rfc_number, rfc_title, peer_host_name])
                else:
                    status_code = 400
            # LIST ALL
            elif split_message[0][0:4] == 'LIST':
                rfc_response_list = rfc_peers
            # LOOKUP
            elif split_message[0] == 'LOOKUP':
                lookup_rfc = split_message[1]
                rfc_response_list = [rfc for rfc in rfc_peers if rfc[0] == lookup_rfc ]
                if len(rfc_response_list) == 0:
                    status_code = 404
            elif split_message[0] == 'END':
                peer_host_name = split_message[4]
                for rfc in rfc_peers:
                    if rfc[2] == peer_host_name:
                        rfc_peers.remove(rfc)
                del active_peers[peer_host_name]
                rfc_response_list = rfc_peers
            else :
                rfc_response_list = []
                status_code = 400

            if status_code == 0:
                status_code = 200
            print (active_peers)
            print (rfc_peers)
        else :
            rfc_response_list = []
            status_code = 505
        return rfc_response_list,status_code

    # Format the message
    def format_message(self, rfc_response_list, status_code):
        response = str(version + ' ' + str(status_code) + ' ' + status_phrases[status_code] + '\r\n' + '\r\n')
        for rfc in rfc_response_list:
            # print rfc
            response = response + ' '.join(rfc) + ' ' + str(active_peers[rfc[2]]) + '\r\n'
        return response



class Server():
    # Create TCP socket for server till it is up and running
    def __init__(self, ip, port, version='P2P Version 1'):
        self.server_ip = ''
        self.server_port = port
        self.version = version
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start()

    def start(self):
        # Bind ip and port to socket and start listening from clients
        self.server_socket.bind((self.server_ip, self.server_port))

        self.server_socket.listen(5)
        # Listen to client and fork the process for it
        while 1:
            # (peer_socket, (peer_ip, peer_port)) = self.server_socket.accept()
            # # print("Client:" + str(peer_ip) + "/" + str(peer_port))
            p = Peer(self.server_socket.accept())
            p.start()

#Starts the serrver
print ("The TCP server is started")
tcpserver = Server('',7734,'P2P-CI/1.0')
