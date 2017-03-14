from select import epoll
from Events import Events

class Epoll (object) :
	def __init__(self) :
		self.epoll_ = epoll()

	def addEventFd(self, events) :
		assert type(events) == Events
		try :
			self.epoll_.register(events.fd_, events.eventMask_)
		except IOError:
			return False
		
		return True


	def modEventFd(self, events) :
		assert type(events) == Events
		self.epoll_.modify(events.fd_, events.eventMask_)

	def delEventFd(self, events) :
		assert type(events) == Events
		self.epoll_.unregister(events.fd_)

	def polling(self, timeout = -1, maxevents = 20) :
		return self.epoll_.poll(timeout, maxevents)

	def __del__(self) :
		self.epoll_.close()

