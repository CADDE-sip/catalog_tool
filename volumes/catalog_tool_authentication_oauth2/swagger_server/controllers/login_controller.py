import connexion
import re
import urllib
from flask import Response, make_response
from logging import getLogger

from swagger_server.services.service import authenticate
from swagger_server.models.request_body import RequestBody  # noqa: E501
from swagger_server.models.response_message import ResponseMessage  # noqa: E501
from swagger_server import util

logger = getLogger(__name__)

__REQUEST_KEY_CKAN_URL = 'ckan_url'
__REQUEST_KEY_USERNAME = 'username'

def login(body):  # noqa: E501
    """対象のCKANユーザに対する認証を行う。

    対象のCKANユーザに対する認証を行い、認証結果を返却する。 # noqa: E501

    :param body: 認証対象のCKANの情報
    :type body: dict

    :rtype: ResponseMessage
    """
    if connexion.request.is_json:
        # body = RequestBody.from_dict(connexion.request.get_json())  # noqa: E501
        body = connexion.request.get_json()
    else:
        logger.error('invalid RequestBody.')
        res = {
            'detail': 'リクエストパラメータはJSON形式ではありません。',
            'status': 400
            }
        response = make_response(res, res['status'])
        return response

    # リクエストボディパラメータのチェック
    if body[__REQUEST_KEY_CKAN_URL] is None:
        logger.error('invalid {}.'.format(__REQUEST_KEY_CKAN_URL))
        res = {
            'detail': 'リクエストパラメータ{}に値が指定されていません。'.format(__REQUEST_KEY_CKAN_URL),
            'status': 400
            }
        response = make_response(res, res['status'])
        return response
    
    if body[__REQUEST_KEY_USERNAME] is None:
        logger.error('invalid {}.'.format(__REQUEST_KEY_USERNAME))
        res = {
            'detail': 'リクエストパラメータ{}に値が指定されていません。'.format(__REQUEST_KEY_USERNAME),
            'status': 400
            }
        response = make_response(res, res['status'])
        return response
    
    res = authenticate(body[__REQUEST_KEY_CKAN_URL], body[__REQUEST_KEY_USERNAME])
    response = make_response(res, res['status'])

    return response

