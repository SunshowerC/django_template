#!/usr/bin/python
#coding=utf-8 
from Crypto.Cipher import AES
import base64
import socket
import struct
import fcntl
import time
import random
import json
import urllib
import urllib2
import logging


def m_encrypt(text, key):
    obj = AES.new(key, AES.MODE_CBC, key) #使用AES-128 mode CBC加密,要求key为16位，明文要为16的倍数，不足16位倍数要补齐
    length = 16
    count = len(text)
    if count < length:
        add = (length-count)
        text = text + ('\0' * add)
    else:
        add = (length-(count % length))
        text = text + ('\0' * add)

    res= obj.encrypt(text)
    ret = base64.b64encode(res)
    return ret

def getSrcIP():
    '''
        获取客户端真实IP
    '''
    try:
        return getip('em2')
    except IOError:
        try:
            return getip('em1')
        except IOError:
            try:
                return getip('eth0')
            except IOError:
                try:
                    return getip('eth1')
                except IOError:
                    return getip('eth2')

def getip(ethname):
    '''
        获取主机ip
    '''
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24])

def authTicket(ticket,APP_ID,APP_KEY):
    '''
        验证ticket有效性
    '''
    logger = logging.getLogger('scripts')
    browseIp = '10.1.50.92'
    logger.info(browseIp)
    parameter = {'ticket':ticket, 'ip':browseIp}
    req_url = 'https://passport.oa.fenqile.com/api/auth.json?'+ urllib.urlencode(parameter)
    makehttp = MakeHttp(APP_ID,APP_KEY, req_url)
    ret = makehttp.execute()
    user_info = {}
    if ret.has_key('result') and ret['result'] == 0 and ret['result_rows'] is not None and len(ret['result_rows']) > 0:
        user_info['result'] = ret['result']
        user_info['res_info'] = ret['res_info']
        user_info['min'] = ret['result_rows']['min']
        user_info['name'] = ret['result_rows']['name']
        user_info['mid'] = ret['result_rows']['mid']
        return user_info
    elif ret.has_key('result') and ret['result'] != 0:
        user_info['result'] = ret['result']
        user_info['res_info'] = ret['res_info']
        return user_info
    else:
        return ret

class MakeHttp(object):

    def __init__(self, appid,appkey,req_url):
        self.appid = appid
        self.appkey = appkey
        self.req_url = req_url

    def execute(self):
        return self.executeHttp();

    def getFofApiRequestHeader(self):
        '''
            返回header 请求头
            timestamp   当前时间戳   header 请求头
            rand    随机数 rand()  header 请求头
            appid   应用appid header 请求头
            token   以应用对应的app_key为密钥，加密timestamp,rand,app_id的串，
            例如encrypt("timestamp=$timestamp&rand=$rand&appip=$appid", $app_key),加密方法请参考各个语言的SDK  header 请求头
        '''
        c_timestamp = int(time.time()) 
        c_random = random.randint(1,50)
        data = "timestamp=%s&rand=%s&appid=%s" %(c_timestamp,c_random,self.appid)
        token = m_encrypt(data,self.appkey)
        input_params = {
            'appid' : self.appid ,
            'rand' : c_random,
            'timestamp' : c_timestamp,
            'token' : token
        }

        return input_params
    
     
    def executeHttp(self):
        logger = logging.getLogger('scripts')
        reques_params = self.getFofApiRequestHeader()
        req = urllib2.Request(self.req_url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        req.add_header('timestamp', reques_params['timestamp'])
        req.add_header('rand', reques_params['rand'])
        req.add_header('appid', reques_params['appid'])
        req.add_header('token', reques_params['token'])
        response=urllib2.urlopen(req).read()
        logger.info(response)
        content = json.loads(response)
        return content
