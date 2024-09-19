from config import *

class SocketWapper(object):
    """套接字包装类"""

    def __init__(self, sock) -> None:
        self.sock = sock

    def recv_data(self) -> str:
        '''接收数据并解码字符串'''
        return self.sock.recv(MAX_BYTE).decode('utf-8')
    
    def send_data(self, message:str) -> str:
        '''发送数据并解码字符串'''
        try:
            return self.sock.send(message.encode('utf-8'))
        except:
            return ""

    def close(self):
        '''关闭套接字'''
        self.sock.close()