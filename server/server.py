from server_socket import ServerSocket
from socket_wapper import SocketWapper
from response_protocoi import *
from method import debug_send
from threading import Thread
from json import load,dump
from config import *

class Server():
    """服务器核心类"""

    def __init__(self) -> None:
        # * 创建服务器套接字
        self.server_socket = ServerSocket()

        # 创建与事件相关联函数的字典
        self.request_dict = {
            REQUEST_CHAT : self.request_chat_handle,
            REQUEST_LOGIN : self.request_login_handle,
            REQUEST_SIGNUP : self.request_signup_handle
        }

        # 创建保存当前登陆用户的字典
        self.clients = {}

    def startup(self):
        '''获取客户端连接，对其提供服务'''
        while True:
            # *获取客户端连接
            debug_send("正在获取客户端连接...")
            soc, addr = self.server_socket.accept()
            debug_send("获取到客户端连接!")

            # *使用套接字生成包装对象
            client_soc = SocketWapper(soc)

            thread = Thread(target = lambda:self.request_handle(client_soc))
            thread.start()

    def request_handle(self, client_soc:SocketWapper):
        '''处理客户端请求'''
        while True:
            # * 收发消息
            try:
                msg = client_soc.recv_data()
                if not msg or msg == 'q':
                    # * 没有数据就应该是客户端已经关闭了,或者用户指定退出
                    self.remove_offline_user(client_soc)
                    break
                else:
                    debug_send(f"服务器收到原始消息:{msg}")
                
                # 解析数据
                parse_data:str = self.parse_request_text(msg)

                # 分析请求类型，并根据请求类型调用相应的处理函数
                func:function = self.request_dict.get(parse_data["request_id"]) #? 用get防报错
                if func : func(client_soc, parse_data)

            except ConnectionResetError:break

        self.remove_offline_user(client_soc)

    def remove_offline_user(self, client_soc:SocketWapper):
        '''客户端下线之后的处理'''
        for username, info in self.clients.items():
            if info['sock'] == client_soc:
                del self.clients[username]
                debug_send(f"用户\'{username}\'离开了服务器")
                # 找到下线用户就没必要再找了
                break
        client_soc.close()

    def parse_request_text(self, data:str):
        '''
        解析客户端发来的数据
        :登录信息：0001/username/password
        :聊天信息：0002/username/message
        '''
        data_list = data.split(DELLMITER)
        # * 按照类型解析数据
        request_data = {}
        request_data["request_id"] = data_list[0]

        if request_data["request_id"] == REQUEST_LOGIN:
            # 用户请求登录
            request_data["username"] = data_list[1]
            request_data["password"] = data_list[2]

        elif request_data["request_id"] == REQUEST_CHAT:
            # 用户请求聊天
            request_data["username"] = data_list[1]
            request_data["messages"] = data_list[2]

        elif request_data["request_id"] == REQUEST_SIGNUP:
            # 用户请求注册
            request_data["username"] = data_list[1]
            request_data["password"] = data_list[2]
            
        return request_data
    
    def request_login_handle(self, client_soc:SocketWapper, request_data:dict):
        '''处理客户端登录'''
        debug_send(f"收到客户端<登录>请求,正在处理响应...")
        # 获取到账号密码
        username = request_data["username"]
        password = request_data["password"]

        # 检查是否能够登录
        result, nickname, username = self.check_user_login(username, password)

        # 如果登陆成功则需要保存当前用户
        if result:
            self.clients[username] = {"sock": client_soc,
                                      "nickname": nickname}
            for u_name, info in self.clients.items():
                sock:SocketWapper = info['sock']
                sock.send_data(f"用户\'{username}\'加入了服务器!")
        else:
            # 如果登陆失败,就将数据隐藏
            nickname = ''
            if username == None:
                # 数据库没有这个账户的信息
                username = ''

        # 拼接返回给客户端的消息
        response_text = ResponseProtocol.response_login_result(str(result), nickname, username)

        # 把结果消息发送给客户端
        client_soc.send_data(response_text)

    def request_signup_handle(self, client_soc:SocketWapper, request_data:dict):
        '''处理注册功能'''
        data:dict = {}
        result:int = 1
        username = request_data['username']
        password = request_data['password']
        with open('server/data/user_data.json','r',encoding = 'utf-8') as f:
            data = load(f)

        if username in data:
            # 是否有重名用户
            result = 0
            username = ''

        if len(password) <= MINNEST_PASSWORD:
            # 密码长度检测
            result = 0
            password = ''

        response_text = ResponseProtocol.response_signup(username, password, str(result))

        if not result:
            # 若失败，提前结束，不录入json
            client_soc.send_data(response_text)
            return
        
        # 录入json
        data[username] = {
            "permissions": "user",
            "nickname": username,
            "password": password
        }
        with open('server/data/user_data.json', 'w', encoding = 'utf-8') as f:
            # 录入文件
            dump(data, f, indent = 2)

        # 返回结果消息
        client_soc.send_data(response_text)

    def request_chat_handle(self, client_soc:SocketWapper, request_data:dict):
        '''处理聊天功能'''
        debug_send(f"收到客户端<聊天>请求,正在处理响应...")
        # 获取消息内容
        username = request_data["username"]
        messages = request_data["messages"]
        nickname = self.clients[username]["nickname"]

        # 拼接发送给客户端的消息文本
        msg = ResponseProtocol.response_chat(nickname, messages)

        # 把消息转发给每一个在线用户
        for u_name, info in self.clients.items():
            sock:SocketWapper = info['sock']
            sock.send_data(msg)

    def check_user_login(self, username, password):
        '''检查登录是否成功,并返回结果'''
        # 打开并读取 JSON 文件
        with open('server/data/user_data.json', 'r') as j:
            data:dict = load(j)

        # 开始检测有没有这个用户
        if username in data:
            # 如果有，就检测ta的密码是否正确
            if data[username]["password"] == password:
                # 密码与用户名符合，登陆成功
                return(1, data[username]["nickname"], username)
            else:
                # 有这个用户，但是密码不符合
                return(0, None, username)
        else:
            # 一个没有注册过的新用户
            return(0, None, None)

if __name__ == "__main__":
    Server().startup()
