

class Buffer(object) :
	def __init__(self) :
		self.initSize_ = 100
		self.buffer_ = bytearray(self.initSize_)
		self.readStartIndex_ = 0
		self.writeStartIndex_ = 0
	
	def insertToBuffer(self, index, data) :
		

	def extend(self, data) :
		length = len(data)
		if (self.writeStartIndex_ < self.readStartIndex_) :
			if (self.writeStartIndex_ + length) < self.readStartIndex_ :
				self.buffer_.replace(old, new)