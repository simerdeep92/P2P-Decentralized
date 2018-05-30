#!/usr/bin/env python
import socket
from time import gmtime, strftime
import os.path, time,thread
status_phrases = {200:'OK',400:'Bad Request',404:'Not Found',505:'P2P-CI Version Not Supported'}
content_type = 'text/text'

class Request_P2S():
    #create object of server request given the inputs
    def __init__(self,method,rfc,version,host,title,port):
        self.method = method
        self.rfc = rfc
        self.version = version
        self.host = host
        self.port = 0
        self.title = title
        self.listen_port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Bind ip and port to socket and start listening from other peerss
        self.s.bind(('',self.port))
        self.port = self.s.getsockname()[1]

    #Sends the request to server
    def send_request(self,send_to_ip,send_to_port):
        self.s.connect((send_to_ip, send_to_port))
        m = self.form_request_message()
        self.s.send(m)
        data =  self.s.recv(1024)
        self.s.close
        # print ("Response: \n" + data)
        return data


    #Creates the request message
    def form_request_message(self):
        if self.method == 'LIST':
            message = str(self.method + ' ALL ' + self.version +  '\r\n' +
                   'Host: ' + self.host  + '\r\n' +
                   'Port: ' + str(self.listen_port)  + '\r\n' +
                   '\r\n'
                   )
        elif self.method == 'END':
            message = str(self.method + ' CONN ' + self.version +  '\r\n' +
                   'Host: ' + self.host  + '\r\n' +
                   'Port: ' + str(self.listen_port)  + '\r\n' +
                   '\r\n'
                   )
        else :
            message = str(self.method + ' ' + self.rfc + ' ' + self.version +  '\r\n' +
                   'Host: ' + self.host  + '\r\n' +
                   'Port: ' + str(self.listen_port)  + '\r\n' +
                   'Title: ' + self.title	+ '\r\n'
                   '\r\n'
                    )
        print ("Request: \r\n" + message)
        return message


class Request_P2P:

    #create object of P2P request given the inputs
    def __init__(self,method,rfc,version,host,os):
        self.method = method
        self.rfc = rfc
        self.version = version
        self.host = host
        self.os = os

    #Sends the request to peer
    def send_request(self,send_to_ip,send_to_port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((send_to_ip, send_to_port))
        print self.form_request_message()
        s.send(self.form_request_message())
        data = s.recv(2000000)
        # print 11111
        # s.close
        print "Response:\n" + str(data)
        data1 = data.split('\r\n')
        return data1[-1]

    #Creates the request message
    def form_request_message(self):
        message = str(self.method + ' ' + self.rfc + ' ' + self.version +  '\r\n' +
                   'Host: ' + self.host  + '\r\n' +
                   'OS: ' + self.os	+ '\r\n'
                   '\r\n'
                    )
        return message

    pass
