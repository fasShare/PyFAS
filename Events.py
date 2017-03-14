from select import EPOLLERR
from select import EPOLLHUP
from select import EPOLLIN
from select import EPOLLOUT
from select import EPOLLPRI

kEevntRead = EPOLLIN | EPOLLPRI 
kEevntWrite = EPOLLOUT

class Events(object) :
	def __init__(self, fd, eventMask) : 
		self.fd_ = fd
		self.eventMask_ = eventMask


