import connexion
import re
import urllib
from flask import Response, make_response
from logging import getLogger

from swagger_server.services.service import get_ngsidata
from swagger_server.models.entity import Entity  # noqa: E501
from swagger_server.models.error_response import ErrorResponse  # noqa: E501
from swagger_server import util

logger = getLogger(__name__)

def get_data():  # noqa: E501
    """NGSIデータ取り込み

    データ取り込み対象のNGSIデータを取得する。 # noqa: E501

    :param type: データ取り込み対象のNGSIデータのエンティティタイプ
    :type type: str
    :param x_catalogtool_ngsi_url: データ取り込み対象のNGSIデータが蓄積されたNGSIサーバのURL
    :type x_catalogtool_ngsi_url: str
    :param fiware_service: データ取り込み対象のNGSIデータが蓄積されたFiware-Service
    :type fiware_service: str
    :param fiware_service_path: データ取り込み対象のNGSIデータが蓄積されたFiware-ServicePath
    :type fiware_service_path: str

    :rtype: Entity
    """
    
    # extract query paramete
    query_string = '?'
    query_key = ''
    for key in connexion.request.args.keys():
        if key == 'type':
            query_string = key + '=' + urllib.parse.quote(connexion.request.args[key])
            query_key = urllib.parse.quote(connexion.request.args[key])
    
    # extract request header
    resource_url = connexion.request.headers['x_catalogtool_ngsi_url']

    fiware_service = None
    fiware_servicepath = None

    if 'fiware_service' in connexion.request.headers:
        fiware_service = connexion.request.headers['fiware_service']
    if 'fiware_servicepath' in connexion.request.headers:
        fiware_servicepath = connexion.request.headers['fiware_servicepath']
    
    # resource_urlのチェック
    # データ管理サーバ（NGSI）のI/Fであることをチェック
    if not re.match(r'https?://.*/v2.*/entities', resource_url):
        logger.error('invalid resource URL. url:' + resource_url)
        res = {
            "detail": "データ管理サーバ（NGSI）のURLが不正です。配信の情報提供ページURLを確認してください。",
            "status": 400
            }
        response = make_response(res, 400)
        return response

    # データ管理サーバ（NGSI）のエンティティの属性値以降を取得するようなI/Fでないことをチェック
    if re.match(r'https?://.*/v2.*/entities/.*/attr', resource_url):
        logger.error('invalid resource URL. url:' + resource_url)
        res = {
            "detail": "データ管理サーバ（NGSI）の未サポートURLです。配信の情報提供ページURLを確認してください。",
            "status": 400
            }
        response = make_response(res, 400)
        return response
    
    parse_url = urllib.parse.urlparse(resource_url)
    query = urllib.parse.parse_qs(parse_url.query)
    
    if 'type' not in query:
        logger.error('invalid X-CATALOGTOOL-NGSI-URL. url:' + resource_url)
        res = {
            "detail": "配信の情報提供ページURLにクエリtypeが含まれていません。配信の情報提供ページURLを確認してください。",
            "status": 400
            }
        response = make_response(res, 400)
        return response

    else:
        if query['type'][0] != query_key:
            logger.error('invalid query type.')
            res = {
                "detail": "配信の情報提供ページURLのクエリtypeとNGSIデータ種別が一致しません。配信の情報提供ページURLを確認してください。",
                "status": 400
                }
            response = make_response(res, 400)
            return response

    data, code = get_ngsidata(
        resource_url,
        fiware_service,
        fiware_servicepath)
    response = make_response(data, code)
    response.headers['Content-Type'] = 'application/json'

    return response
