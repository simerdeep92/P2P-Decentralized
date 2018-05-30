# P2P-Decentralized
CSC 573 – Internet Protocols Project 
(Group - sjolly, ssingh25)
General Details:
The project is coded in Python 2.7.10 and requires a supported OS running this (or a compatible 2.x) Python version.

The directory consists of following files:
a.	server.py (centralized P2S Server implementation)
b.	peer.py  (a P2S Peer implementation with menu driven program to allow peer to make requests to server or other peers)
c.	request.py (Contains code to create and send requests to server or peer from a peer.)


Starting the Server:
Enter the following command on the command line window: 
> python server.py 			(starts the centralized P2S Server)

 

To kill the server, press 	"Ctrl+c"

Peer Application:
Enter the following command on the command line window: 
> python peer.py 		(start the peer with given command line options)

The above commands start the peer server to listen to a specific host and displays the information related to the system like ip address, os and port.
The following information appears and ask you to verify the version of the application to check if it is supported by other peers or server. 
 
	


The input of 1 is given and the following options appear for the peer:-

Choice 1. Add RFC to a peer :
This allows the peer to advertise about the RFCs available in its harddisk to the server. The request and response message is shown accordingly.
 

Choice 2. List all RFC from server:
Displays the RFC index maintained at server side.

 

Choice 3. Lookup for any RFC from centralized server:
Search for the RFC in the server as per the request of the peer.
 
 

Choice 4. Download RFC from another peer:
Lookup all the peers that have the RFC requested by the peer and asks user to enter source host details from where it wants to download the rfc file. The two figures below shows the get and the subsequent ADD request to download the file and update the RFC index of the server

 

 

Choice 6. Exit:
It disconnects the peer from the server deleting all the necessary information from the server. A customized END CONN request is added in P2S protocol to end the connection .The response prints all the RFC present in the server after deleting the RFCs of the disconnecting peer.
 
Error Messages:- 
1.	P2P-CI Version not Supported
If the version doesn’t matches Repose sends the ‘version not supported error’


2.	 File not found:
When the peer lookup for a RFC which is not present in the server file not found error is shown in the reponse to the peer.

 
3.	Bad Request:
If the server or peer encounters any other request other that mentioned in the protocol it responds with bad request error message.
 
