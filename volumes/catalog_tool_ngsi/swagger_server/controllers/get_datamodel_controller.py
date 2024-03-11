import connexion
import re
import urllib
from flask import Response, make_response
from logging import getLogger

from swagger_server.services.service import datamodel_search
from swagger_server.models.entity import Entity  # noqa: E501
from swagger_server.models.error_response import ErrorResponse  # noqa: E501
from swagger_server import util

logger = getLogger(__name__)

def get_datamodel():  # noqa: E501
    """DataModel取得

    クエリに設定したデータ種別を基にデータモデルを取得する。 # noqa: E501

    :param type: データモデルを取得する対象のNGSIデータのエンティティタイプ
    :type type: str
    :param x_catalogtool_ngsi_url: データモデルを取得する対象のNGSIデータが蓄積されたNGSIサーバのURL
    :type x_catalogtool_ngsi_url: str
    :param fiware_service: データモデルを取得する対象のNGSIデータが蓄積されたFiware-Service
    :type fiware_service: str
    :param fiware_service_path: データモデルを取得する対象のNGSIデータが蓄積されたFiware-ServicePath
    :type fiware_service_path: str

    :rtype: Entity
    """
    
    # extract query paramete
    query_string = '?'
    for key in connexion.request.args.keys():
        if key == 'type':
            query_string = key + "=" + urllib.parse.quote(connexion.request.args[key])
    
    # extract request header
    resource_url = connexion.request.headers["x_catalogtool_ngsi_url"]

    fiware_service = None
    fiware_servicepath = None

    if "fiware_service" in connexion.request.headers:
        fiware_service = connexion.request.headers["fiware_service"]
    if "fiware_servicepath" in connexion.request.headers:
        fiware_servicepath = connexion.request.headers["fiware_servicepath"]
    
    # resource_urlのチェック
    # データ管理サーバ（NGSI）のI/Fであることをチェック
    if not re.match(r"https?://.*/v2.*/entities", resource_url):
        logger.error("invalid resource URL. url:" + resource_url)
        res = {
            "detail": "データ管理サーバ（NGSI）のURLが不正です。配信の情報提供ページURLを確認してください。",
            "status": 400
            }
        response = make_response(res, 400)
        return response
    
    # options=value/uniqueが指定された場合はUIと合わないのでエラーとする？
    # 基本的にentities/typesでとれるデータを返却する。で問題なし？

    data, code = datamodel_search(
        resource_url,
        query_string,
        fiware_service,
        fiware_servicepath)
    response = make_response(data, code)

    return response
