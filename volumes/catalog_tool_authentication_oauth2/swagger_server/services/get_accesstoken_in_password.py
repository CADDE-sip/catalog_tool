#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import base64
from logging import getLogger

from swagger_server.services.external_interface import ExternalInterface

external_interface = ExternalInterface()
logger = getLogger(__name__)

__CONFIG_KEY_AUTHENTICATION_URL = 'authentication_url'
__CONFIG_KEY_CLIENT_ID = 'client_id'
__CONFIG_KEY_CLIENT_SECRET = 'client_secret'
__CONFIG_KEY_USER_ID = 'username'
__CONFIG_KEY_USER_PW = 'password'


def get_accesstoken(config: dict) -> dict:

    """
    Resource Owner Password Credentials Grant認証でアクセストークンを取得する


    Args:
        config dict : コンフィグ設定値(config.jsonで設定した値)

    Returns:
        dict : 認証結果
    """

    headers_auth = {}

    # コンフィグ設定値のチェック
    if __CONFIG_KEY_AUTHENTICATION_URL not in config:
        logger.error('not setting {}.'.format(__CONFIG_KEY_AUTHENTICATION_URL))
        res = {
            'detail': 'コンフィグファイルに{}が設定されていません。'.format(__CONFIG_KEY_AUTHENTICATION_URL),
            'status': 500
        }
        return res

    if __CONFIG_KEY_CLIENT_ID not in config:
        logger.error('not setting {}.'.format(__CONFIG_KEY_CLIENT_ID))
        res = {
            'detail': 'コンフィグファイルに{}が設定されていません。'.format(__CONFIG_KEY_CLIENT_ID),
            'status': 500
        }
        return res

    if __CONFIG_KEY_CLIENT_SECRET not in config:
        logger.error('not setting {}.'.format(__CONFIG_KEY_CLIENT_SECRET))
        res = {
            'detail': 'コンフィグファイルに{}が設定されていません。'.format(__CONFIG_KEY_CLIENT_SECRET),
            'status': 500
        }
        return res

    if __CONFIG_KEY_USER_ID not in config:
        logger.error('not setting {}.'.format(__CONFIG_KEY_USER_ID))
        res = {
            'detail': 'コンフィグファイルに{}が設定されていません。'.format(__CONFIG_KEY_USER_ID),
            'status': 500
        }
        return res

    if __CONFIG_KEY_USER_PW not in config:
        logger.error('not setting {}.'.format(__CONFIG_KEY_USER_PW))
        res = {
            'detail': 'コンフィグファイルに{}が設定されていません。'.format(__CONFIG_KEY_USER_PW),
            'status': 500
        }
        return res
    

    # form dataを作成
    # ----------------------------------------------------
    post_form_data = {}
    post_form_data['username'] = config[__CONFIG_KEY_USER_ID]
    post_form_data['password'] = config[__CONFIG_KEY_USER_PW]
    post_form_data['grant_type'] = 'password'
    # ----------------------------------------------------

    # リクエストヘッダを作成
    # ----------------------------------------------------
    header_dict = {}
    header_dict['Accept'] = 'application/json'
    header_dict['Content-Type'] =  'application/x-www-form-urlencoded'
    # 認証サーバへ接続するためのアクセストークンを作成
    tmp_str = config[__CONFIG_KEY_CLIENT_ID] + ':' + config[__CONFIG_KEY_CLIENT_SECRET]
    connect_str = base64.b64encode(tmp_str.encode())
    header_dict['Authorization'] = 'Basic ' + connect_str.decode(encoding='utf-8')
    # ----------------------------------------------------

    # 認証サーバからアクセストークンを取得する
    response = external_interface.http_post(config[__CONFIG_KEY_AUTHENTICATION_URL], header_dict, post_form_data)

    if response.status_code < 200 or 300 <= response.status_code:
        logger.error('HTTP request failed. status:{}, detail:{}'.format(response.status_code, response.text))
        res = {
            'detail': '認証に失敗しました。エラー内容：' + response.text,
            'status': response.status_code
        }
        return res

    res = {
        'detail': '認証に成功しました。',
        'status': 200
    }
    return res

