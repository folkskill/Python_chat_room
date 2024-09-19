import socket
from config import *
from method import debug_send
def test():
    # * 测试
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    while True:
        msg = input("message:")
        client_socket.send(msg.encode('utf-8'))
        if msg == 'q':
            client_socket.close()
            break
        recv_data = client_socket.recv(512)
        debug_send(recv_data.decode('utf-8'))
    client_socket.close()
if __name__ == "__main__":
    test()