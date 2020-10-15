import requests
import json
from random import randrange
from typing import Optional


        
class Proxy:
    ip = None
    port = None
    user = None
    password = None
    
    def __init__(self,ip,port,user,password):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        

class ProxyHandler:
    GET_PROXIES_ENDPOINT = f'https://proxy6.net/api/YOUR_API_ENDPOINT'
    last_proxy_index_used = None
    proxies = []
    total_proxies = 0
    def __init__(self):
        response = requests.get(self.GET_PROXIES_ENDPOINT)
        data = json.loads(response.text)
        if not 'list' in data:
            exit('NO PROXIES AVAILABLE')
        for proxy_id in data['list']:
            raw_data = data['list'][proxy_id]
            if not 'http' in raw_data['type']:
                continue
            if len(str(raw_data['ip']).split('.')) != 4:
                continue
            self.proxies.append(Proxy(
                ip=raw_data['ip'],
                port=raw_data['port'],
                user=raw_data['user'],
                password= raw_data['pass']
            ))
            self.total_proxies= self.total_proxies + 1

                
    def getProxy(self):
        # We get proxies by cycling them (not random, not same everytime)
        if self.total_proxies > 0:
            return self.proxies[self.calculateNextProxyId()]
            
        
        
    def calculateNextProxyId(self):
        if self.last_proxy_index_used == None:
            self.last_proxy_index_used = 0
            return 0
        else:
            # Try to get the next proxy
            if self.last_proxy_index_used < self.total_proxies -1:
                self.last_proxy_index_used = self.last_proxy_index_used + 1
                return self.last_proxy_index_used
            self.last_proxy_index_used = 0
            return 0
