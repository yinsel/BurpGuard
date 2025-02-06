from mitmproxy import http
from Utils.Crypto import *
import httpx
from base64 import b64encode,b64decode
from urllib.parse import quote,unquote
import json
import traceback

class ClientProxyHandler:
    def __init__(self) -> None:
        self.client = httpx.Client(timeout=None,verify=False)
        
    # 处理来自客户端的请求，通常在这里对请求进行解密
    def request(self,flow: http.HTTPFlow):
        try:
            req = flow.request                  # 获取请求对象
            # 在这里编写你的代码
            # ...

        except Exception as e:
            traceback.print_exception(e)
        finally:
            return flow

    # 处理返回给客户端的响应，通常在这里对响应进行加密
    def response(self,flow: http.HTTPFlow):
        try:
            req = flow.request                  # 获取请求对象
            rsp = flow.response                 # 获取响应对象
            # 在这里编写你的代码
            # ...

        except Exception as e:
            traceback.print_exception(e)
        finally:
            return flow
    
addons = [ClientProxyHandler()]