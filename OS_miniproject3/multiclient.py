#!/usr/bin/python
import socket
from threading import Thread
import random
import datetime
import time

# TODO: Implement the multi-threaded client here.
# This program should be able to run with no arguments
# and should connect to "127.0.0.1" on port 8765.  It
# should run approximately 1000 operations, and be extremely likely to
# encounter all error conditions described in the README.

port = 8765
host = "127.0.0.1"
fromaddr = ["1@2.com", "3@4.com", "5@6.com","7@8.com","   ddd@ddd","dd ddd"]
toaddr = ["100@20.com", "me@menobody.com", "world@worl.com","mmm mmm"]
#toaddr = ["mmm m mm"]
helo   = ["Helo","Helo", "  he   lo  "," helo "," helo","heLo", "HeLo"]
mailfrom   = ["MAIL FROM:","m ail from","Mail From:"]
recptto   = ["RCPT TO:","m ail from","RCPT :","rcpt to:","MAIL FROM:"]


def send(socket, message):
    # In Python 3, must convert message to bytes explicitly.
    # In Python 2, this does not affect the message.
    socket.send(message.encode('utf-8'))

def send_clients(thread):
    for i in range(1,100):	
	 msgid = (thread*i)
	 try:
    		sender = random.choice(fromaddr)
    		receiver = random.choice(toaddr)
    		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    		s.connect((host, port))
    		reply = s.recv(500)
		print(reply)
    		nextCommand = "Helo"
		while True:
		 	 if nextCommand == "newscket":
		    		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		    		s.connect((host, port))
		    		nextCommand = "Helo"
			 elif nextCommand == "Helo":
			 	heloVar  = random.choice(helo)
		   	 	send(s, "{} thread{}\r\n".format(heloVar,thread).encode('utf-8'))
		   	 	reply = s.recv(500)
				print(reply)
				if reply.find("250") != -1:
					nextCommand = "mailfrom"
				elif reply.find("421") != -1:
					s.close()
					nextCommand = "newscket"
			 elif nextCommand == "mailfrom":
		    		sender = random.choice(fromaddr)
		    		mailfrmcmd = random.choice(mailfrom)
		   	 	send(s, "{} {}\r\n".format(mailfrmcmd,sender))
		   	 	reply = s.recv(500)
				print(reply)
				if reply.find("250") != -1:
					nextCommand = "rcptto"
				elif reply.find("421") != -1:
					s.close()
					nextCommand = "newscket"
			 elif nextCommand == "rcptto":
		    		receiver = random.choice(toaddr)
		    		rcpttomcmd = random.choice(recptto)
		   	 	send(s, "{} {}\r\n".format(rcpttomcmd,receiver))
		   	 	reply = s.recv(500)
				print(reply)
				if reply.find("250") != -1:
					nextCommand = "data"
				elif reply.find("421") != -1:
					s.close()
					nextCommand = "newscket"
			 elif nextCommand == "data":
		   	 	send(s, "DATA\r\n"
		   	 	        "From: {}\r\n"
		   	 	        "To: {}\r\n"
		   	 	        "Date: {} -0500\r\n"
		   	 	        "Subject: msg {}\r\n\r\n"
		   	 	        "Contents of message {} end here.\r\n"
		   	 	        ".\r\n".format(sender, receiver,
		   	 	                       datetime.datetime.now().ctime(),
		   	 	                       msgid, msgid))
		   	 	reply = s.recv(500)
				print(reply)
				if reply.find("354") != -1:
					nextCommand = "final"
				elif reply.find("421") != -1:
					s.close()
					nextCommand = "newscket"
			 else:
		   	 	reply = s.recv(500)
				print(reply)
				if reply.find("250") != -1:
					s.close()
					nextCommand = "newscket"
					i += 1
					break
				elif reply.find("421") != -1:
					s.close()
					nextCommand = "newscket"
	 except:
		s.close()
		nextCommand = "newscket"
		print("Connection Error")
	
for threadid in range(1, 32):
    thread = Thread(target=send_clients, args=(threadid,))
    thread.start()


