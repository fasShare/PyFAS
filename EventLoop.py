from Epoll import *
from Events import *
from Socket import *
from Handle import Handle

class EventLoop(object):

	def __init__(self):
		self.poller_ = Epoll()
		self.pollTimeOut_ = -1
		self.maxEvents_ = 20
		self.handles_ = {}
		self.newHandles_ = {}


	def addHandle(self, handle) :
		assert type(handle) == Handle
		assert handle.state == Handle.STATE.ADD
		self.newHandles_[handle.getEventFd()] = handle

	def delHandle(self, handle) :
		assert type(handle) == Handle
		assert self.handles_.has_key(handle.getEventFd())
		handle.state = Handle.STATE.DEL
		self.newHandles_[handle.getEventFd()] = handle
 
	def modHandle(self, handle) :
		assert type(handle) == Handle
		assert self.handles_.has_key(handle.getEventFd())
		handle.state = Handle.STATE.MOD	
		self.newHandles_[handle.getEventFd()] = handle	

	def updateHandles(self) :
		for item in self.newHandles_.keys(): 
			#FIXME : according to the state of handle.
			newhandle = self.newHandles_[item]
			newevents = newhandle.getEvents()
			newkey = newhandle.getEventFd()
			newstate = newhandle.state

			if newstate == Handle.STATE.ADD :
				self.poller_.addEventFd(newevents)
				newhandle.state = Handle.STATE.LOOP
				self.handles_[newkey] = newhandle
			elif newstate == Handle.STATE.DEL :
				self.poller_.delEventFd(newevents)
				self.handles_.pop(newhandle.getEventFd())
			elif newstate == Handle.STATE.MOD :
				self.poller_.modEventFd(newevents)
				newhandle.state = Handle.STATE.LOOP
				self.handles_[newkey] = newhandle
			else :
				assert False
		
		self.newHandles_.clear()

	def loop(self) :
		quit = True
		while quit :
			self.updateHandles()	

			revents = self.poller_.polling(self.pollTimeOut_, self.maxEvents_)
			for reventsItem in revents :
				self.handles_[reventsItem[0]].handEvent(reventsItem[0], reventsItem[1])

			del revents


