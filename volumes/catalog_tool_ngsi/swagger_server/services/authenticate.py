#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import json
import urllib.request
import ssl
from logging import getLogger
import importlib



logger = getLogger(__name__)

__IMPORT_FILE_PATH = 'swagger_server.services.'

__CONFIG_KEY_NGSI_TYPE = 'cert_type'
__CONFIG_KEY_NGSI_AUTH = 'auth'
__CONFIG_KEY_NGSI_ENDPOINT = 'endpoint_url'

__CERT_TYPE_STATIC = 'static'
__CERT_TYPE_CLIENT = 'client_credential'
__CERT_TYPE_PASS = 'password'

def get_accesstoken_ngsi(domain, ngsi_config):
    """
    認証サーバからアクセストークンを取得する

    Args:
        domain 対象ドメイン
        ngsi_config コンフィグ

    Returns:
        auth_value : アクセストークンヘッダの値

    """

    auth_value = ""
    ngsi_config_domain = {}

    try:
        # コンフィグファイルのドメインに一致した情報を取得
        for e in ngsi_config:
            if e[__CONFIG_KEY_NGSI_ENDPOINT] == domain:
                ngsi_config_domain = e
                break
                
        if 0 < len(ngsi_config_domain):
            if __CONFIG_KEY_NGSI_TYPE not in ngsi_config_domain:
               logger.error("not setting cert_type.")
               logger.debug(ngsi_config_domain)
               raise Exception("invalid config setting.")

            # 固定値の場合
            if ngsi_config_domain[__CONFIG_KEY_NGSI_TYPE] == __CERT_TYPE_STATIC:
                # 利用者コネクタでのアクセストークン
                auth_value = "Bearer " + ngsi_config_domain[__CONFIG_KEY_NGSI_AUTH]
            #他認証必の場合
            elif ngsi_config_domain[__CONFIG_KEY_NGSI_TYPE] == __CERT_TYPE_CLIENT or\
                 ngsi_config_domain[__CONFIG_KEY_NGSI_TYPE] == __CERT_TYPE_PASS:
                # 提供者コネクタでのアクセストークン
                # 対象のモジュールを呼びだし
                import_path = __IMPORT_FILE_PATH + "get_accesstoken_" + ngsi_config_domain[__CONFIG_KEY_NGSI_TYPE]
                module = importlib.import_module(import_path)

                # アクセストークン取得
                auth_value = module.get_accesstoken(ngsi_config_domain)
            else:
                logger.debug("invalid cert_type.")

    except Exception:
        logger.debug("Failed to get access token.")
        # アクセストークンなし
        raise

    return auth_value


