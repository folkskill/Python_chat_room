from config import *

class ResponseProtocol(object):
    '''响应拼接'''

    @staticmethod
    def response_login_result(result, nickname:str, username:str):
        '''
        拼接登录响应，数据格式应为：“响应协议编号|登陆结果|登录用户昵称|登录用户用户名”
        :param result：登陆结果，0或1，0表示失败，1表示成功
        :param nickname：登陆用户昵称，若登陆失败则该值为空字符串
        :param username：登陆用户名，若登陆失败则该值为空字符串
        :return：登陆结果响应格式字符串
        '''
        return DELLMITER.join([RESPONSE_LOGIN_RESULT, result, nickname, username])
    
    @staticmethod
    def response_signup(username:str, password:str, result:str):
        """
        拼接登录响应，数据格式为：“响应协议编号|用户名|密码|结果”
        """
        return DELLMITER.join([RESPONSE_SIGNUP, username, password, result])

    @staticmethod
    def response_chat(nickname:str, messages:str):
        """
        拼接聊天响应，数据格式为：“响应协议编号|聊天发送者昵称|聊天信息”
        :param nickname：聊天发送者的昵称
        :param messages：聊天内容
        :return 聊天响应协议格式字符串
        """
        return DELLMITER.join([RESPONSE_CHAT, nickname, messages])   