import socket
import errno 
from socket import AF_INET
from socket import AF_INET6
from socket import SOCK_DGRAM
from socket import SOCK_STREAM

socketDefaultFamily = AF_INET
socketDefaultType = SOCK_STREAM

class Socket(object) : 
	def __init__(self, sock = socket.socket(AF_INET, SOCK_STREAM, 0)) :
		self.socket_ = sock
		#FIXME : closeExec
		self.socket_.setblocking(False)

	def bind(self, address = ('127.0.0.1', 8890)) : 
		self.socket_.bind(address)

	def recv(self, length) :
		return self.socket_.recv(length)

	def accept(self) : 
		client = self.socket_.accept()
		client[0].setblocking(False)
		return client

	def listen(self, backlog) :
		self.socket_.listen(backlog)

	def getAddr(self) :
		return self.socket_.getsockname()

	def getPeerAddr(self) :
	    return self.socket_.getpeername()

	def getSocketFd(self) :
		return self.socket_.fileno()

	def close(self) :
		self.socket_.close()

