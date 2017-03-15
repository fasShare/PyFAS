from Socket import Socket
from socket import error
import errno
from socket import fromfd
from Events import kEevntRead
from Events import kEevntWrite
from Events import Events
from Handle import Handle
from Socket import socketDefaultType
from Socket import socketDefaultFamily
from DefaultCallback import defMessageCallback


class TcpConnection(object) :
	def __init__(self, loop, socket, peeraddr) :
		self.loop_ = loop
		self.socket_ = Socket(socket)
		self.peeraddr_ = peeraddr
		self.events_ = Events(self.socket_.getSocketFd(), kEevntRead)
		self.handle_ = Handle(self.events_)
		self.recvBuffer_ = []
		self.writeBuffer_ = []
		self.messageCb_ = defMessageCallback

	
	def tcpConnectionHandRead(self, reventFd, reventMask) :
		assert reventFd == self.socket_.getSocketFd()
		
		length = 30
		while True:
			try :
				data = self.socket_.recv(length)
			except error, e :
				if e.errno == errno.EAGAIN :
					print "no enough data!"
					break
			print type(data)
			self.recvBuffer_.extend(data)
			if len(data) == 0 :
				self.loop_.delHandle(self.handle_)
				self.recvBuffer_ = []
				break
		print self.recvBuffer_

	def connectionInit(self) :
		self.handle_.setReadCb(self.tcpConnectionHandRead)
		
		self.loop_.addHandle(self.handle_)

	def setMessageCallback(self, messagecb) :
		self.messageCb_ = messagecb