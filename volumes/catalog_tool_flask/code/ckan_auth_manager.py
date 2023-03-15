import json
import requests
import traceback

from catalogtool_exception import CatalogToolException

# 認証APIのエンドポイント
AUTHENTICATION_URL = '/login'

# 認証API実行
def authenticate_ckan_user(app, ckan_url, username, auth_server, ckan_type):
    app.logger.warning('CKANユーザ認証API実行')

    res = {
        'status': 'error',
        'message': ''
    }

    target_url = 'http://' + auth_server + AUTHENTICATION_URL
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'ckan_url': ckan_url,
        'username': username
    }

    try:
        auth_res = requests.post(target_url, headers=headers, json=payload)

    except Exception:
        app.logger.error(traceback.format_exc())
        if ckan_type == 'release':
            raise CatalogToolException('authenticate_ckan_user_release_AuthSeverException', 500)
        else:
            raise CatalogToolException('authenticate_ckan_user_detail_AuthSeverException', 500)

    if auth_res.status_code == 400:
        app.logger.warning(json.loads(auth_res.content.decode())['detail'])
        if ckan_type == 'release':
            raise CatalogToolException('authenticate_ckan_user_release_RequestError', 400)
        else:
            raise CatalogToolException('authenticate_ckan_user_detail_RequestError', 400)
    if auth_res.status_code >= 300:
        app.logger.warning(json.loads(auth_res.content.decode())['detail'])
        if ckan_type == 'release':
            raise CatalogToolException('authenticate_ckan_user_release_AuthServerError', 500)
        else:
            raise CatalogToolException('authenticate_ckan_user_detail_AuthServerError', 500)

    res['status'] = 'success'
    res['message'] = json.loads(auth_res.content.decode())['detail']

    return res

