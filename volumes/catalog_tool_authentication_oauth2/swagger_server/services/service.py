# -*- coding: utf-8 -*-
import io
import json
import ssl
import logging
from urllib.parse import urlparse
from flask import jsonify
import importlib

logger = logging.getLogger(__name__)

# const
__CONFIG_FILE_PATH = './swagger_server/configs/config.json'
__CONFIG_KEY_OAUTH2AUTH = 'oauth2_auth'

__IMPORT_FILE_PATH = 'swagger_server.services.'

__CONFIG_KEY_AUTH_TYPE = 'auth_type'
__CONFIG_KEY_CKAN_URL = 'ckan_url'
__CONFIG_KEY_USER_ID = 'username'

__AUTH_TYPE_STATIC = 'static'
__AUTH_TYPE_CLIENT = 'client_credential'
__AUTH_TYPE_PASS = 'password'

def authenticate(
        ckan_url: str,
        username: str) -> dict:

    """
    対象のCKANユーザに対する認証を行い、認証結果を返却する。

    Args:
        ckan_url  str : CKAN URL
        username  str : CKANユーザ名

    Returns:
        dict : 認証結果
    """
    # read config
    oauth2_config = None
    try:
        with open(__CONFIG_FILE_PATH, 'r') as f:
            oauth2_config = json.load(f)
    except Exception as e:
        logger.error(str(e))
        res = {
            'detail': 'コンフィグファイルの読み込みに失敗しました。',
            'status': 500
            }
        return res

    try:
        oauth2_config_ckan = {}
        # コンフィグファイルのCKAN URL、CKANユーザ名に一致した認証サーバの情報を取得
        for e in oauth2_config[__CONFIG_KEY_OAUTH2AUTH]:
            if e[__CONFIG_KEY_CKAN_URL] == ckan_url and \
               e[__CONFIG_KEY_USER_ID] == username:
                oauth2_config_ckan = e
                break
                
        if 0 < len(oauth2_config_ckan):
            if __CONFIG_KEY_AUTH_TYPE not in oauth2_config_ckan:
                logger.error('not setting auth_type.')
                res = {
                    'detail': '認証方式の設定が不正です。',
                    'status': 500
                }
                return res

            # 認証
            if oauth2_config_ckan[__CONFIG_KEY_AUTH_TYPE] == __AUTH_TYPE_CLIENT or\
               oauth2_config_ckan[__CONFIG_KEY_AUTH_TYPE] == __AUTH_TYPE_PASS:
               # 対象の認証モジュールを呼びだし
               import_path = __IMPORT_FILE_PATH + 'get_accesstoken_in_' + oauth2_config_ckan[__CONFIG_KEY_AUTH_TYPE]
               module = importlib.import_module(import_path)

               # アクセストークン取得
               res = module.get_accesstoken(oauth2_config_ckan)
            else:
                logger.error('invalid auth_type.')
                res = {
                    'detail': '認証方式の設定が不正です。',
                    'status': 500
                }
                return res

        else:
            logger.error('not setting oauth2_auth.')
            res = {
                'detail': '対象の認証サーバの設定がありません。',
                'status': 500
            }
            return res

    except Exception as e:
        logger.error(str(e))
        res = {
            "detail": "認証に失敗しました。エラー内容：" + str(e),
            "status": 500
            }
        return res

    return res

