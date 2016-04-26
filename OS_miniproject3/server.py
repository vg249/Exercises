import getopt
import socket
import sys
from threading import Thread, Lock, Condition


# Don't change 'host' and 'port' values below.  If you do, we will not be able to
# find your server when grading.
host = "127.0.0.1"
port = 8765
# Instead, you can pass command-line arguments
# -h/--host [IP] -p/--port [PORT]
# to put your server on a different IP/port.

class ConnectionHandler(Thread):
    """Handles a single client request"""

    def __init__(self, mailProcs,inbox):
	Thread.__init__(self)
	self.mailProc = mailProcs
	self.inboxObj = inbox
	self.clientname = ""
	self.fromadr = ""
	self.toadr  = []

    def handle(self):
	helo_success = 0
	mailfrom_success = 0 
	mailrcpt_success = 0
	data_success = 0
	self.socket.send("220 vg249 SMTP CS4410MP3".encode('utf-8'))
	self.socket.settimeout(10) 
	
	try:
		while helo_success == 0:
			self.clientname = ""
			self.fromadr = ""
			self.toadr  = []
			temp = self.read_line(self.socket) 
	 		helo_success = self.handle_helo(temp)
		if helo_success == 1:
		 	self.socket.send("250 vg249".encode('utf-8'))
		 	self.socket.settimeout(10) 
			while mailfrom_success == 0:
	 			mailfrom_success = self.handle_mailfrom(self.read_line(self.socket))
			if mailfrom_success == 1:
		 		self.socket.send("250.2.1.0 OK".encode('utf-8'))
		 		self.socket.settimeout(10) 
				while mailrcpt_success == 0:
	 				mailrcpt_success = self.handle_rcptto(self.read_line(self.socket))
				if(mailrcpt_success == 1):
		 			self.socket.send("250.2.1.5 OK".encode('utf-8'))
		 			self.socket.settimeout(10) 
					nextmsg = self.read_line(self.socket) 
					while(self.nextDataCmd(nextmsg) == 0):
	 					mailrcpt_success = self.handle_rcptto(nextmsg)
						if mailrcpt_success == 1:
		 					self.socket.send("250.2.1.5 OK".encode('utf-8'))
		 					self.socket.settimeout(10) 
						nextmsg = self.read_line(self.socket) 
					while(data_success == 0):
						data_success = self.handle_data(nextmsg)
						nxtmsg = self.read_line(self.socket) 
					if data_success == 1:
		 				self.socket.send("354 End data with <CR><LF>.<CR><LF>".encode('utf-8'))
		 				self.socket.settimeout(10)
						self.inboxObj.inboxWrite(self.clientname,self.fromadr,self.toadr,self.read_data(self.socket))
		 				self.socket.send("250 OK: Delivered {} messages".format(1).encode('utf-8'))	
		 				self.socket.settimeout(10) 
	except socket.timeout:
		self.socket.send("421 4.4.2 netid Error: timeout exceeded".encode('utf-8'))	

    def handle_helo(self,msg):
	msg_variables = msg.split()
	if len(msg_variables) > 0:
		if msg_variables[0].upper() == "HELO":
			if len(msg_variables) != 2:
	 			self.socket.send("501 Syntax: HELO yourhostname".encode('utf-8'))
				return 0
			self.clientname = msg_variables[1]
			return 1
		else:
	 		self.socket.send("502 5.5.2 Error: HELO not recognized".encode('utf-8'))
			return 0
	else:
	 	self.socket.send("502 5.5.2 Error: HELO not recognized".encode('utf-8'))
		return 0
	
    def nextDataCmd(self,msg):
	nxtmsgsplt = msg.split()
	if len(nxtmsgsplt) > 0:
		if nxtmsgsplt[0].strip().upper() == "DATA":
			return 1
		else:
			return 0
	else:
		return 0						
	   
    def handle_mailfrom(self,msg):
	msg_variables = msg.split()
	if len(msg_variables) < 1:
		self.socket.send("502 5.5.2 Error: MAIL FROM not recognized".encode('utf-8'))
		return 0

	if msg_variables[0].upper() == "HELO":
	 	self.socket.send("503 Error: duplicate HELO".encode('utf-8'))
		return 0

	if msg_variables[0].upper() == "DATA":
	 	self.socket.send("503 Error: need MAIL FROM command".encode('utf-8'))
		return 0
	
	if len(msg_variables) < 2:
		self.socket.send("502 5.5.2 Error: MAIL FROM not recognized".encode('utf-8'))
		return 0
	
	if msg_variables[0].upper() == "MAIL" and msg_variables[1].upper() == "FROM:":
		if len(msg_variables) > 3:
			mailarg = msg.strip().split(" ",1)
			fromarg = mailarg[1].strip().split(" ",1)
	 		self.socket.send(('504 5.5.2 {}: Sender address rejected'.format(fromarg[1])).encode('utf-8'))
			return 0
		elif len(msg_variables) < 3:
	 		self.socket.send(('501 syntax: MAIL FROM: youremailaddress').encode('utf-8'))
			return 0
		else:	
			self.fromadr = msg_variables[2]
			return 1
	else:
		if msg_variables[0].upper() == "RCPT" and msg_variables[1].upper() == "TO:":
	 		self.socket.send("503 Error: need MAIL FROM command".encode('utf-8'))
			return 0
	 	self.socket.send("502 5.5.2 Error: MAIL FROM not recognized".encode('utf-8'))
		return 0
	return 0

    def handle_rcptto(self,msg):
	msg_variables = msg.split()
	if len(msg_variables) < 1:
		self.socket.send("502 5.5.2 Error: RCPT TO not recognized".encode('utf-8'))
		return 0

	if msg_variables[0].upper() == "HELO":
	 	self.socket.send("503 Error: duplicate HELO".encode('utf-8'))
		return 0

	if msg_variables[0].upper() == "DATA":
	 	self.socket.send("503 Error: need RCPT TO command".encode('utf-8'))
		return 0
	
	if len(msg_variables) < 2:
		self.socket.send("502 5.5.2 Error: RCPT TO not recognized".encode('utf-8'))
		return 0
	
	if msg_variables[0].upper() == "RCPT" and msg_variables[1].upper() == "TO:":
		if len(msg_variables) > 3:
			mailarg = msg.strip().split(" ",1)
			fromarg = mailarg[1].strip().split(" ",1)
	 		self.socket.send(('504 5.5.2 %s: recipient address invalid'%fromarg[1]).encode('utf-8'))
			return 0
		elif len(msg_variables) < 3:
	 		self.socket.send(('501 syntax: RCPT TO: youremailaddress').encode('utf-8'))
			return 0	
		else:
			self.toadr.append(msg_variables[2])
			return 1
	else:
		if msg_variables[0].upper() == "MAIL" and msg_variables[1].upper() == "FROM:":
	 		self.socket.send("503 5.5.1 Error: nested MAIL command".encode('utf-8'))
			return 0
	 	self.socket.send("502 5.5.2 Error: RCPT TO not recognized".encode('utf-8'))
		return 0
	return 0

    def handle_data(self,msg):
	msg_variables = msg.split()
	if len(msg_variables) != 1:	
	 	self.socket.send("501 DATA".encode('utf-8'))
		return 0
	elif msg_variables[0] == "DATA":
		return 1
	else:
	 	self.socket.send("501 DATA".encode('utf-8'))
		return 0    		

    def read_line(self,sock):
        chars = []
        while True:
            a = sock.recv(1)
	    if a == "\r":
		a = sock.recv(1) 
		if a == "\n":
                	return "".join(chars)
            chars.append(a)  
    
    def read_data(self,sock):
        lines = []
        while True:
            line = self.read_line(sock)
            if line == ".":
        	return "\n".join(lines)
	    else:
            	lines.append(line)
    

    def run(self):
	while True:
		try:
			self.socket = self.mailProc._Conn_Process()
			self.handle()
		except socket.timeout:
			self.socket.send("421 4.4.2 netid Error: timeout exceeded".encode('utf-8'))	
			self.socket.close()
class ThreadPool:
	def __init__(self,maxConn):
		self.connLock = Lock()
		self.connAvailable = Condition(self.connLock)
		self.mailProcess  = Condition(self.connLock)
		self.maxCon = maxConn
		self.numConns = 0
		self.count_msg = 0
		self.sockList = []
		
	def _Conn_Ready(self, socket):
		with self.connLock:
			while self.numConns >= self.maxCon:
				self.connAvailable.wait()
			self.sockList.append(socket)
			self.numConns += 1
			self.mailProcess.notifyAll()

	def _Conn_Process(self):
		with self.connLock:
			while self.numConns == 0:
				self.mailProcess.wait()
			socket = self.sockList.pop()
			self.numConns -= 1
			self.connAvailable.notifyAll()
			return socket

class BackupThread(Thread):
    def __init__(self,inboxThr):
	Thread.__init__(self)
	self.target = inboxThr
   
    def run(self):
	while True:
		self.target.backup()

class inbox:
    def __init__(self):
	self.msgcount = 0
	self.inboxLock = Lock()			    
	self.backupCount = 0	
	self.messageQue = []	
	self.messageID = 0
	
    def inboxWrite(self,clientname,From,to,msg):
	with self.inboxLock:
		self.messageID += 1
		inboxMsg = "Received from {}\n ID : {} \n From : {}\n".format(clientname,self.messageID,From)
		inboxMsg += "To : {}\n".format(",".join(to))
		inboxMsg += msg
   		self.messageQue.append(inboxMsg)
 
    def backup(self):
	with self.inboxLock:
		while(len(self.messageQue) > 0 and self.msgcount < 32):
			inboxMsg = self.messageQue.pop()
			inboxFile = open("mailbox","a+")
			inboxFile.write(inboxMsg)
			inboxFile.close()
			self.msgcount += 1
			if self.msgcount >= 32:
				backupFile = "mailbox.{} - {}".format((self.backupCount*32)+1,(self.backupCount*32)+32)
				self.backupCount += 1
				self.msgcount -= 32
		 		with open(backupfile,'w') as dest, open("mailbox",'r+') as src:
                			for line in src:
                    				dest.write(line)
				inboxFile = open("mailbox","w+")
				inboxFile.close()
		
def serverloop():
    """The main server loop"""

    mailProcs = ThreadPool(32)

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # mark the socket so we can rebind quickly to this port number
    # after the socket is closed
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind the socket to the local loopback IP address and special port
    serversocket.bind((host, port))
    # start listening with a backlog of 5 connections
    serversocket.listen(5)
	
    inboxObj = inbox()
    bkpThread = BackupThread(inboxObj).start()

    for _ in range(32):
	ConnectionHandler(mailProcs,inboxObj).start()

    while True:
        # accept a connection
        (clientsocket, address) = serversocket.accept()
        mailProcs._Conn_Ready(clientsocket)

# DO NOT CHANGE BELOW THIS LINE

opts, args = getopt.getopt(sys.argv[1:], 'h:p:', ['host=', 'port='])

for k, v in opts:
    if k in ('-h', '--host'):
        host = v
    if k in ('-p', '--port'):
        port = int(v)

print("Server coming up on %s:%i" % (host, port))
serverloop()
