import requests
import json
import traceback
import random
import string
import urllib.parse
import base64

from catalogtool_exception import CatalogToolException


class CaddeAuth:

    # 認証時の固定パラメータ
    __GRANT_TYPE = 'password'

    # コンフィグファイルパス
    __CONFIG_PATH = './config.json'
    __CONFIG_AUTH_KEY = 'authentication'

    # keycloakログイン画面URI
    __KEYCLOAK_CLIENT_ID_QUERY = '/protocol/openid-connect/auth?client_id='
    __KEYCLOAK_REDIRECT_URI_QUERY = '&redirect_uri='
    __KEYCLOAK_STATE_QUERY = '&response_mode=fragment&response_type=code&scope=openid&state='

    # カタログ作成ツール画面URI
    __LOGINLOAD_PATH = 'load/?'
    # 認証サーバAPIパス
    # トークン取得(認可コード)API
    __POST_TOKEN_AUTHORIZATION = '/cadde/api/v4/token/authorizationCode'
    # トークン検証APIパス
    __POST_TOKEN_INTROSPECT = '/cadde/api/v4/token/introspect'
    # トークン更新API
    __POST_TOKEN_REFRESH = '/cadde/api/v4/token/refresh'
    # keycloakログアウトAPI
    __KETCLOAK_LOGOUT = '/protocol/openid-connect/logout'

    def __init__(self, app):
        self.__app = app
        self.__cadde_user_id = None
        self.__token_list = []
        self.auth_state_list = []

    # コンフィグから認証サーバ情報を取得
    def __get_catalog_tool_config(self, config_key):
        config = open(self.__CONFIG_PATH, 'r')
        config = json.load(config)
        return config[self.__CONFIG_AUTH_KEY][config_key]

    # 旧版カタログ作成ツールの来歴認証対応
    # ダミー認可コード生成
    def create_dummy_auth_code(self):
        self.__app.logger.warning('ダミー認可コード生成')
        res = {
            'status': 'error',
            'code': ''
        }

        # ダミー認可コード生成
        string_figure = 36
        dat = string.digits + string.ascii_lowercase + string.ascii_uppercase
        dummy_code = ''.join(
            [random.choice(dat) for i in range(string_figure)])
        # ダミー認可コード保存
        dummy_auth_info = {
            dummy_code: {
                'access_token': '',
                'refresh_token': ''
            }
        }
        self.__token_list.append(dummy_auth_info)
        res['status'] = 'success'
        res['code'] = dummy_code

        return res

    # keycloak画面へのリダイレクトURI作成
    def create_keycloak_redirect_uri(self, catalog_tool_url):
        self.__app.logger.warning('keycloak画面へのリダイレクトURI作成')
        res = {
            'status': 'error',
            'redirect_uri': ''
        }

        # コンフィグからkeycloak情報を取得
        auth_server_url = self.__get_catalog_tool_config('auth_server_url')
        keycloak_endpoint = self.__get_catalog_tool_config('keycloak_endpoint')
        keycloak_client_id = self.__get_catalog_tool_config('client_id')
        if not auth_server_url or not keycloak_endpoint or not keycloak_client_id:
            raise CatalogToolException(
                'create_keycloak_redirect_uri_Exception', 500)

        # keycloakログイン画面からリダイレクトするカタログ作成ツールの画面のURLをエンコーディングして設定
        catalog_tool_url = urllib.parse.quote(
            catalog_tool_url + self.__LOGINLOAD_PATH)

        # UUID生成
        string_figure = 36
        dat = string.digits + string.ascii_lowercase + string.ascii_uppercase
        catalog_tool_uuid = ''.join(
            [random.choice(dat) for i in range(string_figure)])
        # 生成したUUIDを保存
        self.auth_state_list.append(catalog_tool_uuid)

        res['redirect_uri'] = auth_server_url + keycloak_endpoint + self.__KEYCLOAK_CLIENT_ID_QUERY + keycloak_client_id + \
            self.__KEYCLOAK_REDIRECT_URI_QUERY + catalog_tool_url + \
            self.__KEYCLOAK_STATE_QUERY + catalog_tool_uuid
        res['status'] = 'success'
        self.__app.logger.warning(res['redirect_uri'])

        return res

    # トークン取得(認可コード)API実行
    def post_token_authorization_code(self, auth_code, catalog_tool_url):
        self.__app.logger.warning('トークン取得(認可コード)API実行')
        res = {
            'status': 'error'
        }

        # コンフィグからkeycloak情報を取得
        auth_server_url = self.__get_catalog_tool_config('auth_server_url')
        keycloak_client_id = self.__get_catalog_tool_config('client_id')
        keycloak_client_secret = self.__get_catalog_tool_config('client_secret')
        if not auth_server_url or not keycloak_client_id or not keycloak_client_secret:
            raise CatalogToolException(
                'post_token_authorization_code_ConfigError', 500)

        target_url = auth_server_url + self.__POST_TOKEN_AUTHORIZATION
        credential =  f'{keycloak_client_id}:{keycloak_client_secret}'
        bearer = base64.b64encode(credential.encode()).decode()
        headers = {'Authorization': f'Basic {bearer}'}
        redirect_uri = catalog_tool_url + self.__LOGINLOAD_PATH
        payload = {
            'code': auth_code,
            'redirect_uri': redirect_uri
        }

        try:
            token_response = requests.post(target_url, headers=headers, json=payload)
        except Exception:
            self.__app.logger.error(traceback.format_exc())
            raise CatalogToolException(
                'post_token_authorization_code_AuthServerError', 500)
                
        if not token_response.status_code == 200:
            self.__app.logger.error('トークン取得エラー')
            self.__app.logger.error(token_response.status_code)
            raise CatalogToolException(
                'post_token_authorization_code_GetTokenError', 500)

        token_response = json.loads(token_response.content.decode())
        self.__app.logger.warning(token_response)
        token_response = {
            auth_code: {
                'access_token': token_response['access_token'],
                'refresh_token': token_response['refresh_token']
            }
        }
        self.__token_list.append(token_response)

        res['status'] = 'success'

        return res

    # トークン検証API実行
    def post_token_introspect(self, auth_code):
        self.__app.logger.warning('トークン検証API実行')
        res = {
            'status': 'error',
            'user_id': ''
        }

        # コンフィグからkeycloak情報を取得
        auth_server_url = self.__get_catalog_tool_config('auth_server_url')
        keycloak_client_id = self.__get_catalog_tool_config('client_id')
        keycloak_client_secret = self.__get_catalog_tool_config('client_secret')
        if not auth_server_url or not keycloak_client_id or not keycloak_client_secret:
            raise CatalogToolException(
                'post_token_introspect_ConfigError', 500)

        target_url = auth_server_url + self.__POST_TOKEN_INTROSPECT
        credential =  f'{keycloak_client_id}:{keycloak_client_secret}'
        bearer = base64.b64encode(credential.encode()).decode()
        headers = {'Authorization': f'Basic {bearer}'}

        access_token = ''
        for token_info in self.__token_list:
            if auth_code in token_info.keys():
                access_token = token_info[auth_code]['access_token']
                break
        if not access_token:
            # 引数のauth_codeがtoken_listに含まれていない場合、エラー
            raise CatalogToolException(
                'post_token_introspect_NotMatchCode', 500)

        payload = {
            'access_token': access_token
        }

        try:
            introspect_result = requests.post(
                target_url, headers=headers, json=payload)
        except Exception:
            raise CatalogToolException(
                'post_token_introspect_AuthServerError', 500)

        if not introspect_result.status_code == 200:
            self.__app.logger.error('トークン検証エラー')
            self.__app.logger.error(introspect_result.status_code)
            raise CatalogToolException(
                'post_token_introspect_IntrospectError', 500)

        introspect_result = json.loads(introspect_result.content.decode())
        self.__app.logger.warning(introspect_result)
        self.__cadde_user_id = introspect_result['user_id']
        res['user_id'] = introspect_result['user_id']
        res['status'] = 'success'

        return res

    # トークン更新API実行
    def post_token_refresh(self, auth_code):
        self.__app.logger.warning('トークン更新API実行')
        res = {
            'status': 'error',
            'access_token': ''
        }

        # コンフィグからkeycloak情報を取得
        auth_server_url = self.__get_catalog_tool_config('auth_server_url')
        keycloak_client_id = self.__get_catalog_tool_config('client_id')
        keycloak_client_secret = self.__get_catalog_tool_config('client_secret')
        if not auth_server_url or not keycloak_client_id or not keycloak_client_secret:
            raise CatalogToolException(
                'post_token_refresh_ConfigError', 500)

        target_url = auth_server_url + self.__POST_TOKEN_REFRESH
        credential =  f'{keycloak_client_id}:{keycloak_client_secret}'
        bearer = base64.b64encode(credential.encode()).decode()
        headers = {'Authorization': f'Basic {bearer}'}

        old_refresh_token = ''
        for token_info in self.__token_list:
            if auth_code in token_info.keys():
                old_refresh_token = token_info[auth_code]['refresh_token']
        if not old_refresh_token:
            # 引数のauth_codeがtoken_listに含まれていない場合、エラー
            raise CatalogToolException('post_token_refresh_NotMatchCode', 500)

        if not old_refresh_token:
            # 旧版カタログ作成ツールの来歴認証対応
            # token_infoにトークン設定が設定されていない場合は、refresh_tokenを空にして返す
            res['refresh_token'] = ''
            res['status'] = 'success'
            return res

        payload = {
            'refresh_token': old_refresh_token
        }

        try:
            token_response = requests.post(target_url, headers=headers, json=payload)
        except Exception:
            raise CatalogToolException(
                'post_token_refresh_AuthServerError', 500)

        if not token_response.status_code == 200:
            self.__app.logger.error('トークン更新エラー')
            self.__app.logger.error(token_response.status_code)
            raise CatalogToolException(
                'post_token_refresh_TokenRefreshError', 500)

        token_response = json.loads(token_response.content.decode())
        self.__app.logger.warning(token_response)
        for token_info in self.__token_list:
            if auth_code in token_info.keys():
                token_info[auth_code]['access_token'] = token_response['access_token']
                token_info[auth_code]['refresh_token'] = token_response['refresh_token']
                break

        res['access_token'] = token_response['access_token']
        res['status'] = 'success'

        return res

    # keycloakログアウト
    def logout_keycloak(self, auth_code):
        self.__app.logger.warning('keycloakログアウト実行')

        # コンフィグからkeycloak情報を取得
        auth_server_url = self.__get_catalog_tool_config('auth_server_url')
        keycloak_endpoint = self.__get_catalog_tool_config('keycloak_endpoint')
        keycloak_client_id = self.__get_catalog_tool_config('client_id')
        keycloak_client_secret = self.__get_catalog_tool_config('client_secret')
        if not auth_server_url or not keycloak_endpoint or not keycloak_client_id or not keycloak_client_secret:
            raise CatalogToolException(
                'logout_keycloak_Exception', 500)

        target_url = auth_server_url + keycloak_endpoint + self.__KETCLOAK_LOGOUT
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # リフレッシュトークン取得
        refresh_token = ''
        for token_info in self.__token_list:
            if auth_code in token_info.keys():
                refresh_token = token_info[auth_code]['refresh_token']
                break
        if not refresh_token:
            raise CatalogToolException(
                'logout_keycloak_NotMatchCode', 500)

        payload = {
            'client_id': keycloak_client_id,
            'client_secret': keycloak_client_secret,
            'refresh_token': refresh_token
        }
        payload = urllib.parse.urlencode(payload)

        try:
            keycloak_response = requests.post(target_url, headers=headers, data=payload)
        except Exception:
            raise CatalogToolException(
                'logout_keycloak_KeycloakError', 500)

        if not keycloak_response.status_code == 204:
            self.__app.logger.error('keycloakログアウトエラー')
            self.__app.logger.error(keycloak_response.status_code)
            raise CatalogToolException(
                'logout_keycloak_KeycloakLogoutError', 500)

        return

    # トークン情報削除
    def delete_token(self, auth_code):
        self.__app.logger.warning('トークン情報削除実行')

        for index, token_info in enumerate(self.__token_list):
            if auth_code in token_info.keys():
                del self.__token_list[index]
                break
        return
