
def defMessageCallback(tcpConn, recvbuffer) :
	#FIXME : read message!
	print recvbuffer
	tcpConn.sendMsg(recvbuffer) 