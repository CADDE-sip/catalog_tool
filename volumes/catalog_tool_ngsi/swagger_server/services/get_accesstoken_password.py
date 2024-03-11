#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib.request
import ssl
import base64
from logging import getLogger

logger = getLogger(__name__)

__CONFIG_KEY_CERTIFICATION_URL = 'certification_url'
__CONFIG_KEY_CLIENT_ID = 'client_id'
__CONFIG_KEY_CLIENT_SECRET = 'client_secret'
__CONFIG_KEY_USER_ID = 'user_id'
__CONFIG_KEY_USER_PW = 'user_pw'


def get_accesstoken(config):

    """
    Resource Owner Password Credentials Grant認証でアクセストークンを取得する


    Args:
        config : コンフィグ設定値(ngsi.jsonで設定した値)

    Returns:
        auth_value : アクセストークンヘッダの値

    """

    auth_value = ""

    # コンフィグ設定値のチェック
    if __CONFIG_KEY_CERTIFICATION_URL not in config:
        logger.error("not setting certification_url.")
        logger.debug(config)
        raise

    if __CONFIG_KEY_CLIENT_ID not in config:
        logger.error("not setting client_id.")
        logger.debug(config)
        raise Exception("invalid config setting.")

    if __CONFIG_KEY_CLIENT_SECRET not in config:
        logger.error("not setting client_secret.")
        logger.debug(config)
        raise Exception("invalid config setting.")

    if __CONFIG_KEY_USER_ID not in config:
        logger.error("not setting user_id.")
        logger.debug(config)
        raise Exception("invalid config setting.")

    if __CONFIG_KEY_USER_PW not in config:
        logger.error("not setting user_pw.")
        logger.debug(config)
        raise Exception("invalid config setting.")

    try:

        # form dataを作成
        # ----------------------------------------------------
        post_form_data = urllib.parse.urlencode({'username': config["user_id"], 'password': config["user_pw"], 'grant_type': 'password'}).encode('utf-8')
        # ----------------------------------------------------
        url = config["certification_url"]
        req = urllib.request.Request("{}".format(url), data=post_form_data, method='POST')

        # リクエストヘッダを作成
        # ----------------------------------------------------
        req.add_header("Accept", "application/json")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        # 認証サーバへ接続するためのアクセストークンを作成
        tmp_str = config["client_id"] + ":" + config["client_secret"]
        connect_str = base64.b64encode(tmp_str.encode())
        req.add_header("Authorization", "Basic " + connect_str.decode(encoding='utf-8'))
        # ----------------------------------------------------

        context = ssl.SSLContext(ssl.PROTOCOL_TLS)

        # 認証サーバからアクセストークンを取得する
        with urllib.request.urlopen(req, context=context, timeout=10) as res:
            json_body = json.loads(res.read())
            logger.debug(json_body)
            # アクセストークンヘッダの値を作成
            # ----------------------------------------------------
            auth_value = "Bearer " + json_body["access_token"]
            # ----------------------------------------------------

    except Exception as e:
        logger.error(e)
        raise


    return auth_value

