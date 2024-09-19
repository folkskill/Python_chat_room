from config import *

class RequestProtocol(object):


    @staticmethod
    def request_login_result(username, password):
        '''
        类型|账号|密码
        :0001|user1|123456
        '''
        return DELLMITER.join([REQUEST_LOGIN,username,password])
    
    @staticmethod
    def request_signup(username, password):
        '''
        类型|账号|密码
        :0003|user1|123456
        '''
        return DELLMITER.join([REQUEST_SIGNUP, username, password])

    @staticmethod
    def request_chat(username, msg):
        '''
        类型|账号|消息内容
        :0002|user1|msg
        '''
        return DELLMITER.join([REQUEST_CHAT, username, msg])