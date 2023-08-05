#coding:utf-8
#Author: UlionTse

import random
import requests
from .config_UA import *
from .config_proxy import gen

class Req2:
    def __init__(self):
        self.default_UA = PC_UA_POOL
        self.gen_proxy_pool = gen.gen_pool(2)
        self.default_PROXY = gen.test_pool(self.gen_proxy_pool)

        # self.default_PROXY =    [{'http': '211.103.208.244:80'},
        #                          {'https': '124.232.148.7:3128'},
        #                          {'https': '118.31.103.7:3128'},
        #                          {'http': '180.168.179.193:8080'},
        #                          {'https': '122.72.18.34:80'},
        #                          {'https': '120.27.131.204:3128'},
        #                          {'https': '124.232.148.7:3128'},
        #                          {'https': '121.43.178.58:3128'}]
        
    def ua_req(self,method,url,UA_list=None,**kwargs):
        
        '''
        :param method: str, 'get' or 'post'.
        :param url: str, eg: 'https://www.python.org'.
        :param UA_list: list or None. Default_use: self.default_UA.
        :param kwargs: like '**kwargs' of `requests`.
        :return: <Response>
        '''
        
        ss = requests.Session()
        if UA_list:
            ss.headers.update({'User-Agent': random.choice(UA_list)})
        else:
            ss.headers.update({'User-Agent': random.choice(self.default_UA)})
        try:
            if method == 'get':
                res = ss.get(url,**kwargs)
                return res
            if method == 'post':
                res = ss.post(url,**kwargs)
                return res
        finally:
            ss.close()
            

    def proxy_req(self,method,url,PROXY_list=None,**kwargs):
        
        '''
        :param method: str, 'get' or 'post'.
        :param url: str, eg: 'https://www.python.org'.
        :param PROXY_list: list or None. Default_use: self.default_PROXY.
        :param kwargs: like '**kwargs' of `requests`.
        :return: <Response>
        '''
        
        ss = requests.Session()
        if PROXY_list:
            ss.proxies.update(random.choice(PROXY_list))
        else:
            ss.proxies.update(random.choice(self.default_PROXY))
        try:
            if method == 'get':
                res = ss.get(url,**kwargs)
                return res
            if method == 'post':
                res = ss.post(url,**kwargs)
                return res
        finally:
            ss.close()
            
            
    def all_req(self,method,url,UA_list=None,PROXY_list=None,**kwargs):
        
        '''
        :param method: str, 'get' or 'post'.
        :param url: str, eg: 'https://www.python.org'.
        :param UA_list: list or None. Default_use: self.default_UA.
        :param PROXY_list: list or None. Default_use: self.default_PROXY.
        :param kwargs: like '**kwargs' of `requests`.
        :return: <Response>
        '''
        
        ss = requests.Session()
        if UA_list:
            ss.headers.update({'User-Agent': random.choice(UA_list)})
        else:
            ss.headers.update({'User-Agent': random.choice(self.default_UA)})
        if PROXY_list:
            ss.proxies.update(random.choice(PROXY_list))
        else:
            global choice_proxy
            choice_proxy = random.choice(self.default_PROXY)
            ss.proxies.update(choice_proxy)

        try:
            if method == 'get':
                res = ss.get(url,**kwargs)
                return res
            if method == 'post':
                res = ss.post(url,**kwargs)
                return res
        except:
            self.default_PROXY.remove(choice_proxy)
            if not self.default_PROXY:
                print('default_PROXY is None!')
            #self.all_req(self, method, url, UA_list=UA_list, PROXY_list=PROXY_list, **kwargs)
        finally:
            ss.close()


