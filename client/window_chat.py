from tkinter import Toplevel,Text,Button,END,UNITS
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from config import *

class WindowChat(Toplevel):
    '''聊天界面窗口'''

    def __init__(self):
        super(WindowChat, self).__init__()

        # 设置窗口属性
        self.set_window()

        # 添加控件
        self.add_widget()

    def set_window(self):
        '''设置窗口属性'''
        # 变量的获取
        widnow_width,window_height = WINDOW_CHAT_SIZE.split('x')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        pos_x = round((screen_width - int(widnow_width)) / 2)
        pos_y = round((screen_height - int(window_height)) / 2)

        # 设置窗口大小和位置
        self.geometry(f"{WINDOW_CHAT_SIZE}+{pos_x}+{pos_y}")

        # 设置窗口大小不可改变
        self.resizable(False, False)


    def add_widget(self):
        '''添加控件'''
        # 聊天内容显示文本框
        chat_textarea = ScrolledText(self)
        chat_textarea['width'] = 47
        chat_textarea['height'] = 31
        chat_textarea.grid(row = 0, column = 0, columnspan = 2)
        # 添加两个标签(颜色)
        chat_textarea.tag_config('green', foreground = '#008800')
        chat_textarea.tag_config('system', foreground = 'red')
        self.children['chat_text_area'] = chat_textarea # 更新内容

        # 聊天文本输入框
        chat_inputarea = Text(self, name = 'chat_input_area')
        chat_inputarea['width'] = 40
        chat_inputarea['height'] = 7
        chat_inputarea.grid(row = 1, column = 0, pady = 12)

        # 发送按钮
        send_button = Button(self, name = 'send_button')
        send_button['text'] = '发\n送'
        send_button['width'] = 5
        send_button['height'] = 5
        send_button.grid(row = 1, column = 1)

    def set_title(self, title):
        '''设置标题'''
        self.title(f"{TITLE}:{title}")

    def on_send_button_click(self, command):
        '''注册发送按钮的点击事件'''
        self.children['send_button']['command'] = command

    def on_window_closed(self, command):
        '''注册窗口关闭时的事件'''
        self.protocol('WM_DELETE_WINDOW', command)

    def get_inputs(self):
        '''获取输入框内容'''
        msg = self.children['chat_input_area'].get(0.0,END)
        if msg == '\n':
            msg = msg[0:-2]
        return msg
    
    def clear_input(self):
        '''清空输入框'''
        self.children['chat_input_area'].delete(0.0, END)

    def append_message(self, sender:str, message:str):
        '''添加一条消息到聊天区'''
        # 组合发送的内容
        send_info = datetime.now().strftime(f"[%Y-%m-%d %H:%M:%S]<{sender}>")
        line = f"{''.join([LINE for c in send_info])}\n"
        send_info += ('\n' + line)
        self.children['chat_text_area'].insert(END, send_info, 'green')
        self.children['chat_text_area'].insert(END, message)
        self.children['chat_text_area'].insert(END, line + '\n', 'green')

        # 滚动条向下移动
        self.children['chat_text_area'].yview_scroll(100, UNITS)
    
if __name__ == "__main__":
    wc = WindowChat()
    wc.set_title(" 欢迎!")
    wc.mainloop()