from Socket import Socket
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
		self.recvBuffer = []
		self.writeBuffer = []
		self.messageCb_ = defMessageCallback

	
	def tcpConnectionHandRead(self, reventFd, reventMask) :
		sockfd = fromfd(reventFd, socketDefaultFamily, socketDefaultType)
		length = 30
		while True:
			data = []
			data = self.socket_.recv(length)
			self.recvBuffer.extend(data)
			if len(data) == 0 :
				#FIXME : call close callback
				self.loop_.delHandle(self.handle_)
				break;
			if len(data) < length :
				break;

		self.messageCb_(self.recvbuffer)

	def connectionInit(self) :
		self.handle_.setReadCb(self.tcpConnectionHandRead)
		
		self.loop_.addHandle(self.handle_)

	def setMessageCallback(self, messagecb) :
		self.messageCb_ = messagecb