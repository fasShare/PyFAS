from Epoll import Epoll
from Events import *
from Socket import Socket
from Handle import Handle
from EventLoop import EventLoop
from TcpServer import TcpServer

loop = EventLoop()
server = TcpServer(loop)
loop.loop()


