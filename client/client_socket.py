from socket import socket,AF_INET,SOCK_STREAM
from config import *
class ClientSocket(socket):
    """客户端套接字的自定义处理"""

    def __init__(self):
        super(ClientSocket, self).__init__(AF_INET, SOCK_STREAM)
        
    def connect(self):
        '''客户端连接服务器'''
        super(ClientSocket, self).connect((server_ip, server_port))
        
    def recv_data(self):
        '''接收数据并解码字符串'''
        return self.recv(MAX_BYTE).decode('utf-8')
    
    def send_data(self, message:str):
        '''发送数据并解码字符串'''
        return self.send(message.encode('utf-8'))