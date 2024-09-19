from request_protocol import RequestProtocol
from tkinter.messagebox import showinfo
from client_socket import ClientSocket
from window_signup import WindowSignUp
from window_login import WindowLogin
from window_chat import WindowChat
from method import debug_send
from threading import Thread
from sys import exit
from config import *

class Client(object):

    def __init__(self) -> None:
        '''初始化客户端的资源'''
        # 初始化登录窗口
        self.window_login = WindowLogin()
        self.window_login.on_reset_button_click(lambda:self.window_login.clear_entry())
        self.window_login.on_login_button_click(lambda:self.send_login_data())
        self.window_login.on_window_close(lambda:self.exit())

        self.data:dict[str:str] = {}
        self.active = True

        # 初始化聊天窗口
        self.window_chat = WindowChat()
        self.window_chat.withdraw() # 隐藏窗口
        self.window_chat.on_send_button_click(lambda:self.send_chat_data())

        # 初始化注册窗口
        self.window_signup = WindowSignUp()
        self.window_signup.withdraw() # 隐藏窗口
        self.window_signup.on_signup_button_click(lambda:self.signup_user())
        self.window_signup.on_reset_button_click(lambda:self.window_signup.clear_entry())

        # 创建客户端套接字
        self.conn = ClientSocket()

        # 创建与id对应的事件字典
        self.response_dict = {
            RESPONSE_LOGIN_RESULT : self.response_login_handle,
            RESPONSE_CHAT : self.response_chat_handle,
            RESPONSE_SIGNUP : self.response_signup_handle
        }


    def startup(self):
        '''开启窗口'''
        self.conn.connect()
        Thread(target = lambda:self.response_handle()).start()
        self.window_login.mainloop()

    def send_login_data(self):
        '''发送登录信息'''
        # 获取到账号密码及用户名
        self.window_login.get_data()
        password = self.window_login.password
        username = self.window_login.username

        # 生成协议文本
        request_text = RequestProtocol.request_login_result(username, password)

        # 发送协议文本到服务器
        self.conn.send_data(request_text)

    def send_chat_data(self):
        '''获取聊天输入框内容并发送到服务器'''
        # 获取输入
        message = self.window_chat.get_inputs()
        self.window_chat.clear_input()

        # 拼接协议文本
        request_text = RequestProtocol.request_chat(self.data['username'], message)

        # 发送消息内容
        if message == '':
            showinfo(f"{TITLE}:{DEFECT_HINT}", "不能发送空白内容!")
            return
        self.conn.send_data(request_text)

    def response_handle(self):
        '''不断地接受服务器的新消息并处理'''
        while self.active:
            # 接收服务器发来的消息
            recv_data = self.conn.recv_data()
            debug_send(recv_data)

            # 对服务器发来的消息进行解析
            response_data:dict = __class__.parse_response_data(recv_data)

            # 根据消息分别进行处理
            func = self.response_dict.get(response_data['response_id'])
            if func : func(response_data)

    @staticmethod
    def parse_response_data(recv_data:str):
        '''
        解析服务器的消息
        :登陆或是聊天响应
        '''
        # 使用协议约定的符号来切割消息
        response_data_list = recv_data.split(DELLMITER)
        
        # 解析消息的各个组成部分
        response_data = {}
        response_data['response_id'] = response_data_list[0]

        if response_data['response_id'] == RESPONSE_LOGIN_RESULT:
            # 用户登陆结果的响应
            response_data['result'] = response_data_list[1]
            response_data['nickname'] = response_data_list[2]
            response_data['username'] = response_data_list[3]
        
        elif response_data['response_id'] == RESPONSE_CHAT:
            # 聊天消息的响应
            response_data['nickname'] = response_data_list[1]
            response_data['message'] = response_data_list[2]

        elif response_data['response_id'] == RESPONSE_SIGNUP:
            # 注册消息的响应
            response_data['username'] = response_data_list[1]
            response_data['password'] = response_data_list[2]
            response_data['result'] = response_data_list[3]

        return response_data
    
    def show_signup_window(self):
        '''显示注册窗口'''
        self.window_login.withdraw()
        self.window_signup.deiconify()

    def show_login_window(self):
        '''显示登录窗口'''
        self.window_signup.withdraw()
        self.window_login.deiconify()
    
    def response_login_handle(self, response_data:dict):
        '''接收到登录结果之后的操作'''
        result = response_data['result']
        if result == '0':
            error_hint = ""
            if response_data['username'] == '':
                error_hint = "不存在此用户。"
            else:error_hint = "密码输入错误。"
            showinfo(f"{TITLE}:{DEFECT_HINT}",f"登录失败,因为{error_hint}")
            debug_send(f"登录失败,因为{error_hint}")
            self.show_signup_window()
            return
        
        # 登陆成功之后
        debug_send("登陆成功!正在获取信息...")
        nickname:str = response_data['nickname']
        username:str = response_data['username']
        self.data = {# 对数据进行保存
            'username' : username,
            'nickname' : nickname
        }
        debug_send(f"昵称为\'{nickname}\'的用户\'{username}\'登录成功!")
        showinfo(f"{TITLE}:{SUCCESS_HINT}",f"登陆成功! 您的当前昵称为\'{nickname}\'。")

        # 显示聊天窗口,隐藏登录窗口
        self.window_login.withdraw()
        self.window_chat.set_title(f" 欢迎! <{nickname}>")
        self.window_chat.deiconify()

    def response_chat_handle(self, response_data:dict):
        '''接收到聊天结果之后的操作'''
        nickname = response_data['nickname']
        message = response_data['message']
        self.window_chat.append_message(nickname, message)

    def response_signup_handle(self, response_data:dict):
        '''接收到注册结果之后的操作'''
        username = response_data['username']
        password = response_data['password']
        result = response_data['result']
        resason = "???"

        if result == '1':
            # 成功注册
            self.show_login_window()
            showinfo(f"{TITLE}:{SUCCESS_HINT}",f"成功注册名为\'{username}\'的用户。\n您的账户密码是\'{password}\'。")
            return
        else:
            # 排查错误原因
            if username == '':
                resason = "用户名与他人重复!"
            elif password == '':
                resason = f"密码长度必须大于\'{MINNEST_PASSWORD}\'个字符!"

        showinfo(f"{TITLE}:{DEFECT_HINT}", f"失败! 因为{resason}")

    def signup_user(self):
        '''尝试注册新用户'''
        self.window_signup.get_data()
        password = self.window_signup.password
        username = self.window_signup.username
        request_text = RequestProtocol.request_signup(username, password)
        self.conn.send_data(request_text)

    def exit(self):
        '''退出程序'''
        self.active = False # 停止子线程
        self.conn.close() # 关闭套接字
        exit(0) # 退出程序

if __name__ == "__main__": 
    client = Client()
    client.startup()