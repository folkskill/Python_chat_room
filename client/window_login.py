from tkinter import Tk,Button,Label,Entry,Frame,END,LEFT
from config import *

class WindowLogin(Tk):
    """登录窗口"""

    def __init__(self):
        '''初始化登录窗口'''
        super(WindowLogin, self).__init__()
        
        self.username = None
        self.password = None

        # 设置窗口属性
        self.window_init()

        # 填充控件
        self.add_widgets()

    def window_init(self):
        '''初始化窗口属性'''
        # 设置窗口相关设置
        self.title(WINDOW_LOGIN_NAME)
        self.resizable(False, False)

        # 获取相关变量
        window_width,window_height = WINDOW_LOGIN_SIZE.split('x')

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        pos_x = round((screen_width - int(window_width)) / 2)
        pos_y = round((screen_height - int(window_height)) / 2)

        # 设置窗口大小位置
        self.geometry(f"{WINDOW_LOGIN_SIZE}+{pos_x}+{pos_y}")

    def add_widgets(self):
        '''初始化控件到窗口'''
        # 用户名提示标签
        username_lable = Label(self)
        username_lable['text'] = "用户名:"
        username_lable.grid(row = 0, column = 0, padx = 10, pady = 5)
        # 用户名输入文本框
        username_entry = Entry(self, name = 'username_entry')
        username_entry['width'] = 25
        username_entry.grid(row = 0, column = 1)

        # 密码提示标签
        password_lable = Label(self)
        password_lable['text'] = "密  码:"
        password_lable.grid(row = 1, column = 0)
        # 密码提示输入文本框
        password_entry = Entry(self, name = 'password_entry')
        password_entry['show'] = '*'
        password_entry['width'] = 25
        password_entry.grid(row = 1, column = 1)

        # 创建Frame(父物体)
        button_frame = Frame(self, name = 'button_frame')
        # '重置'按钮
        reset_button = Button(button_frame, name = 'reset_button')
        reset_button['text'] = '    清除    '
        reset_button.pack(side = LEFT, padx = 20)
        # '登录'按钮
        login_button = Button(button_frame, name = 'login_button')
        login_button['text'] = '    登录    '
        login_button.pack(side = LEFT)
        # frame设置
        button_frame.grid(row = 2, columnspan = 2, pady = 5)

    def clear_entry(self): 
        '''清空输入框'''
        self.children['username_entry'].delete(0,END)
        self.children['password_entry'].delete(0,END)
        self.username = None
        self.password = None

    def get_data(self):
        '''获取数据'''
        self.username = self.children['username_entry'].get()
        self.password = self.children['password_entry'].get()

    def on_reset_button_click(self, command):
        '''清除按钮的事件注册'''
        reset_button = self.children['button_frame'].children['reset_button']
        reset_button['command'] = command

    def on_login_button_click(self, command):
        '''登录按钮的事件注册'''
        login_button = self.children['button_frame'].children['login_button']
        login_button['command'] = command

    def on_window_close(self, command):
        '''关闭窗口的响应注册'''
        self.protocol('WM_DELETE_WINDOW', command)

if __name__ == "__main__":
    window = WindowLogin()
    window.mainloop()