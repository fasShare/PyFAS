from Events import *
from enum import Enum


def defreadcb(reventFd, reventMask) :
	print "defreadcb"

def defwritecb(reventFd, reventMask) :
	print "defwritecb"

def deferrorcb(reventFd, reventMask) :
	print "deferrorcb"

def defclosecb(reventFd, reventMask) :
	print "defclosecb"



class Handle(object):
	class STATE(Enum) :
		ADD = 1
		MOD = 2
		DEL = 3
		LOOP = 4
	def __init__(self, events, readcb = defreadcb, writecb = defwritecb, errorcb = deferrorcb, closecb = defclosecb):
		assert type(events) == Events
		self.events_ = events
		self.readcb_ = readcb
		self.writecb_ = writecb
		self.errorcb_ = errorcb
		self.closecb_ = closecb
		self.state = Handle.STATE.ADD

	def setEvents(self, events) :
		assert type(events) == Events
		self.events_ = events

	def getEvents(self) :
		return self.events_

	def getEventFd(self) :
		return self.events_.fd_
	def getEventMask(self) : 
		return self.events_.eventMask_

	def setReadCb(self, readcb) :
		self.readcb_ = readcb

	def setWriteCb(self, writecb) :
		self.writecb_ = writecb

	def setErrorCb(self, errorcb) :
		self.errorcb_ = errorcb

	def setCloseCb(self, closecb) :
		self.closecb_ = closecb

	def handEvent(self, reventFd, reventMask) :
		if (reventMask | EPOLLIN) or (reventMask | EPOLLPRI) or (reventMask | EPOLLHUP) :
			self.readcb_(reventFd, reventMask)
		elif (reventMask | EPOLLOUT) :
			self.writecb_(reventFd, reventMask)
		elif (reventMask | POLLERR) :
			self.errorcb_(reventFd, reventMask)
		elif (reventMask | EPOLLHUP) and (not(reventMask | EPOLLIN)) :
			self.closecb_(reventFd, reventMask)
		else :
			print "handle no event!"
