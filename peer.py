#!/usr/bin/env python
from request import *
import os,threading,platform


#To check peer to peer manually ip was given as the domain is not public
ip_details = {'simerish-pc':'10.139.65.55','sud-pc':'10.139.71.0' }
global peer_version
global status_phrases
global peer_port
global peer_host_name

status_phrases = {200:'OK',400:'Bad Request',404:'Not Found',505:'P2P-CI Version Not Supported'}

#Decodes the request received from another peer
def decode_message(message):
    split_message = message.split()
    os = ''.join(split_message[6:])
    status_code = 0
    rfc_n = None
    if (split_message[0] == 'GET'):
        if(split_message[2] == peer_version):
            rfc_n = split_message[1]
        else: status_code = 505
        # print split_message
    else:
        status_code = 400
    return form_response_message(status_code,os,host = split_message[4],rfc = rfc_n)

#Creates the Response message for Download
def form_response_message(status_code,hostos,host,rfc):

    if status_code == 0:
        file_addr = 'rfc' + rfc +'.txt'
        if not os.path.isfile(file_addr):
            status_code = 404
        else:

            # print os.listdir(peer_directory[host])
            with open(file_addr, 'r') as myfile:
                data = myfile.read().replace('\n', '')
            status_code = 200
            message = str(peer_version + ' ' + str(status_code) + ' ' + status_phrases[int(status_code)] + '\r\n' + \
                          'Date: ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\r\n' + \
                          'OS: ' + hostos + '\r\n' + \
                          'Last-Modified: ' + str(time.ctime(os.path.getmtime(file_addr))) + '\r\n' + \
                          'Content-Length: ' + str(os.path.getsize(file_addr)) + '\r\n' + \
                          'Content-Type: ' + str(content_type) + '\r\n' +
                          data
                          )

        if status_code != 200:
            message = str(peer_version + ' ' + str(status_code) + ' ' + status_phrases[status_code] + '\r\n')

    return message

#Creates peer listen server for receiving request from another peers
def start_listen():

    listen_socket.listen(5)
    while 1:
        (peer_socket, (peer_ip, peer_port)) = listen_socket.accept()
        # print("Client1:" + str(peer_ip) + "/" + str(peer_port))
        while 1:

            data = peer_socket.recv(200000)
            # print data
            if not data: break
            # print "Response:\n", str(data)
            response_data = decode_message(str(data))
            # server_response = self.format_message(rfc_response_list,200)
            peer_socket.send(response_data)  # echo

#Initial Configuration of the software
print "Welcome To P2P TCP Version 1 \nCSC-573"
server_ip = '10.139.65.55'
server_port = 7734
peer_ip = socket.gethostbyname(socket.gethostname())
print "IP address of this machine is : " + peer_ip
peer_host_name = socket.gethostname() #  raw_input("Enter Host name of this machine: ")
print "Host Name of this machine is :" + peer_host_name
print "Connecting to P2P CI Server"
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.bind(('',0))
peer_port = listen_socket.getsockname()[1]
listen_thread = threading.Thread(target = start_listen)
listen_thread.start()
print "Listening port of this machine: " + str(peer_port)
peer_os = platform.system()
print "Operating System of this machine: "+ str(peer_os)
print peer_host_name + " is connected to the P2P System"
global content_type
content_type = 'text/text'

# Menu to drive the program
while(1):
        peer_version = raw_input("Press 1 if peer uses P2P-CI/1.0 else press 0")
        if peer_version == '0':
            peer_version = raw_input("Enter Version")
            break;
        elif peer_version == '1':
            peer_version = 'P2P-CI/1.0'
            break
while(1):

    print "\n1.Add RFC to a peer"
    print "2.List all RFC from centralize server"
    print "3.Lookup for any RFC in centralized server"
    print "4.Download RFC from 1 peer to another"
    print "5.Create BAD request"
    print "6.Exit"
    choice_input = raw_input("Input what you want to do ?")
    if(choice_input == '1'):
        print "Add new RFC to peer(automatically adds the peer if not exists)\n"
        # peer_host_name = raw_input("Enter Peer Host to which you want to add rfc:")
        # peer_port = raw_input("Enter Peer Upload Port:")


        number_of_rfc =int(raw_input("Number of RFCs do you want to add:"))
        rfc = [['','']]*number_of_rfc
        for i in range(number_of_rfc):
            print "RFC "+ str(i+1) + ':'
            rfc[i][0] = raw_input("Enter Rfc number:")
            rfc[i][1] = raw_input("Enter Rfc Title:")
            server_request = Request_P2S(method = 'ADD',rfc = rfc[i][0],version = peer_version,host = peer_host_name,title = rfc[i][1],port = peer_port)
            response = server_request.send_request(server_ip,server_port)
            print "Response :\n" + str(response)
    elif(choice_input == '2'):
        server_request = Request_P2S(method = 'LIST',rfc = None,version = 'P2P-CI/1.0',host = peer_host_name, title = None,port = peer_port)
        response = server_request.send_request(server_ip,server_port)
        print "Response :\n" + str(response)

    elif choice_input == '3':
        rfc_number = raw_input("Enter RfC number:")
        rfc_title = raw_input("Enter Rfc Title:")
        server_request = Request_P2S(method = 'LOOKUP',rfc = rfc_number,version = peer_version,host = peer_host_name,title = rfc_title,port = peer_port)
        response = server_request.send_request(server_ip,server_port)
        print "Response :\n" + str(response)

    elif choice_input == '4':

        rfc_number = raw_input("Enter Rfc number:")
        rfc_title = raw_input("Enter Rfc Title:")
        server_request = Request_P2S(method = 'LOOKUP',rfc = rfc_number,version = peer_version,host = peer_host_name,title = rfc_title,port = peer_port)
        response = server_request.send_request(server_ip,server_port)
        print "Response :\n" + str(response)
        length_to_check = len(response.split("\r\n"))
        if(length_to_check > 3):
            source_host_name = raw_input("Enter Source Host of the peer from where to download: ")
            source_port  = raw_input("Enter Source Port of the peer from where to download: ")
            # source_ip = raw_input("Enter IP address of the peer from where to download: ")

            #source_ip -- Can be hardcoded if the hosts are not having any public domain.
            #Download from another peer

            p2p_response_success = 0
            try:
                #source_ip = socket.gethostbyname(source_host_name)
                source_ip = ip_details[source_host_name]
                server_request = Request_P2P(method='GET',rfc = rfc_number,version = peer_version,host = source_host_name, os=peer_os)
                file_data = server_request.send_request(source_ip,int(source_port))
                p2p_response_success = 1
            except socket.error, exc:
                print "Connection error : %s" % exc
            file_present = 0
            if p2p_response_success == 1:
                #Save into disk
                file_addr = 'rfc' + rfc_number +'.txt'
                if os.path.isfile(file_addr):
                    os.remove(file_addr)
                    file_present =  1

                outfile = open(file_addr,'w+')
                outfile.seek(0)
                outfile.write(str(file_data))
                outfile.close()
                # ADD to rfc index

                if file_present == 0:
                    server_request = Request_P2S(method = 'ADD',rfc = rfc_number,version = peer_version,host = peer_host_name,title = rfc_title,port = peer_port)
                    server_request.send_request(server_ip,server_port)
            else :
                print "P2P Download Failed"
        else:
            print "The RFC is not available"
    elif choice_input == '5':
        server_request = Request_P2S(method = 'BAD',rfc = '11233', version = peer_version,host = peer_host_name,title = 'bad',port = peer_port)
        response = server_request.send_request(server_ip,server_port)
        print "Response :\n" + str(response)
    elif choice_input == '6':
        ## server request to delete entries of that peer
        server_request = Request_P2S(method = 'END',rfc = None,version = peer_version,host = peer_host_name,title = None ,port = peer_port)
        response = server_request.send_request(server_ip,server_port)
        print "Response :\n" + str(response)
        ## Stop  the listening port of the peer
        print "The Connection to P2P is closed"
        listen_thread.join()
        listen_socket.close()
        break;
    else:
        print "Bad Input"
  
