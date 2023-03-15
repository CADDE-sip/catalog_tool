# -*- coding: utf-8 -*-
import requests
from io import BytesIO

from requests.exceptions import Timeout
from timeout_decorator import timeout

class ExternalInterface:

    __HTTP_CONNECT_TIMEOUT = 10
    __HTTP_READ_TIMEOUT = 60

    def http_post(
            self,
            target_url: str,
            headers: dict = None,
            post_body: dict = None,
            verify: bool = True):
        """
        対象URLに対してhttp(post)通信を行ってレスポンスを取得する。

        Args:
            target_url str : 接続するURL
            headers : 設定するheader {ヘッダー名:パラメータ}
            post_body : 設定するbody部


        Returns:
            response : gpost通信のレスポンス

        """

        if not headers:
            headers = {}

        if not post_body:
            post_body = {}

        headers['Cache-Control'] = 'no-cache'

        req = requests
        response = requests.Response()
        if not verify:
           req = requests.Session()
           req.verify = False

        try:
            if 'Content-Type' in headers and headers['Content-Type'] == 'application/x-www-form-urlencoded':
                response = req.post(
                    target_url,
                    headers=headers,

                    timeout=(
                        self.__HTTP_CONNECT_TIMEOUT,
                        self.__HTTP_READ_TIMEOUT),
                    data=post_body
                )
            else:
                response = req.post(
                    target_url,
                    headers=headers,

                    timeout=(
                        self.__HTTP_CONNECT_TIMEOUT,
                        self.__HTTP_READ_TIMEOUT),
                    json=post_body
                )
        except Timeout:
            response.status_code = 408
            response._content = b'Request timeout.'

        except Exception as e:
            response.status_code = 500
            response._content = bytes(str(e), 'utf-8')

        return response

