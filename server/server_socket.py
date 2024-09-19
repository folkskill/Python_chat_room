import socket
from config import *
class ServerSocket(socket.socket):
    """服务器"""

    def __init__(self) -> None:
        # * 初始化套接字(tcp)
        super(ServerSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)

        #  绑定地址与端口号
        self.bind((server_ip, server_port))

        # 监听数量设置
        self.listen(MAX_USER)