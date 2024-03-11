# -*- coding: utf-8 -*-
import json
import logging
from urllib.parse import urlparse
from flask import jsonify

from swagger_server.services.authenticate import get_accesstoken_ngsi
from swagger_server.services.ngsi import get_request
from swagger_server.services.ngsiException import ngsiException

logger = logging.getLogger(__name__)

# const
__CONFIG_FILE_PATH = './swagger_server/configs/config.json'
__CONFIG_KEY_NGSI_ENTITIES = 'entities_limit'
__CONFIG_KEY_NGSI_TYPES = 'types_limit'
__CONFIG_KEY_NGSI_NGSIAUTH = 'ngsi_auth'


def datamodel_search(
        resource_url: str,
        query_string: str,
        fiware_service: str,
        fiware_servicepath: str):

    """
    ListEntitesAPIおよびTypes APIを実行し、取得した情報からデータモデルを作成し返却する

    Args:
        resource_url         str : リソースURL(Entites)
        query_string         str : クエリストリング
        fiware_service       str : テナント
        fiware_servicepath   str : サービスパス

    Returns:
        dict : 取得したデータモデル
        int  : ステータスコード

    Raises:

    """
    # read config
    ngsi_config = None
    try:
        with open(__CONFIG_FILE_PATH, "r") as f:
            ngsi_config = json.load(f)
    except Exception as e:
        logger.error(str(e))
        res = {
            "detail": "コンフィグファイル（NGSI）の読み込みに失敗しました。サイト管理者に問い合わせてください。",
            "status": 500
            }
        return res, 500
    
    # get accesstoken
    domain = urlparse(resource_url).netloc
    auth_value = None
    try:
        auth_value = get_accesstoken_ngsi(domain , ngsi_config[__CONFIG_KEY_NGSI_NGSIAUTH])
    except Exception as e:
        logger.error(str(e))
        res = {
            "detail": "データ管理サーバ（NGSI）の認証情報の取得に失敗しました。サイト管理者に問い合わせてください。",
            "status": 500
            }
        return res, 500
    
    # get List Entites
    resource_url = resource_url.split('entities')[0]+'entities'

    req_header = {
        'Accept': 'application/json',
        'Authorization': auth_value
    }
    
    if fiware_service is not None:
        req_header['Fiware-Service'] = fiware_service
    if fiware_servicepath is not None:
        req_header['Fiware-ServicePath'] = fiware_servicepath
    
    entity_limit = 20
    types_limit = 100
    
    if __CONFIG_KEY_NGSI_ENTITIES in ngsi_config:
        entity_limit = ngsi_config[__CONFIG_KEY_NGSI_ENTITIES]
    if __CONFIG_KEY_NGSI_TYPES in ngsi_config:
        types_limit = ngsi_config[__CONFIG_KEY_NGSI_TYPES]
    
    entites = None
    try:
        url = resource_url + '?' + query_string + '&limit=' + str(entity_limit)
        data = get_request(url, req_header)
        entites = json.loads(data.read().decode('utf8'), strict=False)
    except ngsiException as e:
        response = {
            "detail": e.message,
            "status": e.status
        }
        return response, e.status
    
    # convert datamodel
    datamodel = {}
    if entites is not None:
        if len(entites) >= 2:
            # get List Entites
            attributes = None
            try:
                type = query_string.replace('type=', '')
                url = resource_url.replace('entities', 'types') + '/' + type + '?limit=' + str(types_limit)
                data = get_request(url, req_header)
                attributes = json.loads(data.read().decode('utf8'), strict=False)
            except ngsiException as e:
                response = {
                    "detail": e.message,
                    "status": e.status
                }
                return response, e.status
            
            # dict loop, in key
            for tattr in attributes['attrs']:
                flg = False
                target = {}
                
                # array loop, in dict
                for entity in entites:
                    if tattr in entity:
                        target = entity[tattr]
                        flg = True
                        break;
                    
                if flg:
                    datamodel[tattr] = target
                else:
                    datamodel[tattr] = {'type': attributes['attrs'][tattr]['types'][0]}
                
            
        elif len(entites) == 1:
            # delete id and type
            del entites[0]['id'], entites[0]['type']
            datamodel = entites[0]
        else:
            datamodel = {}
    
    return jsonify(datamodel), 200


def get_ngsidata(
        resource_url: str,
        fiware_service: str,
        fiware_servicepath: str):

    """
    データ取り込み対象のNGSIデータを返却する

    Args:
        resource_url         str : リソースURL
        fiware_service       str : テナント
        fiware_servicepath   str : サービスパス

    Returns:
        dict : 取得したNGSIデータ
        int  : ステータスコード

    Raises:

    """

    # NGSIデータ取得
    data, code = __get_ngsidata(
        resource_url,
        fiware_service,
        fiware_servicepath)

    if code != 200:
        return data, code
    else:
        return data.read(), code


def get_original_ngsidata(
        resource_url: str,
        fiware_service: str,
        fiware_servicepath: str):

    """
    原本に使用するNGSIデータを成形したデータを返却する

    Args:
        resource_url         str : リソースURL
        fiware_service       str : テナント
        fiware_servicepath   str : サービスパス

    Returns:
        str : 原本に使用するNGSIデータ
        int : ステータスコード

    Raises:

    """

    # NGSIデータ取得
    data, code = __get_ngsidata(
        resource_url,
        fiware_service,
        fiware_servicepath)
    
    if code != 200:
        return data, code
    
    # 原本生成
    try:
        jsondata = json.loads(data.read().decode('utf8'), strict=False)
        originaldata = json.dumps(jsondata, separators=(',', ':'), sort_keys=True)
    except Exception as e:
        logger.error(str(e))
        res = {
            "detail": "NGSIデータの成形に失敗しました。サイト管理者に問い合わせてください。",
            "status": 500
            }
        return res, 500

    return originaldata, code


def __get_ngsidata(
        resource_url: str,
        fiware_service: str,
        fiware_servicepath: str):
    """
    NGSIデータ取得
    Args:
        resource_url         str : リソースURL
        fiware_service       str : テナント
        fiware_servicepath   str : サービスパス

    Returns:
        dict : NGSIデータ
        int  : ステータスコード

    Raises:

    """

    # read config
    ngsi_config = None
    try:
        with open(__CONFIG_FILE_PATH, 'r') as f:
            ngsi_config = json.load(f)
    except Exception as e:
        logger.error(str(e))
        res = {
            "detail": "コンフィグファイル（NGSI）の読み込みに失敗しました。サイト管理者に問い合わせてください。",
            "status": 500
            }
        return res, 500
    
    # get accesstoken
    domain = urlparse(resource_url).netloc
    auth_value = None
    try:
        auth_value = get_accesstoken_ngsi(domain , ngsi_config[__CONFIG_KEY_NGSI_NGSIAUTH])
    except Exception as e:
        logger.error(str(e))
        res = {
            "detail": "データ管理サーバ（NGSI）の認証情報の取得に失敗しました。サイト管理者に問い合わせてください。",
            "status": 500
            }
        return res, 500
    
    req_header = {
        'Accept': 'application/json',
        'Authorization': auth_value
    }
    
    if fiware_service is not None:
        req_header['Fiware-Service'] = fiware_service
    if fiware_servicepath is not None:
        req_header['Fiware-ServicePath'] = fiware_servicepath
    
    # NGSIデータ取得
    ngsi_data = None
    try:
        ngsi_data = get_request(resource_url, req_header)
    except ngsiException as e:
        response = {
            "detail": e.message,
            "status": e.status
        }
        return response, e.status

    return ngsi_data, 200

