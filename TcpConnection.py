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
		self.recvBuffer_ = ''
		self.writeBuffer_ = ''
		self.messageCb_ = defMessageCallback

	def tcpConnectionHandRead(self, reventFd, reventMask) :
		assert reventFd == self.socket_.getSocketFd()
		data = ''
		length = 30
		while True:
			try :
				data = self.socket_.recv(length)
			except error, e :
				if e.errno == errno.EAGAIN :
					break
			if len(data) == 0 :
				self.loop_.delHandle(self.handle_)
				self.recvBuffer_ = ''
				break
			else :
				self.recvBuffer_ += data
		if len(self.recvBuffer_) != 0 :
			self.messageCb_(self, self.recvBuffer_)
			self.recvBuffer_ = ''

	def sendMsg(self, msg) :
		self.writeBuffer_ += msg
		self.handle_.addEventMask(kEevntWrite)
		self.loop_.modHandle(self.handle_)

	def handleWrite(self, reventFd, reventMask) :
		assert reventFd == self.socket_.getSocketFd()
		ret = 0
		try : 
			ret = self.socket_.send(self.writeBuffer_)
		except socket.error, e :
			if e.errno == errno.ECONNRESET :
				self.loop_.delHandle(self.handle_)

		print "sent %d bytes data!", ret
		if (ret < len(self.writeBuffer_)) :
			self.writeBuffer_ = self.writeBuffer_[ret:]
		else :
			self.writeBuffer_ = ''
			self.handle_.delEventMask(kEevntWrite)
			self.loop_.modHandle(self.handle_)
		
	def connectionInit(self) :
		self.handle_.setReadCb(self.tcpConnectionHandRead)
		self.handle_.setWriteCb(self.handleWrite)
		self.loop_.addHandle(self.handle_)

	def setMessageCallback(self, messagecb) :
		self.messageCb_ = messagecb