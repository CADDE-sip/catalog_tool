# -*- coding: utf-8 -*-
import io
import json
import logging
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from swagger_server.services.ngsiException import ngsiException

logger = logging.getLogger(__name__)


def get_request(
        url: str,
        req_header: dict):
    """
    ListEntitesAPIおよびTypes APIを実行し、取得した情報からデータモデルを作成し返却する

    Args:
        url         str  : URL
        req_header  dict : リクエストヘッダ―

    Returns:
        dict : 取得したデータモデル
        code : 

    Raises: 

    """
    
    response = None
    
    try:
        req = urllib.request.Request(url, headers=req_header)
        with urllib.request.urlopen(req) as res:
            response = io.BytesIO(res.read())
            
    except urllib.error.HTTPError as err:
        logger.error(str(err.code) + " : " + err.reason)
        raise(ngsiException("データ管理サーバ（NGSI）へのリクエストエラーが発生しました。エラー内容:" + err.reason, err.code))
        
    except urllib.error.URLError as err:
        logger.error(err.reason)
        raise(ngsiException("データ管理サーバ（NGSI）に接続できないか、指定したサーバーが存在しません。サイト管理者に問い合わせてください。", 500))
    else:
        return response
        