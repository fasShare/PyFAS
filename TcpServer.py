from Socket import Socket 
from Events import Events
from Events import kEevntRead
from Handle import Handle
from TcpConnection import TcpConnection

from DefaultCallback import defMessageCallback

class TcpServer(object):
	def __init__(self, loop):
		self.loop_ = loop
		self.serversd_ = Socket()
		self.serversd_.bind()
		self.serversd_.listen(100)
		self.conns_ = {}
		self.events_ = Events(self.serversd_.getSocketFd(), kEevntRead)
		self.handle_ = Handle(self.events_, self.serverReadCb)
		self.loop_.addHandle(self.handle_)
		self.messageCb_ = defMessageCallback

	def initNewConn(self, acceptRet) :
		print "initNewConn"
		client = acceptRet[0]
		peeraddr = acceptRet[1]
		
		conn = TcpConnection(self.loop_, client, peeraddr) 
		conn.setMessageCallback(self.messageCb_)

		conn.connectionInit()

		self.conns_[client.fileno()] = conn 

	def setMessageCallback(self, messagecb = defMessageCallback) :
		self.messageCb_ = messagecb

	def serverReadCb(self, reventFd, reventMask) :
		print "serverReadCb"
		assert reventFd == self.serversd_.getSocketFd()

		#(socket object, address info)
		newconn = self.serversd_.accept()
		self.initNewConn(newconn)