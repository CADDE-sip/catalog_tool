import csv
import json
import traceback
import os
import grpc
from flask import Flask, jsonify, request, send_file, make_response, request
import flask_login
from functools import wraps

# 自作モジュール
from ckan_user_manager import get_ckan_user_release
from ckan_user_manager import get_ckan_user_detail
from ckan_user_manager import get_ckan_user
from ckan_user_manager import get_ckan_user_org
from ckan_user_manager import fetch_ckan_userlist
from ckan_user_manager import create_ckan_user
from ckan_user_manager import update_ckan_user
from ckan_user_manager import update_ckan_user_password
from ckan_user_manager import delete_ckan_user
from grpc_protocol import ml_analysis_pb2
from grpc_protocol import ml_analysis_pb2_grpc
from ckan_catalog_manager import regist_release
from ckan_catalog_manager import regist_detail
from ckan_catalog_manager import regist_both
from ckan_catalog_manager import edit_release
from ckan_catalog_manager import edit_detail
from ckan_catalog_manager import edit_both
from ckan_catalog_manager import search_both
from ckan_catalog_manager import search_release
from ckan_catalog_manager import search_detail
from ckan_catalog_manager import get_ckan_info
from ckan_catalog_manager import get_license_list
from ckan_catalog_manager import delete_catalogs
from ckan_catalog_manager import search_auto_correct_catalog
from ckan_catalog_manager import search_auto_correct_resource
from ckan_dataset_manager import CkanDataset
from data_uploader import http_get
from data_uploader import ftp_get
from data_uploader import url_upload
from history_manager import search_history
from extract_spatial import FindByKeyword_name, getFullname
from temporal_saver import write_tmp_data
from temporal_saver import get_tmp_data_files
from temporal_saver import delete_tmp_data
from template_manager import CatalogTemplate
from ngsi_manager import NgsiData
from cadde_auth_manager import CaddeAuth
from postgres_manager import Postgres
from ckan_auth_manager import authenticate_ckan_user
from catalogtool_exception import CatalogToolException

os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)

# 開発環境の指定
prefix_uri = '/api/v1/catalog/tool'
SAVE_DIR_PATH = 'data/'

# Setting file の読み込み
app = Flask(__name__, static_folder='app', template_folder='app/')
app.secret_key = 'secret'
app.config.update(
  # SESSION_COOKIE_SECURE=True,
  SESSION_COOKIE_SAMESITE='Lax'
)
host = os.getenv('APP_ADDRESS', '0.0.0.0')
port = os.getenv('APP_PORT', 18000)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

cadde_auth = CaddeAuth(app)

# configデータ取得


def __get_catalog_tool_config(config_key):
    """コンフィグデータの取得

    Args：
      取得するコンフィグのキー

    Returns:
      コンフィグデータ
    """
    # jsonファイルの読み込み
    config_file_path = './config.json'
    config = open(config_file_path, 'r')
    config = json.load(config)

    if config_key == 'grpc_server':
        return config['server']['grpc']
    elif config_key == 'ngsi_server':
        return config['server']['ngsi']
    elif config_key == 'ckan_auth':
        return config['server']['ckan_authentication']
    elif config_key == 'use_geonames':
        return config['geonames']['use_geonames']
    elif config_key == 'theme':
        return config['machine_learn']['theme']
    elif config_key == 'keyword':
        return config['machine_learn']['keyword']
    elif config_key == 'spatial':
        return config['machine_learn']['spatial']
    elif config_key == 'temporal':
        return config['machine_learn']['temporal']

    return config[config_key]


# データセットインポートエクスポート
ckan_dataset = CkanDataset(app)
ckan_dataset.start()

# user_manager #


class User(flask_login.UserMixin):
    """ユーザクラス

    Attributes
    ----------
    username : String
        ユーザ名
    sysadmin : Boolean
        sysadminか否か

    Methods
    -------
    get_id():
        ユーザ名を返す
    """

    release_user_id = None
    detail_user_id = None
    username = None
    sysadmin = None
    organization = None
    ckan = None
    release_ckan_url = None
    release_ckan_username = None
    release_ckan_apikey = None
    detail_ckan_url = None
    detail_ckan_username = None
    detail_ckan_apikey = None

    def get_id(self):
        return self.username


def sysadmin_required(f):
    """sysadmin用アクセス制御デコレータ
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        if not hasattr(flask_login.current_user, 'is_authenticated'):
            return login_manager.unauthorized()
        if flask_login.current_user.is_authenticated is True:
            if flask_login.current_user.sysadmin is True:
                return f(*args, **kwargs)
            else:
                return login_manager.unauthorized()
        else:
            return login_manager.unauthorized()

    return wrap


@login_manager.user_loader
def load_user(username):
    """flask-loginの内部関数

    ログイン済かを判定する

    Args:
        username: ユーザ名

    Returns:
        user: ユーザ情報

    Raises:
        Exception: 例外
    """
    app.logger.warning('load_user')
    app.logger.warning(username)

    user = User()
    try:
        # コンフィグ値取得
        ckans = __get_catalog_tool_config('ckan_info')

        # CKANユーザ情報取得
        user_info = get_ckan_user(app, username, None, ckans['release'], ckans['detail'])
        app.logger.warning(user_info)

        if not user_info['status'] == 'success':
            app.logger.error(traceback.format_exc())
            return jsonify({'message': user_info['message']}), 400

        user.release_user_id = user_info['release_user_id']
        user.detail_user_id = user_info['detail_user_id']
        user.username = user_info['username']
        user.sysadmin = user_info['sysadmin']
        user.organization = user_info['organization'].split(',')
        user.ckan = user_info['ckan']

        user.release_ckan_url = user_info['about']['release_ckan_url']
        user.release_ckan_username = user_info['about']['release_ckan_username']
        user.release_ckan_apikey = user_info['about']['release_ckan_apikey']

        user.detail_ckan_url = user_info['about']['detail_ckan_url']
        user.detail_ckan_username = user_info['about']['detail_ckan_username']
        user.detail_ckan_apikey = user_info['about']['detail_ckan_apikey']

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'ロードユーザ時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'load_user_Exception'}), 500

    return user


@app.route(prefix_uri + '/login', methods=['POST'])
def login():
    """ログイン

    CADDE認証後、カタログ作成ツールおよびCKANにログインする

    Args:
      dict:
        - cadde_user_id: CADDEユーザID
        - cadde_password: CADDEユーザパスワード
        - ckan_username: CKANユーザ名

    Returns:
      dict: ログイン結果
        - sysadmin: sysadmin判定（true | false）
        - ckan: CKAN種別（internal | external）
        - release_ckan_addr: 横断検索カタログサイトURL
        - detail_ckan_addr: 詳細検索カタログサイトURL
        - message: メッセージ

    Raises:
        Exception: 例外
    """

    app.logger.warning('ログイン')
    app.logger.warning(request)
    ckanUsername = request.json['username']
    ckanUserPassword = request.json['password']
    res = dict()
    user = User()

    try:

        # コンフィグ値取得
        ckans = __get_catalog_tool_config('ckan_info')

        # 認可コード発行(来歴認証対応のため、適当な値を設定）
        auth_response = cadde_auth.create_dummy_auth_code()

        # CKANのユーザ確認
        user_info = get_ckan_user(app, ckanUsername, ckanUserPassword, ckans['release'], ckans['detail'])

        # CKAN情報設定
        user.username = ckanUsername
        user.sysadmin = user_info['sysadmin']
        user.ckan = user_info['ckan']
        user.release_ckan_url = user_info['about']['release_ckan_url']
        user.release_ckan_username = user_info['about']['release_ckan_username']
        user.release_ckan_apikey = user_info['about']['release_ckan_apikey']

        user.detail_ckan_url = user_info['about']['detail_ckan_url']
        user.detail_ckan_username = user_info['about']['detail_ckan_username']
        user.detail_ckan_apikey = user_info['about']['detail_ckan_apikey']

        # ログイン処理
        flask_login.login_user(user, remember=False,
                               duration=None, force=False, fresh=True)

        # 応答
        res['message'] = 'login_Success'
        res['sysadmin'] = user.sysadmin
        res['ckan'] = user.ckan
        res['release_ckan_addr'] = user.release_ckan_url
        res['detail_ckan_addr'] = user.detail_ckan_url
        res['auth_code'] = auth_response['code']

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'ログイン時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。', 'message_id': 'login_Exception'}), 500

    return jsonify(res), 200


@app.route(prefix_uri + '/auth/login', methods=['POST'])
def auth_login():
    """認証ログイン

    CADDE認証後、カタログ作成ツールおよびCKANにログインする

    Args:
      dict:
        - cadde_user_id: CADDEユーザID
        - cadde_password: CADDEユーザパスワード
        - ckan_username: CKANユーザ名

    Returns:
      dict: ログイン結果
        - sysadmin: sysadmin判定（true | false）
        - ckan: CKAN種別（internal | external）
        - release_ckan_addr: 横断検索カタログサイトURL
        - detail_ckan_addr: 詳細検索カタログサイトURL
        - message: メッセージ

    Raises:
        Exception: 例外
    """

    app.logger.warning('認証ログイン')
    data = request.data.decode('utf-8')
    data = json.loads(data)
    keycloak_uuid = data['keycloak_uuid']
    auth_code = data['auth_code']
    catalog_tool_url = data['catalog_tool_url']
    res = dict()
    user = User()

    try:

        # コンフィグ値取得
        ckans = __get_catalog_tool_config('ckan_info')
        config_postgres = __get_catalog_tool_config('postgres')
        sysadmin = __get_catalog_tool_config('sysadmin')
        ckan_auth = __get_catalog_tool_config('ckan_auth')

        # カタログ作成ツールのアプリサーバで生成したUUIDとkeycloakのレスポンスで取得したUUIDが一致することを確認
        if keycloak_uuid in cadde_auth.auth_state_list:
            cadde_auth.auth_state_list.remove(keycloak_uuid)
        else:
            raise CatalogToolException('login_NotMatchUUID', 500)

        # トークン要求API実行
        cadde_auth.post_token_authorization_code(
            auth_code, catalog_tool_url)

        # トークン検証API実行
        cadde_info = cadde_auth.post_token_introspect(auth_code)
        if cadde_info['status'] == 'error':
            raise CatalogToolException('post_token_introspect_Exception', 500)
        cadde_user_id = cadde_info['user_id']

        # CADDEユーザ情報からCKANユーザ情報を取得
        cadde_user_id_list = []
        # CKANユーザ種別が運用管理者ユーザ
        if cadde_user_id in sysadmin['cadde_user_id']:
            ckan_username = sysadmin['ckan_username']
            ckan_user_password = sysadmin['ckan_user_password']
            cadde_user_id_list = sysadmin['cadde_user_id']

        # CKANユーザ種別が提供者ユーザ
        else:
            postgres = Postgres(app, config_postgres)
            db_res = postgres.get_ckan_user_info(cadde_user_id)
            ckan_username = db_res['ckan_username']
            ckan_user_password = db_res['ckan_user_password']
            cadde_user_id_list.append(cadde_user_id)

        # CKAN認証
        # 横断検索用CKANユーザ
        if ckans['release']['authentication']:
            if not ckans['release']['ckan_url']:
                app.logger.warning('横断検索用内部CKANユーザ：CKAN URL情報なし')
                raise CatalogToolException('authenticate_ckan_user_ConfigError', 500)
            release_ckan_url = ckans['release']['ckan_url']
            if not ckans['release']['authentication_method']:
                app.logger.warning('横断検索用内部CKANユーザ：認証方式の指定なし')
                raise CatalogToolException('authenticate_ckan_user_ConfigError', 500)
            auth_method = ckans['release']['authentication_method']
            auth_server_url = ''
            for label in ckan_auth.keys():
                if auth_method == label and ckan_auth[label]:
                    auth_server_url = ckan_auth[label]
                    break
            if not auth_server_url:
                app.logger.warning('横断検索用内部CKANユーザ：指定した認証方式に該当する認証情報なし')
                raise CatalogToolException('authenticate_ckan_user_ConfigError', 500)

            authenticate_ckan_user(app, release_ckan_url, ckan_username, auth_server_url, 'release')
        

        # 詳細検索用CKANユーザ
        if ckans['detail']['authentication']:
            if not ckans['detail']['ckan_url']:
                app.logger.warning('詳細検索用内部CKANユーザ：CKAN URL情報なし')
                raise CatalogToolException('authenticate_ckan_user_ConfigError', 500)
            detail_ckan_url = ckans['detail']['ckan_url']
            if not ckans['detail']['authentication_method']:
                app.logger.warning('詳細検索用内部CKANユーザ：認証方式の指定なし')
                raise CatalogToolException('authenticate_ckan_user_ConfigError', 500)
            auth_method = ckans['detail']['authentication_method']
            auth_server_url = ''
            for label in ckan_auth.keys():
                if auth_method == label and ckan_auth[label]:
                    auth_server_url = ckan_auth[label]
                    break
            if not auth_server_url:
                app.logger.warning('詳細検索用内部CKANユーザ：指定した認証方式に該当する認証情報なし')
                raise CatalogToolException('authenticate_ckan_user_ConfigError', 500)

            authenticate_ckan_user(app, detail_ckan_url, ckan_username, auth_server_url, 'detail')

        # CKANログイン情報取得
        user_info = get_ckan_user(app, ckan_username, ckan_user_password, ckans['release'], ckans['detail'])

        # CKANユーザ情報設定
        app.logger.warning('CKANユーザ情報設定 username:%s', ckan_username)
        user.username = ckan_username
        user.sysadmin = user_info['sysadmin']
        user.ckan = user_info['ckan']
        user.release_ckan_url = user_info['about']['release_ckan_url']
        user.release_ckan_username = user_info['about']['release_ckan_username']
        user.release_ckan_apikey = user_info['about']['release_ckan_apikey']

        user.detail_ckan_url = user_info['about']['detail_ckan_url']
        user.detail_ckan_username = user_info['about']['detail_ckan_username']
        user.detail_ckan_apikey = user_info['about']['detail_ckan_apikey']

        # 外部CKANユーザ認証
        if user.ckan == 'external':
            # 横断検索用CKANユーザ
            if 'release_ckan_auth_method' in user_info['about'] and user_info['about']['release_ckan_auth_method']:
                auth_server_url = ''
                for label in ckan_auth.keys():
                    if user_info['about']['release_ckan_auth_method'] == label and ckan_auth[label]:
                        auth_server_url = ckan_auth[label]
                        break
                if not auth_server_url:
                    app.logger.warning('横断検索用外部CKANユーザ：指定した認証方式に該当する認証情報なし')
                    raise CatalogToolException('authenticate_ckan_user_ConfigError', 500)

                authenticate_ckan_user(app, user.release_ckan_url, user.release_ckan_username, auth_server_url, 'release')

            # 詳細検索用CKANユーザ
            if 'detail_ckan_auth_method' in user_info['about'] and user_info['about']['detail_ckan_auth_method']:
                auth_server_url = ''
                for label in ckan_auth.keys():
                    if user_info['about']['detail_ckan_auth_method'] == label and ckan_auth[label]:
                        auth_server_url = ckan_auth[label]
                        break
                if not auth_server_url:
                    app.logger.warning('詳細検索用外部CKANユーザ：指定した認証方式に該当する認証情報なし')
                    raise CatalogToolException('authenticate_ckan_user_ConfigError', 500)

                authenticate_ckan_user(app, user.detail_ckan_url, user.detail_ckan_username, auth_server_url, 'detail')
            

        # flaskログイン処理
        flask_login.login_user(user, remember=False,
                               duration=None, force=False, fresh=True)

        # レスポンス設定
        res['message'] = 'login_Success'
        res['sysadmin'] = user.sysadmin
        res['ckan'] = user.ckan
        res['release_ckan_addr'] = user.release_ckan_url
        res['detail_ckan_addr'] = user.detail_ckan_url
        res['cadde_user_id'] = cadde_user_id
        res['cadde_user_id_list'] = cadde_user_id_list
        res['ckan_username'] = ckan_username

        # Cookie設定
        response = make_response(res)
        # response.set_cookie('session_id', value=auth_code, secure=True, samesite='Lax')
        response.set_cookie('session_id', value=auth_code, samesite='Lax')
        # response.set_cookie('session_id', value=auth_code)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'ログイン時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。', 'message_id': 'login_Exception'}), 500

    # return jsonify(res), 200
    return response, 200


@app.route(prefix_uri + '/keycloak/redirect', methods=['POST'])
def redirect_keycloak():
    """keycloakリダイレクト
    keycloakのログイン画面にリダイレクトする

    Returns:
      dict: keycloakログイン画面アクセス情報
        - keycloak_url: keycloak画面URL
        - client_id: keycloakのクライアントID
        - encoded_catalog_tool_url: カタログ作成ツールのログインロード画面のエンコードURL
        - catalog_tool_uuid: keycloakログイン画面URLに設定するUUID

    Raises:
        Exception: 例外

    """
    app.logger.warning('keycloakリダイレクト')

    try:
        data = json.loads(request.data.decode('utf-8'))
        res = cadde_auth.create_keycloak_redirect_uri(data['catalog_tool_url'])

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'keycloakリダイレクト時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'redirect_keycloak_Exception'}), 500

    return jsonify(res), 200


@app.route(prefix_uri + '/logout', methods=['GET'])
@flask_login.login_required
def logout():
    """ログアウト

    ログアウトする

    Returns:
      dict: ログアウト結果
        - message: メッセージ
        - error: エラーメッセージ

    Raises:
        Exception: 例外
    """

    app.logger.warning('ログアウト')
    try:
        auth_code = request.cookies.get('session_id')
        # keycloakログアウト
        cadde_auth.logout_keycloak(auth_code)

        # アプリケーションサーバで保持しているトークン情報の削除
        cadde_auth.delete_token(auth_code)     

        # flaskログアウト
        flask_login.logout_user()
        logout_res = {'message': 'ログアウトに成功しました。', 'message_id': 'logout_Success'}

        # Cookieからsession_idを削除
        response = make_response(logout_res)
        response.delete_cookie('session_id')
        return response, 200
    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'ログアウト時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'logout_Exception'}), 500


@app.route(prefix_uri + '/userlist', methods=['GET'])
@sysadmin_required
def fetch_userlist():
    """ユーザ一覧取得

    ユーザ一覧を取得する

    Returns:
      dict: ユーザ一覧取得結果
        - result: CKAN問い合わせの成否
        - userlist: ユーザ情報のリスト
          - dict: ユーザ情報
            - name: ユーザ名
            - sysadmin: sysadmin判定（true | false）
            - status: ユーザ状態（active | deleted）
            - created: 作成日
            - email: メールアドレス
            - organization: 組織情報
            - cadde_user_id: CADDEユーザIDのリスト
            - about: ユーザ付加情報
        - message: メッセージ
        - error: エラー
    """

    app.logger.warning('ユーザ一覧取得')

    try:
        # コンフィグ値取得
        ckans = __get_catalog_tool_config('ckan_info')
        config_postgres = __get_catalog_tool_config('postgres')

        # CKANからユーザ一覧取得
        res = fetch_ckan_userlist(app, ckans['release'], ckans['detail'])

        # CKANから取得したユーザ一覧データ調整
        postgres = Postgres(app, config_postgres)
        for user in res['userlist']:
            # CKANユーザ名をキーにDBからCADDEユーザIDを取得
            db_res = postgres.get_cadde_user_id(user['name'])
            user['cadde_user_id'] = ','.join(db_res['cadde_id_list'])

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'ユーザ一覧取得時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'fetch_userlist_Exception'}), 500

    return jsonify(res), 200


@app.route(prefix_uri + '/users/<username>', methods=['GET'])
@sysadmin_required
def fetch_user(username):
    """ユーザ取得

    ユーザを取得する

    Args:
      username: ユーザ名

    Returns:
      dict: ユーザ情報
        - username: ユーザ名
        - sysadmin: sysadmin判定（true | false）
        - apikey: アプリキー
        - email: メールアドレス
        - organization: 組織情報のリスト
        - cadde_user_id: CADDEユーザIDのリスト
        - status: ユーザ取得状態
        - ckan: 登録先カタログサイト（internal | external）
        - about: ユーザ付加情報
          - release_ckan_url: 外部横断検索カタログサイトURL
          - release_ckan_username: 外部横断検索カタログサイトユーザ名
          - release_ckan_apikey: 外部横断検索カタログサイトアプリキー
          - detail_ckan_url: 外部詳細検索カタログサイトURL
          - detail_ckan_username: 外部詳細検索カタログサイトユーザ名
          - detail_ckan_apikey: 外部詳細検索カタログサイトアプリキー
        - message: メッセージ
        - release_user_id: 横断検索カタログサイトユーザID
        - detail_user_id: 詳細検索カタログサイトユーザID
    """

    app.logger.warning('ユーザ取得')
    app.logger.warning(username)

    try:
        # コンフィグ値取得
        ckans = __get_catalog_tool_config('ckan_info')

        # CKANのユーザ情報取得
        user_info = get_ckan_user(app, username, None, ckans['release'], ckans['detail'])
        config_postgres = __get_catalog_tool_config('postgres')

        # CKANユーザ名をキーにDBからCADDEユーザIDを取得
        postgres = Postgres(app, config_postgres)
        db_res = postgres.get_cadde_user_id(user_info['username'])
        user_info['cadde_user_id'] = ','.join(db_res['cadde_id_list'])

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'ユーザ取得時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'users_Exception'}), 500

    return jsonify(user_info), 200


@app.route(prefix_uri + '/users', methods=['POST'])
@sysadmin_required
def create_user():
    """ユーザ作成

    ユーザを作成する

    Args:
      dict:
        - organization: 組織名
        - username: CKANユーザ名
        - email: メールアドレス
        - password: CKANパスワード
        - caddeUserId: CADDEユーザID
        - releaseCkanUrl: 外部横断検索カタログサイトURL
        - releaseCkanApikey: 外部横断検索カタログサイトアプリキー
        - releaseCkanUsername: 外部横断検索カタログサイトユーザ名
        - detailCkanUrl: 外部詳細検索カタログサイトURL
        - detailCkanApikey: 外部詳細検索カタログサイトアプリキー
        - detailCkanUsername: 外部詳細検索カタログサイトユーザ名

    Returns:
      dict:
        - message: メッセージ
        - status: ユーザ作成の成否
    """

    app.logger.warning('ユーザ作成')

    try:
        req = request.get_json()
        app.logger.warning(req)
        if 'username' not in req or not req['username']:
            raise CatalogToolException('create_user_NoUsername', 400)
        if 'password' not in req or not req['password']:
            raise CatalogToolException('create_user_NoPassword', 400)
        if 'caddeUserId' not in req or not req['caddeUserId']:
            raise CatalogToolException('create_user_NoCaddeUserId', 400)
        if 'email' not in req or not req['email']:
            raise CatalogToolException('create_user_NoEmail', 400)
        if 'organization' not in req or (req['ckan'] == 'internal' and not req['organization']):
            raise CatalogToolException('create_user_NoOrganization', 400)
        if 'ckan' not in req or (not req['ckan'] == 'internal' and not req['ckan'] == 'external'):
            raise CatalogToolException('create_user_NoCkan', 400)

        # コンフィグ値取得
        ckans = __get_catalog_tool_config('ckan_info')
        config_postgres = __get_catalog_tool_config('postgres')

        # 横断CKANのユーザ情報取得
        release_user_info = None
        try:
            release_user_info = get_ckan_user_release(
                app, req['username'], None, ckans['release'])
        except CatalogToolException as e:
            if e.message_id == 'get_ckan_user_release_NotFound':
                pass
            elif e.message_id == 'get_ckan_user_release_DisableUser':
                app.logger.warning('CKANユーザ作成 横断検索用CKAN 削除済みユーザ')
                raise CatalogToolException(
                    'create_ckan_user_release_DuplicateDeletedUser', 400)
            else:
                raise e
        # 横断CKANからユーザ情報が取得できた場合、ユーザ作成エラー
        if release_user_info and release_user_info['status'] == 'success':
            app.logger.warning('CKANユーザ作成 横断検索用CKAN 登録済みユーザ')
            raise CatalogToolException(
                'create_ckan_user_release_AlreadyExist', 409)

        # 詳細CKANのユーザ情報取得
        detail_user_info = None
        try:
            detail_user_info = get_ckan_user_detail(
                app, req['username'], None, ckans['detail'])
        except CatalogToolException as e:
            if e.message_id == 'get_ckan_user_detail_NotFound':
                pass
            elif e.message_id == 'get_ckan_user_release_DisableUser':
                app.logger.warning('CKANユーザ作成 詳細検索用CKAN 削除済みユーザ')
                raise CatalogToolException(
                    'create_ckan_user_detail_DuplicateDeletedUser', 400)
            else:
                raise e
        # 詳細CKANからユーザ情報が取得できた場合、ユーザ作成エラー
        if detail_user_info and detail_user_info['status'] == 'success':
            app.logger.warning('CKANユーザ作成 詳細検索用CKAN 登録済みユーザ')
            raise CatalogToolException(
                'create_ckan_user_detail_AlreadyExist', 409)

        # ユーザレコードをDBに追加
        try:
            postgres = Postgres(app, config_postgres)
            postgres.add_new_record(
                req['username'], req['password'], req['caddeUserId'])
        except Exception as e:
            # DBエラーの場合は処理終了
            return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

        # CKANにユーザ登録
        res = create_ckan_user(app, ckans['release'], ckans['detail'], req)

    except CatalogToolException as e:
        try:
            postgres = Postgres(app, postgres)
            postgres.delete_record(req['username'])
        except Exception:
            app.logger.error('例外処理でDBからユーザレコードの削除に失敗')
            app.logger.error(traceback.format_exc())

        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        # DBから登録したユーザレコードを削除
        try:
            postgres = Postgres(app, postgres)
            postgres.delete_record(req['username'])
        except Exception:
            app.logger.error('例外処理でDBからユーザレコードの削除に失敗')
            app.logger.error(traceback.format_exc())

        return jsonify({'message': 'ユーザ作成時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'create_user_Exception'}), 500

    return jsonify(res), 200


@app.route(prefix_uri + '/users', methods=['PUT'])
@sysadmin_required
def update_user():
    """ユーザ更新

    ユーザを更新する

    Args:
      dict:
        - organization: 組織名
        - username: ユーザ名
        - email: メールアドレス
        - password: パスワード
        - caddeUserId: CADDEユーザID
        - releaseCkanUrl: 外部横断検索カタログサイトURL
        - releaseCkanApikey: 外部横断検索カタログサイトアプリキー
        - releaseCkanUsername: 外部横断検索カタログサイトユーザ名
        - detailCkanUrl: 外部詳細検索カタログサイトURL
        - detailCkanApikey: 外部詳細検索カタログサイトアプリキー
        - detailCkanUsername: 外部詳細検索カタログサイトユーザ名

    Returns:
      dict: ユーザ更新結果
        - status: ユーザ更新の成否
        - message: メッセージ

    Raises:
        Exception: 例外
    """

    app.logger.warning('ユーザ更新')

    try:
        req = request.get_json()
        app.logger.warning(req)
        if 'username' not in req or not req['username']:
            raise CatalogToolException('update_user_NoUsername', 400)
        if 'password' not in req or not req['password']:
            raise CatalogToolException('update_user_NoPassword', 400)
        if 'caddeUserId' not in req or not req['caddeUserId']:
            raise CatalogToolException('update_user_NoCaddeUserId', 400)
        if 'email' not in req or not req['email']:
            raise CatalogToolException('update_user_NoEmail', 400)
        if 'organization' not in req or (req['ckan'] == 'internal' and not req['organization']):
            raise CatalogToolException('update_user_NoOrganization', 400)
        if 'ckan' not in req or (not req['ckan'] == 'internal' and not req['ckan'] == 'external'):
            raise CatalogToolException('update_user_NoCkan', 400)
        if req['ckan'] == 'external':
            # 外部カタログサイトを使用する場合、以下のフィールドが必須（値は空を許容する）
            if 'releaseCkanUrl' not in req:
                raise CatalogToolException('update_user_NoReleaseCkanUrl', 400)
            if 'releaseCkanApikey' not in req:
                raise CatalogToolException(
                    'update_user_NoReleaseCkanApikey', 400)
            if 'releaseCkanUsername' not in req:
                raise CatalogToolException(
                    'update_user_NoReleaseCkanUsername', 400)
            if 'detailCkanUrl' not in req:
                raise CatalogToolException('update_user_NoDetailCkanUrl', 400)
            if 'detailCkanApikey' not in req:
                raise CatalogToolException(
                    'update_user_NoDetailCkanApikey', 400)
            if 'detailCkanUsername' not in req:
                raise CatalogToolException(
                    'update_user_NodDtailCkanUsername', 400)

        # コンフィグ値取得
        ckans = __get_catalog_tool_config('ckan_info')
        config_postgres = __get_catalog_tool_config('postgres')

        # ユーザ情報DBを更新
        postgres = Postgres(app, config_postgres)
        postgres.update_record(
            req['username'], req['password'], req['caddeUserId'])

        res = update_ckan_user(app, ckans['release'], ckans['detail'], req)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'ユーザ更新時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'update_user_Exception'}), 500

    return jsonify(res), 200


@app.route(prefix_uri + '/users/password', methods=['PUT'])
@sysadmin_required
def update_user_password():
    """ユーザパスワード更新

    ユーザのパスワードを更新する

    Args:
      dict:
        - email: メールアドレス
        - password: パスワード

    Returns:
      dict: ユーザパスワード更新結果
        - result: ユーザパスワード更新の成否
        - message: メッセージ
          - release: 横断検索カタログサイトに対してのユーザパスワード更新メッセージ
          - detail: 詳細検索カタログサイトに対してのユーザパスワード更新メッセージ
        - error: エラーメッセージ

    Raises:
        Exception: 例外
    """

    app.logger.warning('ユーザパスワード更新')

    try:
        req = request.get_json()
        app.logger.warning(req)
        if 'username' not in req or not req['username']:
            raise CatalogToolException('update_user_password_NoUsername', 400)
        if 'old_password' not in req or not req['old_password']:
            raise CatalogToolException(
                'update_user_password_NoOldPassword', 400)
        if 'new_password' not in req or not req['new_password']:
            raise CatalogToolException(
                'update_user_password_NoNewPassword', 400)
        if 'email' not in req or not req['email']:
            raise CatalogToolException('update_user_password_NoEmail', 400)

        # コンフィグ値取得
        ckans = __get_catalog_tool_config('ckan_info')
        config_postgres = __get_catalog_tool_config('postgres')

        # CKANのユーザ情報パスワードを更新
        res = update_ckan_user_password(app, ckans['release'], ckans['detail'], req)

        # ユーザ情報DBのパスワード情報更新
        postgres = Postgres(app, config_postgres)
        postgres.update_password(req['username'], req['new_password'])

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'ユーザパスワード更新時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'update_user_password_Exception'}), 500

    return jsonify(res), 200


@app.route(prefix_uri + '/users/<username>', methods=['DELETE'])
@sysadmin_required
def delete_user(username):
    """ユーザ削除

    ユーザを削除する

    Returns:
      dict: ユーザ削除結果
        - result: delete_ckan_user()の成否
        - message: メッセージ
          - release: 横断検索カタログサイトに対してのユーザ削除メッセージ
          - detail: 詳細検索カタログサイトに対してのユーザ削除メッセージ
        - error: エラーメッセージ
    """

    app.logger.warning('ユーザ削除')
    app.logger.warning(username)

    try:
        # コンフィグ値取得
        ckans = __get_catalog_tool_config('ckan_info')
        config_postgres = __get_catalog_tool_config('postgres')

        # ユーザ情報をCKANから削除
        res = delete_ckan_user(app, ckans['release'], ckans['detail'], username)

        # ユーザレコードをDBから削除
        postgres = Postgres(app, config_postgres)
        postgres.delete_record(username)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'ユーザ削除時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'delete_user_Exception'}), 500

    return jsonify(res), 200


@app.route(prefix_uri + '/ckaninfo', methods=['GET'])
def ckaninfo():
    """ カタログサイト情報取得

    横断CKAN、詳細CKANのCKAN情報を取得する

    Returns:
      list: CKAN情報のリスト
        dict: CKAN情報
          - title: カタログのタイトル
          - description: カタログの説明
          - url: カタログの記載のホームページ
          - ckan_type: CKANタイプ(release | detail)
    """
    app.logger.warning('カタログサイト情報取得')

    try:
        ckan_info = get_ckan_info(app,
                                  flask_login.current_user.release_ckan_apikey,
                                  flask_login.current_user.release_ckan_url,
                                  flask_login.current_user.detail_ckan_apikey,
                                  flask_login.current_user.detail_ckan_url)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'カタログサイト情報取得時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'ckaninfo_Exception'}), 500

    app.logger.warning(ckan_info)
    return jsonify(ckan_info), 200

# 組織情報リスト取得


@app.route(prefix_uri + '/organization', methods=['GET'])
def get_organization_list():
    """ 組織情報取得

    Return:
      list: 組織情報リスト
        dict: 組織情報
          - org_label: 組織情報表示名
          - org_value: 組織情報名
    """

    app.logger.warning('組織情報リスト取得')

    try:
        org_list = get_ckan_user_org(app,
                                     flask_login.current_user.release_ckan_username,
                                     flask_login.current_user.release_ckan_apikey,
                                     flask_login.current_user.release_ckan_url,
                                     flask_login.current_user.detail_ckan_username,
                                     flask_login.current_user.detail_ckan_apikey,
                                     flask_login.current_user.detail_ckan_url)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '組織情報取得時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'get_organization_list_Exception'}), 500

    return jsonify(org_list), 200


@app.route(prefix_uri + '/licenselist', methods=['GET'])
def license_list():
    """ ラインセンスリスト取得

    Return:
      list: ライセンスリスト
        dict: ライセンス情報
          - id: ライセンスID
          - title: タイトル
          - url: ライセンスURL
    """
    app.logger.warning('ラインセンスリスト取得')

    try:

        license_list = get_license_list(app,
                                        flask_login.current_user.release_ckan_apikey,
                                        flask_login.current_user.release_ckan_url,
                                        flask_login.current_user.detail_ckan_apikey,
                                        flask_login.current_user.detail_ckan_url)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'ラインセンスリスト取得時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'licenselist_Exception'}), 500

    # app.logger.warning(license_list)
    return jsonify(license_list), 200


@app.route(prefix_uri + '/datacatalog/release/add', methods=['PUT'])
def regist_release_catalog():
    """ 横断検索カタログ登録

    横断検索カタログを登録する

    Args:
      dict
        - release: 横断検索カタログ用データセット
        - detail: 詳細検索カタログ用データセット

    Returns:
      dict
        - message: 横断検索カタログ登録結果メッセージ
        - release: 横断検索カタログ登録結果
            - ckan_url: 登録した横断検索カタログのURL
            - pkg: 登録した横断検索カタログ情報
        - detail: 詳細検索カタログ登録結果
            - ckan_url: 登録した詳細検索カタログのURL
            - pkg: 登録した詳細検索カタログ情報
    """
    app.logger.warning('横断検索カタログ登録')

    ret = {
        'message': 'error',
        'release': {'ckan_url': None, 'pkg': None},
        'detail': {'ckan_url': None, 'pkg': None}
    }

    try:
        data = request.data.decode('utf-8')
        data = json.loads(data)
        auth_code = request.cookies.get('session_id')
        app.logger.warning(json.dumps(data, indent=2, ensure_ascii=False))
        app.logger.warning('====================')

        # コンフィグ値取得
        history_url = __get_catalog_tool_config('history_url')

        # 横断検索用CKANチェック
        if not flask_login.current_user.release_ckan_apikey or not flask_login.current_user.release_ckan_url:
            raise CatalogToolException(
                'regist_release_catalog_userinfo_NoReleaseCKANInfo', 500)

        # 横断検索カタログデータチェック
        if 'release' not in data or not data['release']:
            raise CatalogToolException(
                'regist_release_catalog_NoReleaseCatalogData', 400)

        # 詳細検索カタログに紐づく横断検索カタログを登録する場合
        if data['release']['selected_mode'] == 'release-link-detail_duplicate':
            # 詳細検索用CKANチェック
            if not flask_login.current_user.detail_ckan_apikey or not flask_login.current_user.detail_ckan_url:
                raise CatalogToolException(
                    'regist_release_catalog_userinfo_NoDetailCKANInfo', 500)

            # 詳細検索カタログデータチェック
            if 'detail' not in data or not data['detail']:
                raise CatalogToolException(
                    'regist_release_catalog_NoDetailCatalogData', 400)

        # リフレッシュトークン更新
        token_response = cadde_auth.post_token_refresh(auth_code)
        access_token = token_response['access_token']

        # 横断検索カタログ登録
        ret = regist_release(app,
                             SAVE_DIR_PATH,
                             data['release'],
                             data['detail'],
                             history_url,
                             access_token,
                             flask_login.current_user.release_ckan_apikey,
                             flask_login.current_user.release_ckan_url,
                             flask_login.current_user.detail_ckan_apikey,
                             flask_login.current_user.detail_ckan_url)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '横断検索カタログ登録時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'regist_release_catalog_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/datacatalog/detail/add', methods=['PUT'])
def regist_detail_catalog():
    """ 詳細検索カタログ登録

    既存の横断検索カタログに紐づいた詳細検索カタログ登録を登録し、詳細検索用データセットIDを紐づける

    Args:
      dict
        - release: 横断検索カタログ用データセット
        - detail: 詳細検索カタログ用データセット

    Returns:
      dict
        - message: 詳細検索カタログ登録・横断検索カタログ編集結果メッセージ
        - release: 横断検索カタログ編集結果
            - ckan_url: 編集した横断検索カタログのURL
            - pkg: 編集した横断検索カタログ情報
        - detail: 詳細検索カタログ登録結果
            - ckan_url: 登録した詳細検索カタログのURL
            - pkg: 登録した詳細検索カタログ情報
    """

    app.logger.warning('詳細検索カタログ登録')

    ret = {
        'message': 'error',
        'release': {'ckan_url': None, 'pkg': None},
        'detail': {'ckan_url': None, 'pkg': None}
    }

    try:
        data = request.data.decode('utf-8')
        data = json.loads(data)
        auth_code = request.cookies.get('session_id')
        app.logger.warning(json.dumps(data, indent=2, ensure_ascii=False))
        app.logger.warning('====================')

        # コンフィグ値取得
        history_url = __get_catalog_tool_config('history_url')

        # 詳細検索用CKANチェック
        if not flask_login.current_user.detail_ckan_apikey or not flask_login.current_user.detail_ckan_url:
            raise CatalogToolException(
                'regist_detail_catalog_userinfo_NoDetailCKANInfo', 500)

        # 詳細検索カタログデータチェック
        if 'detail' not in data or not data['detail']:
            raise CatalogToolException(
                'regist_detail_catalog_NoDetailCatalogData', 400)
            ret['message'] = 'requestdata_detail_NotFound'
            return jsonify(ret), 400

        # 横断検索カタログに紐づく横断検索カタログを登録する場合
        if data['detail']['selected_mode'] == 'detail-link-release_duplicate':
            # 横断検索用CKANチェック
            if not flask_login.current_user.release_ckan_apikey or not flask_login.current_user.release_ckan_url:
                raise CatalogToolException(
                    'regist_detail_catalog_userinfo_NoReleaseCKANInfo', 500)

            # 横断検索カタログデータチェック
            if 'release' not in data or not data['release']:
                raise CatalogToolException(
                    'regist_detail_catalog_NoReleaseCatalogData', 400)

        # リフレッシュトークン更新
        token_response = cadde_auth.post_token_refresh(auth_code)
        access_token = token_response['access_token']

        # 詳細検索カタログ登録
        ret = regist_detail(app,
                            SAVE_DIR_PATH,
                            data['release'],
                            data['detail'],
                            history_url,
                            access_token,
                            flask_login.current_user.release_ckan_apikey,
                            flask_login.current_user.release_ckan_url,
                            flask_login.current_user.detail_ckan_apikey,
                            flask_login.current_user.detail_ckan_url)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '詳細検索カタログ登録時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'regist_detail_catalog_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/datacatalog/add', methods=['PUT'])
def regist_both_catalog():
    """ 横断検索カタログ・詳細検索カタログ登録

    横断検索カタログ・詳細検索カタログ登録を登録し、詳細検索用データセットIDを紐づける

    Args:
      dict
        - release: 横断検索カタログ用データセット
        - detail: 詳細検索カタログ用データセット

    Returns:
      dict
        - message: カタログ登録結果メッセージ
        - release: 横断検索カタログ登録結果
            - ckan_url: 登録した横断検索カタログのURL
            - pkg: 登録した横断検索カタログ情報
        - detail: 詳細検索カタログ登録結果
            - ckan_url: 登録した詳細検索カタログのURL
            - pkg: 登録した詳細検索カタログ情報
    """
    app.logger.warning('横断検索カタログ・詳細検索カタログ登録')

    ret = {
        'message': 'error',
        'release': {'ckan_url': None, 'pkg': None},
        'detail': {'ckan_url': None, 'pkg': None}
    }

    try:
        data = request.data.decode('utf-8')
        data = json.loads(data)
        auth_code = request.cookies.get('session_id')
        app.logger.warning(json.dumps(data, indent=2, ensure_ascii=False))
        app.logger.warning('====================')

        # コンフィグ値取得
        history_url = __get_catalog_tool_config('history_url')

        # 横断検索用CKANチェック
        if not flask_login.current_user.release_ckan_apikey or not flask_login.current_user.release_ckan_url:
            raise CatalogToolException(
                'regist_both_catalog_userinfo_NoReleaseCKANInfo', 500)

        # 横断検索カタログデータチェック
        if 'release' not in data or not data['release']:
            raise CatalogToolException(
                'regist_both_catalog_NoReleaseCatalogData', 400)

        # 詳細検索用CKANチェック
        if not flask_login.current_user.detail_ckan_apikey or not flask_login.current_user.detail_ckan_url:
            raise CatalogToolException(
                'regist_both_catalog_userinfo_NoDetailCKANInfo', 500)

        # 詳細検索カタログデータチェック
        if 'detail' not in data or not data['detail']:
            raise CatalogToolException(
                'regist_both_catalog_NoDetailCatalogData', 400)

        # リフレッシュトークン更新
        token_response = cadde_auth.post_token_refresh(auth_code)
        access_token = token_response['access_token']

        # 横断検索カタログ・詳細検索カタログ登録
        ret = regist_both(app,
                          SAVE_DIR_PATH,
                          data['release'],
                          data['detail'],
                          history_url,
                          access_token,
                          flask_login.current_user.release_ckan_apikey,
                          flask_login.current_user.release_ckan_url,
                          flask_login.current_user.detail_ckan_apikey,
                          flask_login.current_user.detail_ckan_url)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '横断検索カタログ・詳細検索カタログ登録時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'regist_both_catalog_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/datacatalog/release/edit', methods=['PUT'])
def edit_release_catalog():
    """ 横断検索カタログ編集

    横断検索カタログを編集する

    Args:
      dict
        - release: 横断検索カタログ用データセット

    Returns:
      dict
        - message: カタログ編集結果メッセージ
        - release: 横断検索カタログ編集結果
            - ckan_url: 編集した横断検索カタログのURL
            - pkg: 編集した横断検索カタログ情報
    """
    app.logger.warning('横断検索カタログ編集')

    ret = {
        'message': 'error',
        'release': {'ckan_url': '', 'pkg': None}
    }

    try:
        data = request.data.decode('utf-8')
        data = json.loads(data)
        auth_code = request.cookies.get('session_id')
        app.logger.warning(json.dumps(data, indent=2, ensure_ascii=False))
        app.logger.warning('====================')

        # コンフィグ値取得
        history_url = __get_catalog_tool_config('history_url')

        # 横断検索用CKANチェック
        if not flask_login.current_user.release_ckan_apikey or not flask_login.current_user.release_ckan_url:
            raise CatalogToolException(
                'edit_release_catalog_userinfo_NoReleaseCKANInfo', 500)

        # 横断検索カタログデータチェック
        if 'release' not in data or not data['release']:
            raise CatalogToolException(
                'edit_release_catalog_NoReleaseCatalogData', 400)

        # リフレッシュトークン更新
        token_response = cadde_auth.post_token_refresh(auth_code)
        access_token = token_response['access_token']

        # 横断検索カタログのみ編集
        ret_edit_release = edit_release(app,
                                        SAVE_DIR_PATH,
                                        data['release'],
                                        history_url,
                                        access_token,
                                        flask_login.current_user.release_ckan_apikey,
                                        flask_login.current_user.release_ckan_url)

        ret['message'] = ret_edit_release['message']
        ret['release']['ckan_url'] = ret_edit_release['ckan_url']
        ret['release']['pkg'] = ret_edit_release['pkg']

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '横断検索カタログ編集時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'edit_release_catalog_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/datacatalog/detail/edit', methods=['PUT'])
def edit_detail_catalog():
    """ 詳細検索カタログ編集

    詳細検索カタログを編集する

    Args:
      dict
        - detail: 詳細検索カタログ用データセット

    Returns:
      dict
        - message: 詳細検索カタログ編集結果メッセージ
        - detail: 詳細検索カタログ編集結果
            - ckan_url: 編集した詳細検索カタログのURL
            - pkg: 編集した詳細検索カタログ情報
    """
    app.logger.warning('詳細検索カタログ編集')

    ret = {
        'message': 'error',
        'detail': {'ckan_url': '', 'pkg': None}
    }

    try:
        data = request.data.decode('utf-8')
        data = json.loads(data)
        auth_code = request.cookies.get('session_id')
        app.logger.warning(json.dumps(data, indent=2, ensure_ascii=False))
        app.logger.warning('====================')

        # コンフィグ値取得
        ckans = __get_catalog_tool_config('ckan_info')
        history_url = __get_catalog_tool_config('history_url')

        # 詳細CKANチェック
        if not ckans['detail']['ckan_url'] or not ckans['detail']['sysadmin_key']:
            raise CatalogToolException(
                'edit_detail_catalog_userinfo_NoDetailCKANInfo', 500)

        # カタログデータチェック
        if 'detail' not in data or not data['detail']:
            raise CatalogToolException(
                'edit_detail_catalog_NoDetailCatalogData', 400)

        # リフレッシュトークン更新
        token_response = cadde_auth.post_token_refresh(auth_code)
        access_token = token_response['access_token']

        # 詳細検索カタログのみ編集
        ret_edit_detail = edit_detail(app,
                                      SAVE_DIR_PATH,
                                      data['detail'],
                                      history_url,
                                      access_token,
                                      flask_login.current_user.detail_ckan_apikey,
                                      flask_login.current_user.detail_ckan_url)

        ret['message'] = ret_edit_detail['message']
        ret['detail']['ckan_url'] = ret_edit_detail['ckan_url']
        ret['detail']['pkg'] = ret_edit_detail['pkg']

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '詳細検索カタログ編集時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'edit_detail_catalog_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/datacatalog/edit', methods=['PUT'])
def edit_both_catalog():
    """ 横断検索カタログ・詳細検索カタログ編集

    横断検索カタログ・詳細検索カタログを編集する

    Args:
      dict
        - release: 横断検索カタログ用データセット
        - detail: 詳細検索カタログ用データセット

    Returns:
      dict
        - message: 横断検索カタログ編集結果メッセージ
        - release: 横断検索カタログ編集結果
            - ckan_url: 編集した横断検索カタログのURL
            - pkg: 編集した横断検索カタログ情報
        - detail: 詳細検索カタログ編集結果
            - ckan_url: 編集した詳細検索カタログのURL
            - pkg: 編集した詳細検索カタログ情報
    """
    app.logger.warning('横断検索カタログ・詳細検索カタログ編集')

    ret = {
        'message': 'error',
        'release': {'ckan_url': '', 'pkg': None},
        'detail': {'ckan_url': '', 'pkg': None}
    }

    try:
        data = request.data.decode('utf-8')
        data = json.loads(data)
        auth_code = request.cookies.get('session_id')
        app.logger.warning(json.dumps(data, indent=2, ensure_ascii=False))
        app.logger.warning('====================')

        # コンフィグ値取得
        history_url = __get_catalog_tool_config('history_url')

        # 横断検索用CKANチェック
        if not flask_login.current_user.release_ckan_apikey or not flask_login.current_user.release_ckan_url:
            raise CatalogToolException(
                'edit_both_catalog_userinfo_NoReleaseCKANInfo', 500)

        # 横断検索カタログデータチェック
        if 'release' not in data or not data['release']:
            raise CatalogToolException(
                'edit_both_catalog_NoReleaseCatalogData', 400)

        # 詳細検索用CKANチェック
        if not flask_login.current_user.detail_ckan_apikey or not flask_login.current_user.detail_ckan_url:
            raise CatalogToolException(
                'edit_both_catalog_userinfo_NoDetailCKANInfo', 500)

        # 詳細検索カタログデータチェック
        if 'detail' not in data or not data['detail']:
            raise CatalogToolException(
                'edit_both_catalog_NoDetailCatalogData', 400)

        # リフレッシュトークン更新
        token_response = cadde_auth.post_token_refresh(auth_code)
        access_token = token_response['access_token']

        # 横断検索カタログ・詳細検索カタログを編集
        ret = edit_both(app,
                        SAVE_DIR_PATH,
                        data['release'],
                        data['detail'],
                        history_url,
                        access_token,
                        flask_login.current_user.release_ckan_apikey,
                        flask_login.current_user.release_ckan_url,
                        flask_login.current_user.detail_ckan_apikey,
                        flask_login.current_user.detail_ckan_url)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '横断検索カタログ・詳細検索カタログ編集時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'edit_both_catalog_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/datacatalog/release/search', methods=['POST'])
def search_release_catalog():
    """ 横断検索カタログ検索

    横断検索カタログからカタログを検索して取得する
    また、横断検索カタログに紐づいている詳細検索カタログも詳細検索用データセットIDから検索し、取得する

    Args:
      dict
        - keyword: 検索キーワード
        - url: CKANデータセット名

    Returns:
      dict
        - message: カタログ検索結果メッセージ
        - release: 横断検索カタログ検索結果
        - detail: 詳細検索カタログ検索結果
    """
    app.logger.warning('横断検索カタログ検索')

    ret = {
        'message': 'error',
        'release': 'none'
    }

    try:
        # パラメータ取得
        data = request.data.decode('utf-8')
        data = json.loads(data)
        app.logger.warning(json.dumps(data, indent=2, ensure_ascii=False))
        app.logger.warning('=======================')

        start = 0
        rows = 100
        if 'start' in data:
            start = data['start']
        if 'rows' in data:
            rows = data['rows']
        if 'keyword' in data:
            keyword = str(data['keyword'])
        if 'url' in data:
            url = str(data['url'])
        if not keyword and not url:
            raise CatalogToolException(
                'search_release_catalog_NoUrlOrKeyword', 400)

        # 組織情報設定
        if flask_login.current_user.sysadmin:
            # ローカルCKAN運用管理者ユーザ
            organization = None
        if flask_login.current_user.ckan == 'external':
            # 外部CKAN
            external_organization = get_ckan_user_org(app,
                                                      flask_login.current_user.release_ckan_username,
                                                      flask_login.current_user.release_ckan_apikey,
                                                      flask_login.current_user.release_ckan_url,
                                                      flask_login.current_user.detail_ckan_username,
                                                      flask_login.current_user.detail_ckan_apikey,
                                                      flask_login.current_user.detail_ckan_url)
            organization = [dic['org_label'] for dic in external_organization]
        else:
            # ローカルCKAN提供者ユーザ
            organization = flask_login.current_user.organization

        ret = search_release(app,
                             keyword,
                             url,
                             organization,
                             flask_login.current_user.release_ckan_apikey,
                             flask_login.current_user.release_ckan_url,
                             flask_login.current_user.detail_ckan_apikey,
                             flask_login.current_user.detail_ckan_url,
                             start,
                             rows)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '横断検索カタログ検索時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'search_release_catalog_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/datacatalog/detail/search', methods=['POST'])
def search_detail_catalog():
    """ 詳細検索カタログ検索

    詳細検索カタログからカタログを検索して取得する
    また、詳細検索カタログに紐づいている横断検索カタログも詳細検索用データセットIDから検索し、取得する

    Args:
      dict
        - keyword: 検索キーワード
        - url: CKANデータセット名

    Returns:
      dict
        - message: カタログ検索結果メッセージ
        - datasets: dict
            - release: 横断検索カタログ検索結果
            - detail: 詳細検索カタログ検索結果
    """
    app.logger.warning('詳細検索カタログ検索')

    ret = {
        'message': 'error',
        'release': 'none'
    }

    try:
        # パラメータ取得
        data = request.data.decode('utf-8')
        data = json.loads(data)
        app.logger.warning(json.dumps(data, indent=2, ensure_ascii=False))
        app.logger.warning('=======================')

        start = 0
        rows = 100
        if 'start' in data:
            start = data['start']
        if 'rows' in data:
            rows = data['rows']
        if 'keyword' in data:
            keyword = str(data['keyword'])
        if 'url' in data:
            url = str(data['url'])
        if not keyword and not url:
            raise CatalogToolException(
                'search_detail_catalog_NoUrlOrKeyword', 400)

        # 組織情報設定
        if flask_login.current_user.sysadmin:
            # ローカルCKAN運用管理者ユーザ
            organization = None
        if flask_login.current_user.ckan == 'external':
            # 外部CKAN
            external_organization = get_ckan_user_org(app,
                                                      flask_login.current_user.release_ckan_username,
                                                      flask_login.current_user.release_ckan_apikey,
                                                      flask_login.current_user.release_ckan_url,
                                                      flask_login.current_user.detail_ckan_username,
                                                      flask_login.current_user.detail_ckan_apikey,
                                                      flask_login.current_user.detail_ckan_url)
            organization = [dic['org_label'] for dic in external_organization]
        else:
            # ローカルCKAN提供者ユーザ
            organization = flask_login.current_user.organization

        ret = search_detail(app,
                            keyword,
                            url,
                            organization,
                            flask_login.current_user.release_ckan_apikey,
                            flask_login.current_user.release_ckan_url,
                            flask_login.current_user.detail_ckan_apikey,
                            flask_login.current_user.detail_ckan_url,
                            start,
                            rows)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '詳細検索カタログ検索時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'search_detail_catalog_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/datacatalog/search', methods=['POST'])
def search_catalog():
    """ 横断検索カタログ・詳細検索カタログ検索

    横断検索カタログ、詳細検索カタログをそれぞれ検索して取得する
    横断検索カタログと詳細検索カタログの詳細検索カタログも詳細検索用データセットIDが同一である場合、紐づける

    Args:
      dict
        - keyword: 検索キーワード
        - url: CKANデータセット名

    Returns:
      dict
        - message: カタログ検索結果メッセージ
        - release: 横断検索カタログ検索結果
        - detail: 詳細検索カタログ検索結果
    """
    app.logger.warning('横断検索カタログ・詳細検索カタログ検索')

    ret = {
        'message': 'error',
        'release': 'none'
    }

    try:
        # パラメータ取得
        data = request.data.decode('utf-8')
        data = json.loads(data)
        app.logger.warning(json.dumps(data, indent=2, ensure_ascii=False))
        app.logger.warning('=======================')

        start = 0
        rows = 100
        if 'start' in data:
            start = data['start']
        if 'rows' in data:
            rows = data['rows']
        if 'keyword' in data:
            keyword = str(data['keyword'])
        if 'url' in data:
            url = str(data['url'])
        if not keyword and not url:
            raise CatalogToolException('search_catalog_NoUrlOrKeyword', 400)

        # 組織情報設定
        if flask_login.current_user.sysadmin:
            # ローカルCKAN運用管理者ユーザ
            organization = None
        if flask_login.current_user.ckan == 'external':
            # 外部CKAN
            external_organization = get_ckan_user_org(app,
                                                      flask_login.current_user.release_ckan_username,
                                                      flask_login.current_user.release_ckan_apikey,
                                                      flask_login.current_user.release_ckan_url,
                                                      flask_login.current_user.detail_ckan_username,
                                                      flask_login.current_user.detail_ckan_apikey,
                                                      flask_login.current_user.detail_ckan_url)
            organization = [dic['org_label'] for dic in external_organization]
        else:
            # ローカルCKAN提供者ユーザ
            organization = flask_login.current_user.organization

        ret = search_both(app,
                          keyword,
                          url,
                          organization,
                          flask_login.current_user.release_ckan_apikey,
                          flask_login.current_user.release_ckan_url,
                          flask_login.current_user.detail_ckan_apikey,
                          flask_login.current_user.detail_ckan_url,
                          start,
                          rows)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '横断検索カタログ・詳細検索カタログ検索時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'search_catalog_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/datacatalog', methods=['DELETE'])
def delete_catalog():
    """ カタログ削除

    横断検索カタログ・詳細検索カタログを削除する

    Args:
      dict
        - release: 削除する横断検索カタログのCKANデータセット名のリスト
        - detail: 削除する詳細検索カタログのCKANデータセット名のリスト

    Returns:
      string: カタログ削除結果メッセージ
    """
    app.logger.warning('カタログ削除')

    ret = {
        'message': 'suceess',
        'release': [],
        'detail': []
    }

    try:
        data = request.data.decode('utf-8')
        data = json.loads(data)
        app.logger.warning(json.dumps(data, indent=2, ensure_ascii=False))
        app.logger.warning('=======================')
        if 'release' not in data:
            raise CatalogToolException('delete_catalog_NoRelease', 400)
        if 'detail' not in data:
            raise CatalogToolException('delete_catalog_NoDetail', 400)

        # 組織情報設定
        if flask_login.current_user.sysadmin:
            # ローカルCKAN運用管理者ユーザ
            organization = None
        if flask_login.current_user.ckan == 'external':
            # 外部CKAN
            external_organization = get_ckan_user_org(app,
                                                      flask_login.current_user.release_ckan_username,
                                                      flask_login.current_user.release_ckan_apikey,
                                                      flask_login.current_user.release_ckan_url,
                                                      flask_login.current_user.detail_ckan_username,
                                                      flask_login.current_user.detail_ckan_apikey,
                                                      flask_login.current_user.detail_ckan_url)
            organization = [dic['org_label'] for dic in external_organization]
        else:
            # ローカルCKAN提供者ユーザ
            organization = flask_login.current_user.organization

        ret = delete_catalogs(app,
                              organization,
                              data['release'],
                              data['detail'],
                              flask_login.current_user.release_ckan_apikey,
                              flask_login.current_user.release_ckan_url,
                              flask_login.current_user.detail_ckan_apikey,
                              flask_login.current_user.detail_ckan_url)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'カタログ削除時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'delete_catalog_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/import/release', methods=['POST'])
def import_release():
    """ 横断検索カタログインポート

    横断検索用CKANにカタログをインポートする

    Args:
      dict
        - delete_ckan: 横断検索用CKANのカタログ削除フラグ
        - file: インポートファイル

    Returns:
      dict
        - status: インポート結果
        - message: メッセージ
    """

    app.logger.warning('横断検索カタログインポート')
    app.logger.warning(flask_login.current_user.username)

    ret = {
        'status': 'faild',
        'message': ''
    }

    try:

        # 横断CKANチェック
        if not flask_login.current_user.release_ckan_url or not flask_login.current_user.release_ckan_apikey:
            raise CatalogToolException('import_release_ckan_NotFound', 500)

        # データカタログの削除(True or False)
        data = json.loads(request.form['data'])
        if 'delete_ckan' not in data:
            raise CatalogToolException('import_release_NoDeleteFlug', 400)

        delete_catalog = True if data['delete_ckan'] == 'true' else False

        # ファイルの有無チェック
        if 'file' not in request.files:
            app.logger.warning('ファイルパートなし')
            raise CatalogToolException('import_release_NoFile', 400)

        # ファイル取得
        file = request.files['file']
        app.logger.warning(type(file))
        app.logger.warning(file)
        if file.filename == '':
            app.logger.warning('ファイル選択なし')
            raise CatalogToolException('import_release_NoFilename', 400)

        # 組織情報設定
        if flask_login.current_user.ckan == 'external':
            # 外部CKAN
            external_organization = get_ckan_user_org(app,
                                                      flask_login.current_user.release_ckan_username,
                                                      flask_login.current_user.release_ckan_apikey,
                                                      flask_login.current_user.release_ckan_url,
                                                      flask_login.current_user.detail_ckan_username,
                                                      flask_login.current_user.detail_ckan_apikey,
                                                      flask_login.current_user.detail_ckan_url)
            organization = [dic['org_label'] for dic in external_organization]
        else:
            # ローカルCKAN提供者ユーザ
            organization = flask_login.current_user.organization

        # インポート処理
        catalog_type = 'release'
        ret = ckan_dataset.import_dataset(flask_login.current_user.username,
                                          file,
                                          flask_login.current_user.release_ckan_url,
                                          flask_login.current_user.release_ckan_apikey,
                                          organization,
                                          catalog_type,
                                          delete_catalog)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '横断検索カタログインポート時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'import_release_Exception'}), 500

    app.logger.warning(ret)
    return jsonify(ret), 200


@app.route(prefix_uri + '/import/detail', methods=['POST'])
def import_detail():
    """ 詳細検索カタログインポート

    詳細検索用CKANにカタログをインポートする

    Args:
      dict
        - delete_ckan: 横断検索用CKANのカタログ削除フラグ
        - file: インポートファイル

    Returns:
      dict
        - status: インポート結果
        - message: メッセージ
    """

    app.logger.warning('詳細検索カタログインポート')
    app.logger.warning(flask_login.current_user.username)

    ret = {
        'status': 'faild',
        'message': ''
    }

    try:
        # 詳細CKANチェック
        if not flask_login.current_user.detail_ckan_url or not flask_login.current_user.detail_ckan_apikey:
            raise CatalogToolException('import_detail_ckan_NotFound', 500)

        # データカタログの削除(True or False)
        data = json.loads(request.form['data'])
        if 'delete_ckan' not in data:
            raise CatalogToolException('import_detail_NoDeleteFlug', 400)

        delete_catalog = True if data['delete_ckan'] == 'true' else False

        # ファイルの有無チェック
        if 'file' not in request.files:
            app.logger.warning('ファイルパートなし')
            raise CatalogToolException('import_detail_NoFile', 400)

        # ファイル取得
        file = request.files['file']
        app.logger.warning(type(file))
        app.logger.warning(file)
        if file.filename == '':
            app.logger.warning('ファイル選択なし')
            raise CatalogToolException('import_detail_NoFilename', 400)

        # 組織情報設定
        if flask_login.current_user.ckan == 'external':
            # 外部CKAN
            external_organization = get_ckan_user_org(app,
                                                      flask_login.current_user.release_ckan_username,
                                                      flask_login.current_user.release_ckan_apikey,
                                                      flask_login.current_user.release_ckan_url,
                                                      flask_login.current_user.detail_ckan_username,
                                                      flask_login.current_user.detail_ckan_apikey,
                                                      flask_login.current_user.detail_ckan_url)
            organization = [dic['org_label'] for dic in external_organization]
        else:
            # ローカルCKAN提供者ユーザ
            organization = flask_login.current_user.organization

        # インポート処理
        catalog_type = 'detail'
        ret = ckan_dataset.import_dataset(flask_login.current_user.username,
                                          file,
                                          flask_login.current_user.detail_ckan_url,
                                          flask_login.current_user.detail_ckan_apikey,
                                          organization,
                                          catalog_type,
                                          delete_catalog)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '詳細検索カタログインポート時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'import_detail_Exception'}), 500

    app.logger.warning(ret)
    return jsonify(ret), 200


@app.route(prefix_uri + '/export/release', methods=['POST'])
def export_release():
    """ 横断検索カタログエクスポート

    横断検索用CKANからにカタログをエクスポートする

    Returns:
      dict
        - status: エクスポート結果
        - message: メッセージ
        - filename: エクスポートファイル名
    """

    app.logger.warning('横断検索カタログエクスポート')
    app.logger.warning(flask_login.current_user.username)

    ret = {
        'status': 'faild',
        'message': '',
        'filename': ''
    }

    try:
        # 横断CKANチェック
        if not flask_login.current_user.release_ckan_url or not flask_login.current_user.release_ckan_apikey:
            raise CatalogToolException('export_release_ckan_NotFound', 500)

        # 組織情報設定
        if flask_login.current_user.ckan == 'external':
            # 外部CKAN
            external_organization = get_ckan_user_org(app,
                                                      flask_login.current_user.release_ckan_username,
                                                      flask_login.current_user.release_ckan_apikey,
                                                      flask_login.current_user.release_ckan_url,
                                                      flask_login.current_user.detail_ckan_username,
                                                      flask_login.current_user.detail_ckan_apikey,
                                                      flask_login.current_user.detail_ckan_url)
            organization = [dic['org_label'] for dic in external_organization]
        else:
            # ローカルCKAN提供者ユーザ
            organization = flask_login.current_user.organization
        
        # エクスポート処理
        ret = ckan_dataset.export_dataset(flask_login.current_user.username,
                                          organization,
                                          flask_login.current_user.release_ckan_url,
                                          flask_login.current_user.release_ckan_apikey,
                                          'release')

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '横断検索カタログエクスポート時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'export_release_Exception'}), 500

    app.logger.warning(ret)
    return jsonify(ret), 200


@app.route(prefix_uri + '/export/detail', methods=['POST'])
def export_detail():
    """ 詳細検索カタログエクスポート

    詳細検索用CKANにカタログをエクスポートする

    Returns:
      dict
        - status: エクスポート結果
        - message: メッセージ
        - filename: エクスポートファイル名
    """

    app.logger.warning('詳細検索カタログエクスポート')
    app.logger.warning(flask_login.current_user.username)

    ret = {
        'status': 'faild',
        'message': '',
        'filename': ''
    }

    try:
        # 詳細CKANチェック
        if not flask_login.current_user.detail_ckan_url or not flask_login.current_user.detail_ckan_apikey:
            raise CatalogToolException('export_detail_ckan_NotFound', 500)

        # 組織情報設定
        if flask_login.current_user.ckan == 'external':
            # 外部CKAN
            external_organization = get_ckan_user_org(app,
                                                      flask_login.current_user.release_ckan_username,
                                                      flask_login.current_user.release_ckan_apikey,
                                                      flask_login.current_user.release_ckan_url,
                                                      flask_login.current_user.detail_ckan_username,
                                                      flask_login.current_user.detail_ckan_apikey,
                                                      flask_login.current_user.detail_ckan_url)
            organization = [dic['org_label'] for dic in external_organization]
        else:
            # ローカルCKAN提供者ユーザ
            organization = flask_login.current_user.organization

        # エクスポート処理
        ret = ckan_dataset.export_dataset(flask_login.current_user.username,
                                          organization,
                                          flask_login.current_user.detail_ckan_url,
                                          flask_login.current_user.detail_ckan_apikey,
                                          'detail')

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '詳細検索カタログエクスポート時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'export_detail_Exception'}), 500

    app.logger.warning(ret)
    return jsonify(ret), 200


@app.route(prefix_uri + '/export/status', methods=['POST'])
def export_status():
    """ エクスポート状況取得

    エクスポート状況を取得する

    Returns:
      dict
        - status: エクスポート状況（available | notavailable）
        - message: メッセージ
    """

    app.logger.warning('エクスポート状況取得')
    app.logger.warning(flask_login.current_user.username)
    data = json.loads(request.data.decode('utf-8'))
    ckan_type = data['ckan_type']

    ret = {
        'status': 'notavailable',
        'message': 'エクスポート処理中またはエクスポートファイルがありません。'
    }

    available = ckan_dataset.available_export_file(
        flask_login.current_user.username,
        ckan_type)
    if available:
        ret['status'] = 'available'
        ret['message'] = 'エクスポートファイルが取得可能です。'

    app.logger.warning(ret)
    return jsonify(ret), 200


@app.route(prefix_uri + '/export/file/<ckan_type>', methods=['GET'])
def export_file(ckan_type):
    """ エクスポートファイル取得

    エクスポートファイルを取得する

    Returns:
      file: エクスポートファイル
    """

    app.logger.warning('エクスポートファイル取得')
    app.logger.warning(flask_login.current_user.username)

    export_file_path, export_filename = ckan_dataset.get_file_path(
        flask_login.current_user.username,
        ckan_type)
    
    return send_file(export_file_path,
                     as_attachment=True,
                     download_name=export_filename,
                     mimetype='application/gzip')


def analyseThemeKeywords(stub, title, desc, analyse_type):
    """ テーマとキーワード分析処理

    Args:
      stub: grpcのchannel
      title: データセットのタイトル
      description: データセットの説明
      analyse_type: 分析タイプ(theme or tag)

    Returns:
      best: 最高値
      toplist: 上位リスト
      prob: 上位リストの確率
    """
    mes, best, toplist, prob = [], [], [], []

    # 送信メッセージ作成
    mes.append(ml_analysis_pb2.AnalysisThemeKeyword(title=title,
                                                    description=desc,
                                                    analyse_type=analyse_type))
    # 送信及び受信
    responses = stub.ThemeKeywordAnalyseServer(iter(mes))
    app.logger.warning('analyseThemeKeywords responses')
    app.logger.warning(responses)

    # 受信メッセージの解析
    for res in responses:
        app.logger.warning('responses: ')
        app.logger.warning(res)
        if best == []:
            best = str(res.best_analyse)
            app.logger.warning('best: ')
            app.logger.warning(best)
        elif toplist == []:
            toplist = str(res.top_analyse)
            app.logger.warning('toplist: ')
            app.logger.warning(toplist)
        elif prob == []:
            prob = str(res.probability)
            app.logger.warning('prob: ')
            app.logger.warning(prob)

    return best, toplist, prob


def analyse_run(title, desc, analyse_type):
    """ gRPCサーバの設定

    Args:
      stub: grpcのchannel
      title: データセットのタイトル
      description: データセットの説明
      analyse_type: 分析タイプ(theme or tag)

    Returns:
      best: 最高値
      toplist: 上位リスト
      prob: 上位リストの確率
    """
    best, toplist, prob = [], [], []

    # コンフィグ値取得
    grpc_server = __get_catalog_tool_config('grpc_server')

    # gRPCチャネル設定
    with grpc.insecure_channel(grpc_server) as channel:
        stub = ml_analysis_pb2_grpc.AnalyseServiceStub(channel)

        # 分析処理の呼び出し
        best, toplist, prob = analyseThemeKeywords(
            stub, title, desc, analyse_type)

    return best, toplist, prob


@app.route(prefix_uri + '/config', methods=['GET'])
def get_external_service():
    """ 外部サービスおよび機械学習使用有無確認

    クライアント画面で使用するコンフィグ値、
    外部サービス（Geonames）や機械学習を使用するか否かの値をWebサーバに返還する

    Returns:
      dict
        - geonames
          - use_geonames: geonamesの使用有無
        - machine_learn
          - theme: 主分類の機械学習使用有無
          - keyword: キーワードの機械学習使用有無
          - spatial: 地域分析の機械学習使用有無
          - temporal: 日時分析の機械学習使用有無
    """
    app.logger.warning('外部サービスおよび機械学習使用有無確認')

    try:
        ret = {
            'geonames': {
                'use_geonames': __get_catalog_tool_config('use_geonames')
            },
            'machine_learn': {
                'theme': __get_catalog_tool_config('theme'),
                'keyword': __get_catalog_tool_config('keyword'),
                'spatial': __get_catalog_tool_config('spatial'),
                'temporal': __get_catalog_tool_config('temporal')
            }
        }

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '外部サービスおよび機械学習使用有無確認時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'get_external_service_Exception'}), 500

    return jsonify(ret)

@app.route(prefix_uri + '/config/ckanauth', methods=['GET'])
def get_ckanauth_method():
    """ CKAN認証コンフィグ情報の取得

    クライアント画面(ユーザ作成画面)で表示するCKAN認証方式をコンフィグから取得する

    Returns:
      list: CKAN認証方式のリスト
    """
    app.logger.warning('CKAN認証コンフィグ情報の取得')

    try:
        ckan_authentication =  __get_catalog_tool_config('ckan_auth')
        ckan_authentication_methods = [method for method in ckan_authentication.keys()]

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'CKAN認証コンフィグ情報の取得時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'et_ckanauth_method_Exception'}), 500

    return jsonify(ckan_authentication_methods)

@app.route(prefix_uri + '/geonamesearch', methods=['GET'])
def get_geonames():
    """ 地域検索

    キーワードから地域情報を検索する

    Args:
      dict
        - keyword: 検索キーワード

    Returns:
      list
        - dict
            - geonameId: 地域名ID
            - name: 地域名
            - countryName: 国名
            - adminName1: 県名
            - lat: 緯度
            - lng: 軽度
            - fcl: ファシリティ
    """
    app.logger.warning('地域検索')

    try:
        keyword = request.args.get('keyword', '')
        print('Get geoname keyword: {}'.format(keyword))

        if not keyword:
            raise CatalogToolException('get_geonames_ValueError', 400)

        # コンフィグ値取得
        geonames = __get_catalog_tool_config('geonames')

        # find keyword
        ret = FindByKeyword_name(keyword, geonames['username'])

    except ValueError:
        return jsonify({'message': '検索キーワードが未設定です。', 'message_id': 'get_geonames_ValueError'}), 400

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '地域検索時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'get_geonames_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/geonameIdsearch', methods=['GET'])
def get_fullgeoname():
    """ 地域のフルネーム取得

    地域名IDから地域のフルネームを取得する
    例 日本>千葉県>千葉市>中央区

    Args:
      dict
        - geonameId: 地域名ID

    Returns:
      string: 地域のフルネーム
              例 日本>千葉県>千葉市>中央区
    """
    app.logger.warning('地域のフルネーム取得')

    try:
        geoname_id = request.args.get('geonameId', '')
        print('GET geoname ID: {}'.format(geoname_id))

        if not geoname_id:
            raise CatalogToolException('get_fullgeoname_ValueError', 400)

        # コンフィグ値取得
        geonames = __get_catalog_tool_config('geonames')

        result_geoname = getFullname(geoname_id, geonames['username'])

    except ValueError:
        return jsonify({'message': '地域名IDが未設定です。', 'message_id': 'get_fullgeoname_ValueError'}), 400

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '地域検索時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'get_fullgeoname_Exception'}), 500

    return result_geoname, 200


@app.route(prefix_uri + '/resource/<resource_type>/<path:url>', methods=['GET'])
def get_resource(url, resource_type):
    """ リソース取得

    リソースURL、リソースタイプからリソースファイルを取得する
    取得したリソースファイルを読み込み、リソース情報をレスポンスとして返却する

    Returns:
      Dict
        - error_label: エラーメッセージ
        - data_list: 読み込んだファイル内データ
        - mime_type: メディアタイプ
        - file_size: ファイルサイズ
        - dataname: リソースファイル名
        - format: ファイルフォーマット
    """
    app.logger.warning('ローカルファイルアップロードダミー')

    ret = {
        'error_label': '',
        'data_list': [],
        'mime_type': '',
        'file_size': '',
        'dataname': '',
        'format': ''
    }

    try:
        if resource_type == 'http':
            app.logger.warning('--- http get files Start ---')
            http_auth = __get_catalog_tool_config('http_auth')
            ret = http_get(app, SAVE_DIR_PATH, url, http_auth)

        elif resource_type == 'ftp':
            app.logger.warning('--- ftp get files Start ---')
            ftp_auth = __get_catalog_tool_config('ftp_auth')
            ret = ftp_get(app, SAVE_DIR_PATH, url, ftp_auth)

        else:
            app.logger.warning('不正なリソース提供手段の識別子')
            raise CatalogToolException('get_resource_ResourceTypeError', 400)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'リソース取得時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'get_resource_Exception'}), 500

    app.logger.warning(ret)
    return jsonify(ret), 200


@app.route(prefix_uri + '/localuploads', methods=['POST'])
def local_upload():
    """ ローカルファイルアップロードダミーIF

    ローカルファイルアップロード時、自動的に発火する
    アプリケーションサーバへのリクエストに対して応答(200)する
    """
    app.logger.warning('ローカルファイルアップロードダミー')
    return 'Dummy Success', 200

# ローカルファイルアップロード


@app.route(prefix_uri + '/uploads', methods=['POST'])
def file_upload():
    """ ローカルファイルアップロード

    ローカルファイルを保存する
    保存したファイルを読み込み、リソース情報をレスポンスとして返却する

    Args:
      file: ファイル

    Returns:
      Dict
        - data_list: データの変数の名前
        - mimetype: メディアタイプ
        - dataname: リソースファイル名
        - format: ファイルフォーマット
    """
    app.logger.warning('ローカルファイルアップロード')

    try:
        # ファイルの有無チェック
        if 'file' not in request.files:
            app.logger.warning('--> No file parts...')
            raise CatalogToolException('file_upload_NoFile', 400)

        # ファイルの整形
        file = request.files['file']
        app.logger.warning(type(file))
        app.logger.warning(file)
        if file.filename == '':
            app.logger.warning('ファイル選択なし')
            raise CatalogToolException('file_upload_NoFilename', 400)

        ret = url_upload(app, SAVE_DIR_PATH, file)
        app.logger.warning(ret)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'ローカルファイルアップロード時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'get_resource_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/ngsidata', methods=['POST'])
def get_ngsi_data():
    """NGSIデータ取得

    NGSIデータモデルを取得する処理

    Args:
      Dict
        - url: 配信の取得先URL
        - tenant: NGSIテナント
        - service_path: NGSIサービスパス

    Returns:
      Dict
        - status: ステータスコード
        - message: エラーメッセージ
        - data_model: 取得したNGSIデータモデル結果
    """
    app.logger.warning('NGSIデータ取得')

    ret = {
        'status': 'error',
        'message': '',
        'data_list': '',
        'dataname': '',
        'file_size': '',
        'format': '',
        'mime_type': ''
    }

    try:
        data = json.loads(request.data.decode('utf-8'))
        app.logger.warning(data)
        if 'url' not in data or not data['url']:
            raise CatalogToolException('get_ngsi_data_NoURL', 400)
        if 'tenant' not in data:
            raise CatalogToolException('get_ngsi_data_NoTenant', 400)
        if 'service_path' not in data:
            raise CatalogToolException('get_ngsi_data_NoServicePath', 400)

        # コンフィグ値取得
        ngsi_server = __get_catalog_tool_config('ngsi_server')

        ngsi = NgsiData(app, ngsi_server)
        ret = ngsi.get_ngsi_data(data)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'NGSIデータ取得時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'get_ngsi_data_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/ngsidatamodel', methods=['POST'])
def get_ngsi_data_model():
    """NGSIデータモデル取得

    NGSIデータモデルを取得する処理

    Args:
      Dict
        - url: 配信のアクセスURL
        - tenant: NGSIテナント
        - service_path: NGSIサービスパス
        - entity_type: NGSIデータ種別

    Returns:
      Dict
        - status: ステータスコード
        - message: エラーメッセージ
        - data_model: 取得したNGSIデータモデル結果
    """
    app.logger.warning('NGSIデータモデル取得')

    ret = {
        'status': 'failed',
        'message': '',
        'data_model': []
    }

    try:
        data = json.loads(request.data.decode('utf-8'))
        if 'url' not in data or not data['url']:
            raise CatalogToolException('get_ngsi_data_model_NoURL', 400)
        if 'tenant' not in data:
            raise CatalogToolException('get_ngsi_data_model_NoTenant', 400)
        if 'service_path' not in data:
            raise CatalogToolException(
                'get_ngsi_data_model_NoServicePath', 400)
        if 'entity_type' not in data:
            raise CatalogToolException('get_ngsi_data_model_NoEntityType', 400)

        # コンフィグ値取得
        ngsi_server = __get_catalog_tool_config('ngsi_server')

        ngsi = NgsiData(app, ngsi_server)
        ret = ngsi.get_ngsi_data_model(data)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'NGSIデータモデル取得時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'get_ngsi_data_model_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/previouseventid', methods=['POST'])
def search_previouseventid():
    """前段イベント識別子検索

    前段イベント識別子を検索する処理

    Args:
      Dict
        - data
          - filename: ファイル名
          - cadde_user_id: CADDEユーザID

    Returns:
      Dict
        - status: 検索状況
        - message: 検索結果有無
        - result: 検索結果
    """
    app.logger.warning('前段イベント識別子検索')

    try:
        data = request.data.decode('utf-8')
        data = json.loads(data)
        app.logger.warning(data)
        auth_code = request.cookies.get('session_id')
        if 'provider_id' not in data or not data['provider_id']:
            raise CatalogToolException('search_history_NoCaddeProviderId', 400)
        if not auth_code:
            raise CatalogToolException('search_history_NoAuthCodoe', 400)

        # コンフィグ値取得
        history_url = __get_catalog_tool_config('history_url')

        # リフレッシュトークン更新
        token_response = cadde_auth.post_token_refresh(auth_code)
        access_token = token_response['access_token']

        ret = search_history(app, data, history_url, access_token)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '前段イベント識別子検索時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'search_previouseventid_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/extracttemporal', methods=['POST'])
def temporalAnalyzer():
    """ 日時分析

    日時を分析する処理

    Args:
      Dict
        - text: 分析対象のテキスト
        - filepath: 分析対象のCSVファイルパス
        - column_name: 分析対象のファイルパスのカラム名
        - input_datetime_format: 分析対象のフォーマット

    Returns:
      Dict
        - start_datetime: 開始日時
        - end_datetime: 終了日時
    """
    app.logger.warning('日時分析')

    try:
        get_message = json.loads(request.data.decode('utf-8'))
        if 'text' not in get_message:
            raise CatalogToolException('temporalAnalyzer_NoText', 400)
        if 'filepath' not in get_message or not get_message['filepath']:
            raise CatalogToolException('temporalAnalyzer_NoFilepath', 400)
        if 'column_name' not in get_message:
            raise CatalogToolException('temporalAnalyzer_NoColumnName', 400)
        if 'input_datetime_format' not in get_message:
            raise CatalogToolException(
                'temporalAnalyzer_NoInputDatetimeFormat', 400)

        text = str(get_message['text'])
        filepath = SAVE_DIR_PATH + str(get_message['filepath'])
        column_name = str(get_message['column_name'])
        input_datetime_format = str(get_message['input_datetime_format'])

        app.logger.warning('temporalAnalyzer')
        app.logger.warning(get_message)
        app.logger.warning('temporalAnalyzer text')
        app.logger.warning(text)
        app.logger.warning('temporalAnalyzer filepath')
        app.logger.warning(filepath)
        app.logger.warning('temporalAnalyzer column_name')
        app.logger.warning(column_name)
        app.logger.warning('temporalAnalyzer input_datetime_format')
        app.logger.warning(input_datetime_format)

        try:
            # csvファイル以外の場合はnone
            extension = filepath.rsplit('.', 1)[1]
            if extension == 'csv':
                # ファイルの読み込み
                csv_to_list = []
                with open(filepath) as f:
                    reader = csv.reader(f)
                    csv_to_list = [row for row in reader]

                csv_str = ''
                for _csv in csv_to_list:
                    csv_str = csv_str + ','.join(_csv) + '\n'
            else:
                csv_str = 'none'
        except OSError:
            csv_str = 'none'

        app.logger.warning('temporalAnalyzer 分析実行前')
        app.logger.warning(csv_str)
        app.logger.warning(column_name)
        # コンフィグ値取得
        grpc_server = __get_catalog_tool_config('grpc_server')

        # 分析実行
        with grpc.insecure_channel(grpc_server) as channel:
            stub = ml_analysis_pb2_grpc.AnalyseServiceStub(channel)

            req_mes = []
            req_mes.append(ml_analysis_pb2.AnalysisTemporal(text=text,
                                                            data=csv_str,
                                                            column_name=column_name,
                                                            input_datetime_format=input_datetime_format))
            res_msg = stub.TemporalAnalyseServer(iter(req_mes))

            result_start_datetime, result_end_datetime = [], []
            for response in res_msg:
                if result_start_datetime == []:
                    app.logger.warning(response.start_datetime)
                    result_start_datetime = response.start_datetime
                elif result_end_datetime == []:
                    app.logger.warning(response.end_datetime)
                    result_end_datetime = response.end_datetime

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '日時分析時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'temporalAnalyzer_Exception'}), 500

    result_json = {
        'start_datetime': result_start_datetime,
        'end_datetime': result_end_datetime
    }

    return jsonify(result_json)


@app.route(prefix_uri + '/extractspatial', methods=['POST'])
def spatialAnalyzer():
    """ 地域分析

    地域を分析する処理

    Args:
      Dict
        - title: 分析対象のタイトル
        - filepath: 分析対象のファイルパス
        - notes: 説明文
        - method: メソッドの選択

    Returns:
      Dict
        spatial_list: 地域の分析結果
    """
    app.logger.warning('地域分析')

    try:
        get_message = json.loads(request.data.decode('utf-8'))
        if 'title' not in get_message:
            raise CatalogToolException('spatialAnalyzer_NoTitle', 400)
        if 'filepath' not in get_message or not get_message['filepath']:
            raise CatalogToolException('spatialAnalyzer_NoFilepath', 400)
        if 'notes' not in get_message:
            raise CatalogToolException('spatialAnalyzer_NoNotes', 400)
        if 'method' not in get_message:
            raise CatalogToolException('spatialAnalyzer_NoMethod', 400)

        title = str(get_message['title'])
        filepath = SAVE_DIR_PATH + str(get_message['filepath'])
        notes = str(get_message['notes'])
        method = str(get_message['method'])

        # コンフィグ値取得
        grpc_server = __get_catalog_tool_config('grpc_server')

        # ファイルの読み込み
        csv_to_list = []
        try:
            with open(filepath) as f:
                reader = csv.reader(f)
                csv_to_list = [row for row in reader]

        except OSError:
            raise CatalogToolException('spatialAnalyzer_FileOpenError', 500)

        csv_str = ''
        for _csv in csv_to_list:
            csv_str = csv_str + ','.join(_csv) + '\n'

        # 分析実行
        with grpc.insecure_channel(grpc_server) as channel:
            stub = ml_analysis_pb2_grpc.AnalyseServiceStub(channel)

            req_mes = []
            req_mes.append(ml_analysis_pb2.AnalysisSpatial(title=title,
                                                           data=csv_str,
                                                           notes=notes,
                                                           method=method))
            res_msg = stub.SpatialAnalyseServer(iter(req_mes))

            app.logger.warning('res_msg:')
            app.logger.warning(res_msg)
            result = []

            for response in res_msg:
                app.logger.warning(response.spatial_list)
                result = response.spatial_list

            result = result.replace("\'", "\"")
            result = json.loads(result)
            json_result = []
            for data in result:
                json_result.append(
                    {
                        'geonameId': data[0],
                        'fcl': data[2],
                        'lat': data[3],
                        'lng': data[4],
                        'adminName1': data[5],
                        'adminName2': data[6],
                        'name': data[6],
                        'score': data[7],
                        'searchMethod': data[8]
                    }
                )
            app.logger.warning('json_result:')
            app.logger.warning(json_result)

        result_json = {
            'spatial_list': json_result
        }

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '地域分析時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'spatialAnalyzer_Exception'}), 500

    return jsonify(result_json)


@app.route(prefix_uri + '/analysis', methods=['POST'])
def themeKeywordAnalyzer():
    """ テーマとキーワードの予測分析

    テーマ、または、キーワードから予測候補を取得する

    Args:
      Dict
        - catarog_title: データセットのタイトル
        - catarog_description: データセットの説明文
        - analyse_type: 分析タイプ(theme | tag)

    Returns:
      Dict
        pred_main: 予測候補のリスト(label:value)
        pred_sub: 予測候補の上位リスト(label:value)
        pred_prob: 予測候補の確率(label:value)
    """
    app.logger.warning('テーマとキーワードの予測分析')

    mes_json = []
    try:
        # フォーマット変換
        get_message = json.loads(request.data.decode('utf-8'))
        if 'catarog_title' not in get_message:
            raise CatalogToolException(
                'themeKeywordAnalyzer_NoCatarogTitle', 400)
        if 'catarog_description' not in get_message:
            raise CatalogToolException(
                'themeKeywordAnalyzer_NoCatarogDescription', 400)
        if 'analyse_type' not in get_message:
            raise CatalogToolException(
                'themeKeywordAnalyzer_NoAnalyseType', 400)

        # 取得した分析対象のデータ(いつか'catalog'に直したい)
        title = str(get_message['catarog_title'])
        description = str(get_message['catarog_description'])
        analyse_type = str(get_message['analyse_type'])

        app.logger.warning('themeKeywordAnalyzer')
        app.logger.warning(get_message)
        app.logger.warning('themeKeywordAnalyzer title')
        app.logger.warning(title)
        app.logger.warning('themeKeywordAnalyzer description')
        app.logger.warning(description)
        app.logger.warning('themeKeywordAnalyzer analyse_type')
        app.logger.warning(analyse_type)

        # 分析(grpc送信)
        best, toplist, prob = analyse_run(title, description, analyse_type)

        res_best, res_toplist, res_prob = [], [], []

        # 分析モードが'Theme'の場合
        if get_message['analyse_type'] == 'theme':

            # Best
            res_best = [{'label': best, 'value': best}]

            # Top List
            toplist = toplist.replace('[', '').replace(']', '')
            toplist = toplist.split(',')

            for _key in toplist:
                res_toplist.append({'label': _key, 'value': _key})

            # Probability
            prob = prob.replace('[', '').replace(']', '').replace('(', '')
            prob = prob.split('), ')
            prob = list(map(lambda x: x.replace(')', ''), prob))

            for _prob in list(prob):
                res_prob.append({'label': _prob, 'value': _prob})

        # 分析モードが'Tag'の場合
        elif get_message['analyse_type'] == 'tag':

            # Best
            best = best.replace('(', '').replace(')', '').replace('\'', '')
            best = best.split(', ')
            best = list(map(lambda tags: tags.replace(',', ''), best))

            for _key in best:
                if _key:
                    res_best.append({'label': _key, 'value': _key})

            # Top List
            toplist = toplist.replace('[', '').replace(']', '')
            toplist = toplist.split(',')

            for _key in toplist:
                res_toplist.append({'label': _key, 'value': _key})

            # Probability
            prob = prob.replace('[', '').replace(']', '').replace('(', '')
            prob = prob.split('), ')
            prob = list(map(lambda x: x.replace(')', ''), prob))

            for _prob in list(prob):
                res_prob.append({'label': _prob, 'value': _prob})

        # 分析モードが'Prefecture'の場合
        elif get_message['analyse_type'] == 'prefecture':

            # Best
            best = best.replace('[', '').replace(']', '').replace(' ', '')
            best = best.split(',')

            for _key in best:
                if _key:
                    res_best.append({'label': _key, 'value': _key})

        # Responseの変形
        mes_json = {
            'pred_main': res_best,
            'pred_sub': res_toplist,
            'pred_prob': res_prob}

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'テーマ・キーワードの予測分析時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'themeKeywordAnalyzer_Exception'}), 500

    return jsonify(mes_json), 200


@app.route(prefix_uri + '/temporal', methods=['PUT'])
def save_temporal():
    """ 入力データ一時保存

    カタログ情報をアプリケーションサーバに保存する

    Args:
      dict:
        - tmpFile: 一時保存データ

    Returns:
      dict: 一時保存結果
        - status: 一時保存状態
        - error: エラーメッセージ
    """
    app.logger.warning('入力データ一時保存')

    try:
        data = request.data.decode('utf-8')
        data = json.loads(data)

        if 'tmpFile' not in data or not data['tmpFile']:
            raise CatalogToolException('save_temporal_NoTmpFile', 400)
        if 'dataForUpdate' not in data or not data['dataForUpdate']:
            raise CatalogToolException('save_temporal_NoDataForUpdate', 400)
        if 'datasetinfo' not in data or not data['datasetinfo']:
            raise CatalogToolException('save_temporal_NoDatasetinfo', 400)
        if 'datajacket' not in data or data['datajacket'] == '':
            raise CatalogToolException('save_temporal_NoDatajacket', 400)
        if 'datasetoptionalinfo' not in data or not data['datasetoptionalinfo']:
            raise CatalogToolException(
                'save_temporal_NoDatasetoptionalinfo', 400)
        if 'userterms' not in data or not data['userterms']:
            raise CatalogToolException('save_temporal_NoUserterms', 400)

        ret = write_tmp_data(app, data, flask_login.current_user.username)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '一時保存時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'save_temporal_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/temporal', methods=['GET'])
def get_temporal():
    """ 一時保存データ取得

    アプリケーションサーバに保存している一時保存データを取得する

    Returns:
      list: 一時保存データ配列
        - dict: 一時保存したカタログ情報
    """
    app.logger.warning('一時保存データ取得')

    try:
        ret = get_tmp_data_files(app, flask_login.current_user.username)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '一時保存データ取得時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'get_temporal_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/temporal', methods=['DELETE'])
def remove_temporal():
    """ 一時保存データ削除

    アプリケーションサーバに保存している一時保存データを削除する

    Args:
      list: 一時保存削除対象配列

    Returns:
      dict: 一時保存削除結果
        - del_data: 削除した一時保存カタログ情報配列
    """
    app.logger.warning('一時保存データ削除')

    try:
        data = request.data.decode('utf-8')
        data = json.loads(data)
        if not data:
            raise CatalogToolException('remove_temporal_NoTemporal', 400)

        ret = delete_tmp_data(app, data, flask_login.current_user.username)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': '一時保存データ削除時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'remove_temporal_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/template', methods=['PUT'])
def save_template():
    """ テンプレート保存

    アプリケーションサーバにテンプレートデータを保存する

    Args:
        Dict: 保存するテンプレート
          - catalog_display: 画面表示制御用設定
          - catalog_value: フィールドデフォルト値

    Returns:
        Dict: テンプレート保存結果
          - status: テンプレート保存結果
          - message: メッセージ

    """

    app.logger.warning('テンプレート保存')
    app.logger.warning(flask_login.current_user.username)

    ret = {
        'status': 'faild',
        'message': ''
    }

    try:
        data = request.data.decode('utf-8')
        data = json.loads(data)

        if not data or 'catalog_display' not in data or 'catalog_value' not in data:
            app.logger.error('フィールドなし')
            raise CatalogToolException('save_template_NoTemplateData', 400)

        template = CatalogTemplate(app, flask_login.current_user.username)
        ret = template.save_template(data)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'テンプレート保存時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'save_template_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/template', methods=['GET'])
def get_template():
    """ テンプレート取得

    アプリケーションサーバに保存しているテンプレートを取得する

    Returns:
        Dict: テンプレート保存結果
          - status: テンプレート保存結果
          - message: メッセージ
          - template: テンプレート
            - catalog_display: 画面表示制御用設定
            - catalog_value: フィールドデフォルト値

    """

    app.logger.warning('テンプレート取得')
    # app.logger.warning(flask_login.current_user.username)

    ret = {
        'status': 'faild',
        'message': ''
    }

    try:
        template = CatalogTemplate(app, flask_login.current_user.username)
        ret = template.get_template()

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'テンプレート取得時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'get_template_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/datacatalog/autocorrect', methods=['POST'])
def search_auto_correct():
    """ カタログ項目オートコンプリート

    指定されたカタログ項目のオートコンプリート候補を検索、取得する

    Args:
        dict:
          - label: カタログ項目
          - value: オートコンプリートキーワード

    Return:
        dict:
          - message: 検索結果状況
          - candidates: オートコンプリート候補
    """
    app.logger.warning('カタログ項目自動補完候補検索')

    ret = []

    try:
        get_material = json.loads(request.data.decode('utf-8'))
        if 'label' not in get_material:
            raise CatalogToolException('search_auto_correct_NoLabel', 400)
        if 'value' not in get_material:
            raise CatalogToolException('search_auto_correct_NoValue', 400)

        data = {'search_key': get_material['label'],
                'search_value': get_material['value']}
        app.logger.warning(data)

        # 組織情報設定
        if flask_login.current_user.sysadmin:
            # ローカルCKAN運用管理者ユーザ
            organization = None
        if flask_login.current_user.ckan == 'external':
            # 外部CKAN
            external_organization = get_ckan_user_org(app,
                                                      flask_login.current_user.release_ckan_username,
                                                      flask_login.current_user.release_ckan_apikey,
                                                      flask_login.current_user.release_ckan_url,
                                                      flask_login.current_user.detail_ckan_username,
                                                      flask_login.current_user.detail_ckan_apikey,
                                                      flask_login.current_user.detail_ckan_url)
            organization = [dic['org_label'] for dic in external_organization]
        else:
            # ローカルCKAN提供者ユーザ
            organization = flask_login.current_user.organization

        ret = search_auto_correct_catalog(app,
                                          data,
                                          organization,
                                          flask_login.current_user.release_ckan_apikey,
                                          flask_login.current_user.release_ckan_url,
                                          flask_login.current_user.detail_ckan_apikey,
                                          flask_login.current_user.detail_ckan_url)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'カタログ項目項目自動補完候補検索時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'search_auto_correct_Exception'}), 500

    return jsonify(ret), 200


@app.route(prefix_uri + '/resource/autocorrect', methods=['POST'])
def search_resource_auto_correct():
    """ リソース項目オートコンプリート

    指定されたリソース項目のオートコンプリート候補を検索、取得する

    Args:
        dict:
          - label: カタログ項目
          - value: オートコンプリートキーワード

    Return:
        dict:
          - message: 検索結果状況
          - candidates: オートコンプリート候補
    """
    app.logger.warning('リソース項目自動補完候補検索')

    ret = []

    try:
        get_material = json.loads(request.data.decode('utf-8'))
        if 'label' not in get_material:
            raise CatalogToolException(
                'search_resource_auto_correct_NoLabel', 400)
        if 'value' not in get_material:
            raise CatalogToolException(
                'search_resource_auto_correct_NoValue', 400)

        data = {'search_key': get_material['label'],
                'search_value': get_material['value']}
        app.logger.warning(data)

        # 組織情報設定
        if flask_login.current_user.sysadmin:
            # ローカルCKAN運用管理者ユーザ
            organization = None
        if flask_login.current_user.ckan == 'external':
            # 外部CKAN
            external_organization = get_ckan_user_org(app,
                                                      flask_login.current_user.release_ckan_username,
                                                      flask_login.current_user.release_ckan_apikey,
                                                      flask_login.current_user.release_ckan_url,
                                                      flask_login.current_user.detail_ckan_username,
                                                      flask_login.current_user.detail_ckan_apikey,
                                                      flask_login.current_user.detail_ckan_url)
            organization = [dic['org_label'] for dic in external_organization]
        else:
            # ローカルCKAN提供者ユーザ
            organization = flask_login.current_user.organization

        ret = search_auto_correct_resource(app,
                                           data,
                                           organization,
                                           flask_login.current_user.release_ckan_apikey,
                                           flask_login.current_user.release_ckan_url,
                                           flask_login.current_user.detail_ckan_apikey,
                                           flask_login.current_user.detail_ckan_url)

    except CatalogToolException as e:
        return jsonify({'message': e.message, 'message_id': e.message_id}), e.http_status_code

    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({'message': 'リソース項目自動補完候補検索時にカタログ作成ツールで例外が発生しました。\n管理者に問い合わせてください。',
                        'message_id': 'search_resource_auto_correct_Exception'}), 500

    return jsonify(ret), 200


def main():
    print(app.url_map)
    app.run(host=host, port=port)


if __name__ == '__main__':
    # 未使用
    main()
