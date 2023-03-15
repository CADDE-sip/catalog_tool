import json
import datetime
import requests
import traceback
from ckanapi import RemoteCKAN, NotAuthorized, NotFound, ValidationError, CKANAPIError, ServerIncompatibleError

from passlib.hash import pbkdf2_sha512

from catalogtool_exception import CatalogToolException

ERROR_REASON = {
    'duplicate_deleted_user': 'That login name is not available.',
    'duplicate_emai_address_forward': 'The email address',
    'duplicate_emai_address_back': 'belongs to a registered user'
}


def connect_ckan(addr, apikey):
    """CKAN接続関数

      Arguments:
        addr: 接続先CKANアドレス
        apikey: 接続先CKANAPIキー

      Returns:
        ckan_api
    """
    session = requests.Session()
    ckan_api = RemoteCKAN(addr, apikey=apikey, session=session)
    return ckan_api


def get_ckan_user_release(app, username, password, release_ckan):
    """横断検索用CKANユーザチェック関数

      Arguments:
        app: flaskのアプリケーションオブジェクト
        username: ユーザ名
        release_ckan: 横断検索用CKAN情報

      Returns:
        user_info(dict): ユーザ情報

    """
    user_info = {
        'status': 'error',
        'message': '',
        'username': None,
        'sysadmin': False,
        'organization': '',
        'ckan': None,
        'about': None
    }

    # 横断CKAN
    try:
        release_ckan_api = connect_ckan(
            release_ckan['ckan_url'], apikey=release_ckan['sysadmin_key'])
        release_user = release_ckan_api.action.user_show(
            id=str(username), include_password_hash=True)
        org_list = release_ckan_api.action.organization_list_for_user(
            id=str(username), permission='create_dataset')
        app.logger.warning('get_ckan_user release_user')
        app.logger.warning(release_user)

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('ユーザ情報取得 横断検索用CKAN 認証エラー')
        raise CatalogToolException('get_ckan_user_release_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('ユーザ情報取得 横断検索用CKAN 検索エラー')
        raise CatalogToolException('get_ckan_user_release_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('ユーザ情報取得 横断検索用CKAN 変数エラー')
        raise CatalogToolException(
            'get_ckan_user_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('ユーザ情報取得 横断検索用CKAN APIエラー')
        raise CatalogToolException('get_ckan_user_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('ユーザ情報取得 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'get_ckan_user_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('ユーザ情報取得 横断検索用CKAN 属性エラー')
        raise CatalogToolException('get_ckan_user_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('ユーザ情報取得 横断検索用CKAN 例外')
        raise CatalogToolException('get_ckan_user_release_Exception', 500)

    # ユーザ有効チェック
    if release_user['state'] != 'active':
        # ユーザ無効
        app.logger.error('ユーザ情報取得 横断検索用CKAN ユーザ非アクティブ')
        raise CatalogToolException('get_ckan_user_release_DisableUser', 500)

    # パスワードチェック
    if not release_ckan['authentication'] and password:
        release_passcheck = pbkdf2_sha512.verify(
            password, release_user['password_hash'])
        if not release_passcheck:
            # パスワード不一致
            app.logger.error('ユーザ情報取得 横断検索用CKAN パスワード不一致')
            raise CatalogToolException(
                'get_ckan_user_release_PasswordNotSame', 500)

    user_info['status'] = 'success'
    user_info['release_user_id'] = release_user['id']
    user_info['detail_user_id'] = ''
    user_info['username'] = str(username)
    user_info['email'] = release_user['email']
    user_info['sysadmin'] = release_user['sysadmin']
    organization = []
    for org in org_list:
        organization.append(org['name'])
    user_info['organization'] = ','.join(organization)

    # 外部CKAN設定取得
    about = {}
    if 'about' in release_user and release_user['about']:
        about = json.loads(release_user['about'])
    if about:
        user_info['ckan'] = 'external'
        user_info['about'] = about
    else:
        user_info['ckan'] = 'internal'
        user_info['about'] = {
            'release_ckan_url': release_ckan['ckan_url'],
            'release_ckan_apikey': release_user['apikey'],
            'release_ckan_username': username,
            'detail_ckan_url': '',
            'detail_ckan_apikey': '',
            'detail_ckan_username': ''
        }

    return user_info


def get_ckan_user_detail(app, username, password, detail_ckan):
    """CKANユーザチェック関数

      Arguments:
        app: flaskのアプリケーションオブジェクト
        username: ユーザ名
        detail_ckan: 詳細検索用CKAN情報

      Returns:
        user_info(dict): ユーザ情報

    """
    user_info = {
        'status': 'error',
        'message': '',
        'username': None,
        'sysadmin': False,
        'organization': '',
        'ckan': None,
        'about': None
    }

    # 詳細CKAN
    try:
        detail_ckan_api = connect_ckan(
            detail_ckan['ckan_url'], apikey=detail_ckan['sysadmin_key'])
        detail_user = detail_ckan_api.action.user_show(
            id=str(username), include_password_hash=True)
        org_list = detail_ckan_api.action.organization_list_for_user(
            id=str(username), permission='create_dataset')
        # app.logger.warning('get_ckan_user detail_user')
        # app.logger.warning(detail_user)

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('ユーザ情報取得 詳細検索用CKAN 認証エラー')
        raise CatalogToolException('get_ckan_user_detail_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('ユーザ情報取得 詳細検索用CKAN 検索エラー')
        raise CatalogToolException('get_ckan_user_detail_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('ユーザ情報取得 詳細検索用CKAN 変数エラー')
        raise CatalogToolException('get_ckan_user_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('ユーザ情報取得 詳細検索用CKAN APIエラー')
        raise CatalogToolException('get_ckan_user_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('ユーザ情報取得 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'get_ckan_user_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('ユーザ情報取得 詳細検索用CKAN 属性エラー')
        raise CatalogToolException('get_ckan_user_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('ユーザ情報取得 詳細検索用CKAN 例外')
        raise CatalogToolException('get_ckan_user_detail_Exception', 500)

    # ユーザ有効チェック
    if detail_user['state'] != 'active' or detail_user['state'] != 'active':
        # ユーザ無効
        app.logger.error('ユーザ情報取得 詳細検索用CKAN ユーザ非アクティブ')
        raise CatalogToolException('get_ckan_user_detail_DisableUser', 500)

    # パスワードチェック
    if not detail_ckan['authentication'] and password:
        detail_passcheck = pbkdf2_sha512.verify(
            password, detail_user['password_hash'])
        if not detail_passcheck:
            # パスワード不一致
            app.logger.error('ユーザ情報取得 詳細検索用CKAN パスワード不一致')
            raise CatalogToolException(
                'get_ckan_user_detail_PasswordNotSame', 500)

    user_info['status'] = 'success'
    user_info['release_user_id'] = ''
    user_info['detail_user_id'] = detail_user['id']
    user_info['username'] = detail_user['name']
    user_info['email'] = detail_user['email']
    user_info['sysadmin'] = detail_user['sysadmin']
    organization = []
    for org in org_list:
        organization.append(org['name'])
    user_info['organization'] = ','.join(organization)

    # 外部CKAN設定取得
    about = {}
    if 'about' in detail_user and detail_user['about']:
        about = json.loads(detail_user['about'])
    if about:
        user_info['ckan'] = 'external'
        user_info['about'] = about
    else:
        user_info['ckan'] = 'internal'
        user_info['about'] = {
            'release_ckan_url': '',
            'release_ckan_apikey': '',
            'release_ckan_username': '',
            'detail_ckan_url': detail_ckan['ckan_url'],
            'detail_ckan_apikey': detail_user['apikey'],
            'detail_ckan_username': username
        }

    return user_info


def get_ckan_user_both(app, username, password, release_ckan, detail_ckan):
    """CKANユーザチェック関数

      Arguments:
        app: flaskのアプリケーションオブジェクト
        username: ユーザ名
        release_ckan: 横断検索用CKAN情報
        detail_ckan: 詳細検索用CKAN情報

      Returns:
        user_info(dict): ユーザ情報

    """
    user_info = {
        'status': 'error',
        'message': '',
        'username': None,
        'sysadmin': False,
        'organization': '',
        'ckan': None,
        'about': None
    }

    # 横断CKAN
    release_user = get_ckan_user_release(app, username, password, release_ckan)

    # 詳細CKAN
    detail_user = get_ckan_user_detail(app, username, password, detail_ckan)

    # ユーザ情報判定
    if release_user['username'] != detail_user['username'] or release_user['sysadmin'] != detail_user['sysadmin']:
        # ユーザ不一致
        app.logger.error('ユーザ情報取得 横断・詳細検索用CKAN ユーザ不一致')
        raise CatalogToolException('get_ckan_user_both_UserNotSame', 500)

    user_info['status'] = 'success'
    user_info['release_user_id'] = release_user['release_user_id']
    user_info['detail_user_id'] = detail_user['detail_user_id']
    user_info['username'] = str(username)
    user_info['email'] = release_user['email']
    user_info['sysadmin'] = release_user['sysadmin']
    set_organization = set(release_user['organization'].split(
        ',')) & set(detail_user['organization'].split(','))
    user_info['organization'] = ','.join(list(set_organization))
    user_info['ckan'] = release_user['ckan']

    app.logger.warning('release_user:%s', release_user)
    app.logger.warning('detail_user:%s', detail_user)
    # 横断検索用CKANと詳細検索用CKANのログイン情報設定
    user_info['about'] = {
        'release_ckan_url': release_user['about']['release_ckan_url'],
        'release_ckan_apikey': release_user['about']['release_ckan_apikey'],
        'release_ckan_username': release_user['about']['release_ckan_username'],
        'release_ckan_auth_method': release_user['about']['release_ckan_auth_method'] if 'release_ckan_auth_method' in release_user['about'] else '',
        'detail_ckan_url': detail_user['about']['detail_ckan_url'],
        'detail_ckan_apikey': detail_user['about']['detail_ckan_apikey'],
        'detail_ckan_username': detail_user['about']['detail_ckan_username'],
        'detail_ckan_auth_method': release_user['about']['detail_ckan_auth_method'] if 'detail_ckan_auth_method' in detail_user['about'] else ''
    }

    return user_info


def get_ckan_user(app, username, password, release_ckan, detail_ckan):
    """CKANユーザチェック関数

      Arguments:
        app: flaskのアプリケーションオブジェクト
        username: ユーザ名
        release_ckan: 横断検索用CKAN情報
        detail_ckan: 詳細検索用CKAN情報

      Returns:
        user: ユーザ情報
        release_user: 横断CKANから取得したユーザ情報
        detail_user: 詳細CKANから取得したユーザ情報

    """
    app.logger.warning('=== ckan_user_manager.py get_ckan_user ===')
    user_info = {
        'status': 'error',
        'message': '',
        'username': None,
        'apikey': None,
        'sysadmin': False,
        'organization': '',
        'ckan': None,
        'about': None
    }

    # トークンが引数に指定されている場合は、apikeyにトークンを指定する
    if release_ckan['ckan_url'] and release_ckan['sysadmin_key'] and detail_ckan['ckan_url'] and detail_ckan['sysadmin_key']:
        # 横断・詳細検索用CKANからユーザ情報を取得
        user_info = get_ckan_user_both(app, username, password, release_ckan, detail_ckan)
    elif release_ckan['ckan_url'] and release_ckan['sysadmin_key']:
        # 横断検索用CKANからユーザ情報を取得
        user_info = get_ckan_user_release(app, username, password, release_ckan)
    elif detail_ckan['ckan_url'] and detail_ckan['sysadmin_key']:
        # 詳細検索用CKANからユーザ情報を取得
        user_info = get_ckan_user_detail(app, username, password, detail_ckan)
    else:
        app.logger.error('ユーザ情報取得 コンフィグCKAN設定なし')
        raise CatalogToolException('get_ckan_user_config_ckan_NotFound', 500)

    user_info['status'] = 'success'
    user_info['message'] = ''
    app.logger.warning('user_info')
    app.logger.warning(user_info)
    return user_info


def get_ckan_user_org(app, release_username, release_apikey, release_addr, detail_username, detail_apikey, detail_addr):
    """ CKANユーザの組織リスト取得関数

      Arguments:
        app: flaskのアプリケーションオブジェクト
        release_username: 横断検索用CKANのユーザ名
        release_apikey: 横断検索用CKANのsysadminのapikey
        release_addr: 横断検索用CKANアドレス
        detail_username: 詳細検索用CKANのユーザ名
        detail_apikey: 詳細検索用CKANのsysadminのapikey
        detail_addr: 詳細検索用CKANアドレス

      Returns:
        organization list
    """

    app.logger.warning('get_ckan_user_org')

    org_list = []
    release_org_list = []
    detail_org_list = []
    try:
        # 横断検索用CKANから組織情報取得
        if release_username and release_apikey and release_addr:
            release_ckan = connect_ckan(
                release_addr, apikey=release_apikey)
            release_org_list = release_ckan.action.organization_list_for_user(
                id=str(release_username), permission='create_dataset')

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('組織リスト取得 横断検索用CKAN 認証エラー')
        raise CatalogToolException(
            'get_ckan_user_org_release_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('組織リスト取得 横断検索用CKAN 検索エラー')
        raise CatalogToolException('get_ckan_user_org_release_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('組織リスト取得 横断検索用CKAN 変数エラー')
        raise CatalogToolException(
            'get_ckan_user_org_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('組織リスト取得 横断検索用CKAN APIエラー')
        raise CatalogToolException(
            'get_ckan_user_org_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('組織リスト取得 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'get_ckan_user_org_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('組織リスト取得 横断検索用CKAN 属性エラー')
        raise CatalogToolException(
            'get_ckan_user_org_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('組織リスト取得 横断検索用CKAN 例外')
        raise CatalogToolException('get_ckan_user_org_release_Exception', 500)

    try:
        # 詳細検索用CKANから組織情報取得
        if detail_username and detail_apikey and detail_addr:
            detail_ckan = connect_ckan(detail_addr, apikey=detail_apikey)
            detail_org_list = detail_ckan.action.organization_list_for_user(
                id=str(detail_username), permission='create_dataset')

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('組織リスト取得 詳細検索用CKAN 認証エラー')
        raise CatalogToolException(
            'get_ckan_user_org_detail_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('組織リスト取得 詳細検索用CKAN 検索エラー')
        raise CatalogToolException('get_ckan_user_org_detail_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('組織リスト取得 詳細検索用CKAN 変数エラー')
        raise CatalogToolException(
            'get_ckan_user_org_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('組織リスト取得 詳細検索用CKAN APIエラー')
        raise CatalogToolException(
            'get_ckan_user_org_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('組織リスト取得 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'get_ckan_user_org_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('組織リスト取得 詳細検索用CKAN 属性エラー')
        raise CatalogToolException(
            'get_ckan_user_org_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('組織リスト取得 詳細検索用CKAN 例外')
        raise CatalogToolException('get_ckan_user_org_detail_Exception', 500)

    # 組織情報整形
    # 横断・詳細検索用CKANから取得
    # 共通値を抽出してリストを作成
    if release_org_list and detail_org_list:
        for release_org in release_org_list:
            for detail_org in detail_org_list:
                if release_org['name'] == detail_org['name']:
                    org_list.append({
                        'org_label': release_org['name'],
                        'org_value': release_org['name']
                    })

    # 横断検索用CKANからのみ取得
    elif release_org_list:
        for _org in release_org_list:
            org_list.append({
                'org_label': _org['name'],
                'org_value': _org['name']
            })

    # 詳細検索用CKANからのみ取得
    elif detail_org_list:
        for _org in detail_org_list:
            org_list.append({
                'org_label': _org['name'],
                'org_value': _org['name']
            })

    app.logger.warning('org_list')
    app.logger.warning(org_list)
    return org_list


def fetch_ckan_userlist(app, release_ckan, detail_ckan):
    """ CKANユーザ一覧取得

    CKANからユーザ一覧を取得する

    Arguments:
        app: Flaskインスタンス
        release_ckan: 横断検索用CKAN情報
        detail_ckan: 詳細検索用CKAN情報

    Returns:
        dict:
            res['status']
            res['message']
            res['userlist']
    """
    app.logger.warning('=== ckan_user_manager.py fetch_ckan_userlist ===')
    res = dict()
    release_user_list = list()
    detail_user_list = list()
    user_list = list()

    try:

        # 横断検索用CKANからユーザリスト取得
        if release_ckan['ckan_url'] and release_ckan['sysadmin_key']:
            ckan_api = connect_ckan(
                release_ckan['ckan_url'], apikey=release_ckan['sysadmin_key'])
            tmp_user_list = []
            tmp_user_list = ckan_api.action.user_list()

            # sysadminユーザはユーザ一覧に含めない
            for user in tmp_user_list:
                if user['sysadmin'] is False:
                    release_user_list.append(user)

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ一覧取得 横断検索用CKAN 認証エラー')
        raise CatalogToolException(
            'fetch_ckan_userlist_release_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ一覧取得 横断検索用CKAN 検索エラー')
        raise CatalogToolException('fetch_ckan_userlist_release_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ一覧取得 横断検索用CKAN 変数エラー')
        raise CatalogToolException(
            'fetch_ckan_userlist_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ一覧取得 横断検索用CKAN APIエラー')
        raise CatalogToolException(
            'fetch_ckan_userlist_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ一覧取得 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'fetch_ckan_userlist_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ一覧取得 横断検索用CKAN 属性エラー')
        raise CatalogToolException(
            'fetch_ckan_userlist_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ一覧取得 横断検索用CKAN 例外')
        raise CatalogToolException(
            'fetch_ckan_userlist_release_Exception', 500)

    try:
        # 詳細検索用CKANからユーザリスト取得
        if detail_ckan['ckan_url'] and detail_ckan['sysadmin_key']:
            ckan_api = connect_ckan(
                detail_ckan['ckan_url'], apikey=detail_ckan['sysadmin_key'])
            tmp_user_list = []
            tmp_user_list = ckan_api.action.user_list()

            # sysadminユーザはユーザ一覧に含めない
            for user in tmp_user_list:
                if user['sysadmin'] is False:
                    detail_user_list.append(user)

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ一覧取得 詳細検索用CKAN 認証エラー')
        raise CatalogToolException(
            'fetch_ckan_userlist_detail_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ一覧取得 詳細検索用CKAN 検索エラー')
        raise CatalogToolException('fetch_ckan_userlist_detail_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ一覧取得 詳細検索用CKAN 変数エラー')
        raise CatalogToolException(
            'fetch_ckan_userlist_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ一覧取得 詳細検索用CKAN APIエラー')
        raise CatalogToolException(
            'fetch_ckan_userlist_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ一覧取得 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'fetch_ckan_userlist_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ一覧取得 詳細検索用CKAN 属性エラー')
        raise CatalogToolException(
            'fetch_ckan_userlist_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ一覧取得 詳細検索用CKAN 例外')
        raise CatalogToolException('fetch_ckan_userlist_detail_Exception', 500)

    # ユーザ一覧整形
    # 横断・詳細検索用CKANから取得
    # 共通値を抽出してリストを作成
    if release_user_list and detail_user_list:
        for release_user in release_user_list:
            for detail_user in detail_user_list:
                if release_user['name'] == detail_user['name']:
                    user_list.append(release_user)

    # 横断検索用CKANからのみ取得
    elif release_user_list:
        for release_user in release_user_list:
            user_list.append(release_user)

    # 詳細検索用CKANからのみ取得
    elif detail_user_list:
        for detail_user in detail_user_list:
            user_list.append(detail_user)

    # CKANから取得したユーザ一覧データ調整
    for user in user_list:
        # タイプスタンプを年月日に変更
        user['created'] = user['created'].split('T')[0]
        # 組織情報を追加
        org_list = ckan_api.action.organization_list_for_user(id=user['name'])
        for org in org_list:
            if 'organization' in user.keys():
                user['organization'] = user['organization'] + ", " + org['name']
            else:
                user['organization'] = org['name']

    res['status'] = 'success'
    res['message'] = ''
    res['userlist'] = user_list
    return res


def create_ckan_user(app, release_ckan, detail_ckan, req):
    """ CKANユーザ作成

    Arguments:
        app: Flaskインスタンス
        release_ckan: 横断検索用CKAN情報
        detail_ckan: 詳細検索用CKAN情報
        req: ユーザ情報

    Returns:
        res['status']: CKAN問い合わせの成否
        res['message']: メッセージ

    Raises:
        ValidationError: CKANの例外
        Exception: 例外
    """

    app.logger.warning('=== create_user ===')
    res = {
        'status': 'error',
        'message': ''
    }

    try:

        # ユーザ作成(横断CKAN)
        if release_ckan['ckan_url'] and release_ckan['sysadmin_key']:
            ckan_api = connect_ckan(
                release_ckan['ckan_url'], apikey=release_ckan['sysadmin_key'])

            ckan_info = dict()
            if req['ckan'] == 'external':
                ckan_info['release_ckan_url'] = req['releaseCkanUrl']
                ckan_info['release_ckan_apikey'] = req['releaseCkanApikey']
                ckan_info['release_ckan_username'] = req['releaseCkanUsername']
                ckan_info['release_ckan_auth_method'] = req['releaseAuthenticationMethod']
                ckan_info['detail_ckan_url'] = req['detailCkanUrl']
                ckan_info['detail_ckan_apikey'] = req['detailCkanApikey']
                ckan_info['detail_ckan_username'] = req['detailCkanUsername']
                ckan_info['detail_ckan_auth_method'] = req['detailAuthenticationMethod']

                ckan_api.action.user_create(
                    name=req['username'], email=req['email'], password=req['password'], about=ckan_info)
            else:
                ckan_api.action.user_create(
                    name=req['username'], email=req['email'], password=req['password'], about=ckan_info)
                ckan_api.action.user_generate_apikey(
                    id=req['username'])

            app.logger.warning('横断検索用CKANにユーザを作成しました。')

            # 組織作成
            if req['organization']:
                organization_list = ckan_api.action.organization_list()
                for org_name in req['organization']:
                    if org_name not in organization_list:
                        ckan_api.action.organization_create(name=org_name)
                        app.logger.warning('横断検索用CKANに組織を作成しました。')

                    ckan_api.action.organization_member_create(
                        id=org_name, username=req['username'], role='editor')
                    app.logger.warning('横断検索用CKANのユーザに組織のロールを付与しました。')

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ作成 横断検索用CKAN 認証エラー')
        raise CatalogToolException(
            'create_ckan_user_release_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ作成 横断検索用CKAN 検索エラー')
        raise CatalogToolException('create_ckan_user_release_NotFound', 500)
    except ValidationError as e:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ作成 横断検索用CKAN 変数エラー')
        if ERROR_REASON['duplicate_deleted_user'] in str(e):
            # 削除済みのユーザ名と重複
            app.logger.error('create_ckan_user duplicate_deleted_user')
            raise CatalogToolException(
                'create_ckan_user_release_DuplicateDeletedUser', 400)
        elif (ERROR_REASON['duplicate_emai_address_forward'] in str(e)
              and ERROR_REASON['duplicate_emai_address_back'] in str(e)):
            # 登録済みのメールアドレスと重複
            app.logger.error('create_ckan_user duplicate_emai_address_forward')
            raise CatalogToolException(
                'create_ckan_user_release_DumlicateEmailAddressForward', 400)

        raise CatalogToolException(
            'create_ckan_user_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ作成 横断検索用CKAN APIエラー')
        raise CatalogToolException(
            'create_ckan_user_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ作成 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'create_ckan_user_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ作成 横断検索用CKAN 属性エラー')
        raise CatalogToolException(
            'create_ckan_user_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ作成 横断検索用CKAN 例外')
        raise CatalogToolException('create_ckan_user_release_Exception', 500)

    try:
        # ユーザ作成(詳細CKAN)
        if detail_ckan['ckan_url'] and detail_ckan['sysadmin_key']:
            ckan_api = connect_ckan(
                detail_ckan['ckan_url'], apikey=detail_ckan['sysadmin_key'])

            ckan_info = dict()
            if req['ckan'] == 'external':
                ckan_info['release_ckan_url'] = req['releaseCkanUrl']
                ckan_info['release_ckan_apikey'] = req['releaseCkanApikey']
                ckan_info['release_ckan_username'] = req['releaseCkanUsername']
                ckan_info['release_ckan_auth_method'] = req['releaseAuthenticationMethod']
                ckan_info['detail_ckan_url'] = req['detailCkanUrl']
                ckan_info['detail_ckan_apikey'] = req['detailCkanApikey']
                ckan_info['detail_ckan_username'] = req['detailCkanUsername']
                ckan_info['detail_ckan_auth_method'] = req['detailAuthenticationMethod']

                ckan_api.action.user_create(
                    name=req['username'], email=req['email'], password=req['password'], about=ckan_info)
            else:
                ckan_api.action.user_create(
                    name=req['username'], email=req['email'], password=req['password'], about=ckan_info)
                ckan_api.action.user_generate_apikey(
                    id=req['username'])

            app.logger.warning('詳細検索用CKANにユーザを作成しました。')

            # 組織作成
            if req['organization']:
                organization_list = ckan_api.action.organization_list()

                for org_name in req['organization']:
                    if org_name not in organization_list:
                        ckan_api.action.organization_create(
                            name=org_name)
                        app.logger.warning('詳細検索用CKANに組織を作成しました。')

                    ckan_api.action.organization_member_create(
                        id=org_name, username=req['username'], role='editor')
                    app.logger.warning('詳細検索用CKANのユーザに組織のロールを付与しました。')

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ作成 詳細検索用CKAN 認証エラー')
        raise CatalogToolException(
            'create_ckan_user_detail_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ作成 詳細検索用CKAN 検索エラー')
        raise CatalogToolException('create_ckan_user_detail_NotFound', 500)
    except ValidationError as e:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ作成 詳細検索用CKAN 変数エラー')
        if ERROR_REASON['duplicate_deleted_user'] in str(e):
            # 削除済みのユーザ名と重複
            app.logger.error('create_ckan_user duplicate_deleted_user')
            raise CatalogToolException(
                'create_ckan_user_detail_DuplicateDeletedUser', 400)
        elif (ERROR_REASON['duplicate_emai_address_forward'] in str(e)
              and ERROR_REASON['duplicate_emai_address_back'] in str(e)):
            # 登録済みのメールアドレスと重複
            app.logger.error('create_ckan_user duplicate_emai_address_forward')
            raise CatalogToolException(
                'create_ckan_user_detail_DumlicateEmailAddressForward', 400)

        raise CatalogToolException(
            'create_ckan_user_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ作成 詳細検索用CKAN APIエラー')
        raise CatalogToolException('create_ckan_user_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ作成 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'create_ckan_user_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ作成 詳細検索用CKAN 属性エラー')
        raise CatalogToolException(
            'create_ckan_user_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ作成 詳細検索用CKAN 例外')
        raise CatalogToolException('create_ckan_user_detail_Exception', 500)

    res['status'] = 'success'
    return res


def update_ckan_user(app, release_ckan, detail_ckan, req):
    """ CKANユーザ更新

    Args:
        app: Flaskインスタンス
        release_ckan: 横断検索用CKAN情報
        detail_ckan: 詳細検索用CKAN情報
        req: ユーザ編集フォーム

    Returns:
        status: CKANユーザ更新の成否
        message: メッセージ
    """
    res = dict()
    message = {'release': '', 'detail': ''}
    now = datetime.datetime.now()
    tmp_mail = 'changeemail_' + now.strftime('%Y%m%d%H%M%S') + '@temporarily'

    try:
        # 横断CKANユーザ更新
        if release_ckan['ckan_url'] and release_ckan['sysadmin_key']:
            ckan_api = connect_ckan(
                release_ckan['ckan_url'], apikey=release_ckan['sysadmin_key'])
            ckan_info = dict()
            if req['ckan'] == 'external':
                ckan_info['release_ckan_url'] = req['releaseCkanUrl']
                ckan_info['release_ckan_apikey'] = req['releaseCkanApikey']
                ckan_info['release_ckan_username'] = req['releaseCkanUsername']
                ckan_info['release_ckan_auth_method'] = req['releaseAuthenticationMethod']
                ckan_info['detail_ckan_url'] = req['detailCkanUrl']
                ckan_info['detail_ckan_apikey'] = req['detailCkanApikey']
                ckan_info['detail_ckan_username'] = req['detailCkanUsername']
                ckan_info['detail_ckan_auth_method'] = req['detailAuthenticationMethod']

            ckan_api.action.user_update(
                id=req['username'], email=tmp_mail)
            ckan_api.action.user_update(
                id=req['username'], password=req['password'], email=req['email'], about=ckan_info)
            message['release'] = 'ユーザ情報を更新しました。'

            # 組織作成
            if req['organization']:
                organization_list = ckan_api.action.organization_list()
                for org_name in req['organization']:
                    if org_name not in organization_list:
                        ckan_api.action.organization_create(
                            name=org_name)
                        message['release'] += '組織を作成しました。'

                    ckan_api.action.organization_member_create(
                        id=org_name, username=req['username'], role='editor')
                    message['release'] += 'ユーザに組織のロールを付与しました。'

            # ユーザの組織情報削除
            org_data = ckan_api.action.organization_list_for_user(
                id=str(req['username']), permission='create_dataset')
            organization_list = [org['name'] for org in org_data]
            for organization in organization_list:
                matchOrg = False
                if organization in req['organization']:
                    matchOrg = True
                if not matchOrg:
                    ckan_api.action.organization_member_delete(
                        id=organization, username=req['username'])

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ更新 横断検索用CKAN 認証エラー')
        raise CatalogToolException(
            'update_ckan_user_release_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ更新 横断検索用CKAN 検索エラー')
        raise CatalogToolException('update_ckan_user_release_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ更新 横断検索用CKAN 変数エラー')
        raise CatalogToolException(
            'update_ckan_user_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ更新 横断検索用CKAN APIエラー')
        raise CatalogToolException(
            'update_ckan_user_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ更新 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'update_ckan_user_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ更新 横断検索用CKAN 属性エラー')
        raise CatalogToolException(
            'update_ckan_user_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ更新 横断検索用CKAN 例外')
        raise CatalogToolException('update_ckan_user_release_Exception', 500)

    try:
        # 詳細CKANユーザ更新
        if detail_ckan['ckan_url'] and detail_ckan['sysadmin_key']:
            ckan_api = connect_ckan(
                detail_ckan['ckan_url'], apikey=detail_ckan['sysadmin_key'])
            ckan_info = dict()
            if req['ckan'] == 'external':
                ckan_info['release_ckan_url'] = req['releaseCkanUrl']
                ckan_info['release_ckan_apikey'] = req['releaseCkanApikey']
                ckan_info['release_ckan_username'] = req['releaseCkanUsername']
                ckan_info['release_ckan_auth_method'] = req['releaseAuthenticationMethod']
                ckan_info['detail_ckan_url'] = req['detailCkanUrl']
                ckan_info['detail_ckan_apikey'] = req['detailCkanApikey']
                ckan_info['detail_ckan_username'] = req['detailCkanUsername']
                ckan_info['detail_ckan_auth_method'] = req['detailAuthenticationMethod']

            ckan_api.action.user_update(
                id=req['username'], email=tmp_mail)
            ckan_api.action.user_update(
                id=req['username'], email=req['email'], password=req['password'], about=ckan_info)
            message['detail'] = 'ユーザ情報を更新しました。'

            # 組織作成
            if req['organization']:
                organization_list = ckan_api.action.organization_list()
                for org_name in req['organization']:
                    if org_name not in organization_list:
                        ckan_api.action.organization_create(
                            name=org_name)
                        message['detail'] += '組織を作成しました。'

                    ckan_api.action.organization_member_create(
                        id=org_name, username=req['username'], role='editor')
                    message['detail'] += 'ユーザに組織のロールを付与しました。'

            # ユーザの組織情報削除
            org_data = ckan_api.action.organization_list_for_user(
                id=str(req['username']), permission='create_dataset')
            organization_list = [org['name'] for org in org_data]
            for organization in organization_list:
                matchOrg = False
                if organization in req['organization']:
                    matchOrg = True
                if not matchOrg:
                    ckan_api.action.organization_member_delete(
                        id=organization, username=req['username'])

    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ更新 詳細検索用CKAN 認証エラー')
        raise CatalogToolException(
            'update_ckan_user_detail_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ更新 詳細検索用CKAN 検索エラー')
        raise CatalogToolException('update_ckan_user_detail_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ更新 詳細検索用CKAN 変数エラー')
        raise CatalogToolException(
            'update_ckan_user_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ更新 詳細検索用CKAN APIエラー')
        raise CatalogToolException('update_ckan_user_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ更新 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'update_ckan_user_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ更新 詳細検索用CKAN 属性エラー')
        raise CatalogToolException(
            'update_ckan_user_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ更新 詳細検索用CKAN 例外')
        raise CatalogToolException('update_ckan_user_detail_Exception', 500)

    res['status'] = 'success'
    res['message'] = ''
    return res


def update_ckan_user_password(app, release_ckan, detail_ckan, req):
    """ CKANユーザパスワード更新

    Args:
        app: Flaskインスタンス
        release_ckan: 横断検索用CKAN情報
        detail_ckan: 詳細検索用CKAN情報
        req: ユーザ編集フォーム

    Returns:
        status: CKANユーザパスワード更新の成否
        message: CKANユーザパスワード更新のエラーメッセージ
    """
    res = dict()

    # 横断CKAN
    if release_ckan['ckan_url'] and release_ckan['sysadmin_key']:
        try:
            ckan_api = connect_ckan(
                release_ckan['ckan_url'], apikey=release_ckan['sysadmin_key'])
            user_info = ckan_api.action.user_show(
                id=str(req['username']), include_password_hash=True)
        except NotAuthorized:
            app.logger.error(traceback.format_exc())
            app.logger.error('CKANユーザパスワード更新(ユーザ情報取得) 横断検索用CKAN 認証エラー')
            raise CatalogToolException(
                'update_ckan_user_password_usershow_release_NotAuthorized', 500)
        except NotFound:
            app.logger.error(traceback.format_exc())
            app.logger.error('CKANユーザパスワード更新(ユーザ情報取得) 横断検索用CKAN 検索エラー')
            raise CatalogToolException(
                'update_ckan_user_password_usershow_release_NotFound', 500)
        except ValidationError:
            app.logger.error(traceback.format_exc())
            app.logger.error('CKANユーザパスワード更新(ユーザ情報取得) 横断検索用CKAN 変数エラー')
            raise CatalogToolException(
                'update_ckan_user_password_usershow_release_ValidationError', 500)
        except CKANAPIError:
            app.logger.error(traceback.format_exc())
            app.logger.error('CKANユーザパスワード更新(ユーザ情報取得) 横断検索用CKAN APIエラー')
            raise CatalogToolException(
                'update_ckan_user_password_usershow_release_CKANAPIError', 500)
        except ServerIncompatibleError:
            app.logger.error(traceback.format_exc())
            app.logger.error('CKANユーザパスワード更新(ユーザ情報取得) 横断検索用CKAN 互換性エラー')
            raise CatalogToolException(
                'update_ckan_user_password_usershow_release_ServerIncompatibleError', 500)
        except AttributeError:
            app.logger.error(traceback.format_exc())
            app.logger.error('CKANユーザパスワード更新(ユーザ情報取得) 横断検索用CKAN 属性エラー')
            raise CatalogToolException(
                'update_ckan_user_password_usershow_release_AttributeError', 500)
        except Exception:
            app.logger.error(traceback.format_exc())
            app.logger.error('CKANユーザパスワード更新(ユーザ情報取得) 横断検索用CKAN 例外')
            raise CatalogToolException(
                'update_ckan_user_password_usershow_release_Exception', 500)

    # 詳細CKAN
    else:
        try:
            ckan_api = connect_ckan(
                detail_ckan['ckan_url'], apikey=detail_ckan['sysadmin_key'])
            user_info = ckan_api.action.user_show(
                id=str(req['username']), include_password_hash=True)
        except NotAuthorized:
            app.logger.error(traceback.format_exc())
            app.logger.error('CKANユーザパスワード更新(ユーザ情報取得) 詳細検索用CKAN 認証エラー')
            raise CatalogToolException(
                'update_ckan_user_password_usershow_detail_NotAuthorized', 500)
        except NotFound:
            app.logger.error(traceback.format_exc())
            app.logger.error('CKANユーザパスワード更新(ユーザ情報取得) 詳細検索用CKAN 検索エラー')
            raise CatalogToolException(
                'update_ckan_user_password_usershow_detail_NotFound', 500)
        except ValidationError:
            app.logger.error(traceback.format_exc())
            app.logger.error('CKANユーザパスワード更新(ユーザ情報取得) 詳細検索用CKAN 変数エラー')
            raise CatalogToolException(
                'update_ckan_user_password_usershow_detail_ValidationError', 500)
        except CKANAPIError:
            app.logger.error(traceback.format_exc())
            app.logger.error('CKANユーザパスワード更新(ユーザ情報取得) 詳細検索用CKAN APIエラー')
            raise CatalogToolException(
                'update_ckan_user_password_usershow_detail_CKANAPIError', 500)
        except ServerIncompatibleError:
            app.logger.error(traceback.format_exc())
            app.logger.error('CKANユーザパスワード更新(ユーザ情報取得) 詳細検索用CKAN 互換性エラー')
            raise CatalogToolException(
                'update_ckan_user_password_usershow_detail_ServerIncompatibleError', 500)
        except AttributeError:
            app.logger.error(traceback.format_exc())
            app.logger.error('CKANユーザパスワード更新(ユーザ情報取得) 詳細検索用CKAN 属性エラー')
            raise CatalogToolException(
                'update_ckan_user_password_usershow_detail_AttributeError', 500)
        except Exception:
            app.logger.error(traceback.format_exc())
            app.logger.error('CKANユーザパスワード更新(ユーザ情報取得) 詳細検索用CKAN 例外')
            raise CatalogToolException(
                'update_ckan_user_password_usershow_detail_Exception', 500)

    # 古いパスワードのチェック
    passcheck = pbkdf2_sha512.verify(
        req['old_password'], user_info['password_hash'])
    if not passcheck:
        # 旧パスワード不正
        app.logger.error('update_ckan_user_password incorrect old password')
        raise CatalogToolException(
            'update_ckan_user_password_MismatchPassword', 400)

    now = datetime.datetime.now()
    tmp_mail = 'changeemail_' + now.strftime('%Y%m%d%H%M%S') + '@temporarily'

    try:
        # 横断CKANユーザパスワード更新
        if release_ckan['ckan_url'] and release_ckan['sysadmin_key']:
            ckan_api = connect_ckan(
                release_ckan['ckan_url'], apikey=release_ckan['sysadmin_key'])
            ckan_api.action.user_update(
                id=str(req['username']), email=tmp_mail)
            ckan_api.action.user_update(
                id=str(req['username']), email=req['email'], password=req['new_password'])
    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザパスワード更新(ユーザ情報更新) 横断検索用CKAN 認証エラー')
        raise CatalogToolException(
            'update_ckan_user_password_userupdate_release_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザパスワード更新(ユーザ情報更新) 横断検索用CKAN 検索エラー')
        raise CatalogToolException(
            'update_ckan_user_password_userupdate_release_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザパスワード更新(ユーザ情報更新) 横断検索用CKAN 変数エラー')
        raise CatalogToolException(
            'update_ckan_user_password_userupdate_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザパスワード更新(ユーザ情報更新) 横断検索用CKAN APIエラー')
        raise CatalogToolException(
            'update_ckan_user_password_userupdate_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザパスワード更新(ユーザ情報更新) 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'update_ckan_user_password_userupdate_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザパスワード更新(ユーザ情報更新) 横断検索用CKAN 属性エラー')
        raise CatalogToolException(
            'update_ckan_user_password_userupdate_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザパスワード更新(ユーザ情報更新) 横断検索用CKAN 例外')
        raise CatalogToolException(
            'update_ckan_user_password_userupdate_release_Exception', 500)

    try:
        # 詳細CKANユーザパスワード更新
        if detail_ckan['ckan_url'] and detail_ckan['sysadmin_key']:
            ckan_api = connect_ckan(
                detail_ckan['ckan_url'], apikey=detail_ckan['sysadmin_key'])
            ckan_api.action.user_update(
                id=str(req['username']), email=tmp_mail)
            ckan_api.action.user_update(
                id=str(req['username']), email=req['email'], password=req['new_password'])
    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザパスワード更新(ユーザ情報更新) 詳細検索用CKAN 認証エラー')
        raise CatalogToolException(
            'update_ckan_user_password_userupdate_detail_NotAuthorized', 500)
    except NotFound:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザパスワード更新(ユーザ情報更新) 詳細検索用CKAN 検索エラー')
        raise CatalogToolException(
            'update_ckan_user_password_userupdate_detail_NotFound', 500)
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザパスワード更新(ユーザ情報更新) 詳細検索用CKAN 変数エラー')
        raise CatalogToolException(
            'update_ckan_user_password_userupdate_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザパスワード更新(ユーザ情報更新) 詳細検索用CKAN APIエラー')
        raise CatalogToolException(
            'update_ckan_user_password_userupdate_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザパスワード更新(ユーザ情報更新) 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'update_ckan_user_password_userupdate_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザパスワード更新(ユーザ情報更新) 詳細検索用CKAN 属性エラー')
        raise CatalogToolException(
            'update_ckan_user_password_userupdate_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザパスワード更新(ユーザ情報更新) 詳細検索用CKAN 例外')
        raise CatalogToolException(
            'update_ckan_user_password_userupdate_detail_Exception', 500)

    res['status'] = 'success'
    return res


def delete_ckan_user(app, release_ckan, detail_ckan, username):
    """ CKANユーザ削除

    Args:
        app: Flaskインスタンス
        release_ckan: 横断検索用CKAN情報
        detail_ckan: 詳細検索用CKAN情報
        username (str): ユーザ名

    Returns:
        dict:
            res['result']: CKANユーザ削除の成否
            res['message']: メッセージ

    Raises:
        Exception: 例外
    """
    app.logger.warning('=== delete_ckan_user ===')
    res = {
        'status': 'error',
        'message': ''
    }

    # 横断カタログCKANからユーザ削除
    try:
        if release_ckan['ckan_url'] and release_ckan['sysadmin_key']:
            ckan_api = connect_ckan(
                release_ckan['ckan_url'], apikey=release_ckan['sysadmin_key'])
            ckan_api.action.user_delete(id=username)
            res['message'] = '横断検索用CKANから該当ユーザを削除しました。'
    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ削除 横断検索用CKAN 認証エラー')
        raise CatalogToolException(
            'delete_ckan_user_release_NotAuthorized', 500)
    except NotFound:
        # 削除対象のユーザが見つからない場合はスルー
        app.logger.warning('CKANユーザ削除 横断検索用CKAN 検索エラー')
        res['message'] = '横断検索用CKANに該当ユーザはありません。'
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ削除 横断検索用CKAN 変数エラー')
        raise CatalogToolException(
            'delete_ckan_user_release_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ削除 横断検索用CKAN APIエラー')
        raise CatalogToolException(
            'delete_ckan_user_release_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ削除 横断検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'delete_ckan_user_release_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ削除 横断検索用CKAN 属性エラー')
        raise CatalogToolException(
            'delete_ckan_user_release_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ削除 横断検索用CKAN 例外')
        raise CatalogToolException('delete_ckan_user_release_Exception', 500)

    # 詳細カタログCKANからユーザ削除
    try:
        if detail_ckan['ckan_url'] and detail_ckan['sysadmin_key']:
            ckan_api = connect_ckan(
                detail_ckan['ckan_url'], apikey=detail_ckan['sysadmin_key'])
            ckan_api.action.user_delete(id=username)
            res['message'] += '詳細検索用CKANから該当ユーザを削除しました。'
    except NotAuthorized:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ削除 詳細検索用CKAN 認証エラー')
        raise CatalogToolException(
            'delete_ckan_user_detail_NotAuthorized', 500)
    except NotFound:
        # 削除対象のユーザが見つからない場合はスルー
        app.logger.warning(traceback.format_exc())
        res['message'] += '詳細検索用CKANに該当ユーザはありません。'
    except ValidationError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ削除 詳細検索用CKAN 変数エラー')
        raise CatalogToolException(
            'delete_ckan_user_detail_ValidationError', 500)
    except CKANAPIError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ削除 詳細検索用CKAN APIエラー')
        raise CatalogToolException('delete_ckan_user_detail_CKANAPIError', 500)
    except ServerIncompatibleError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ削除 詳細検索用CKAN 互換性エラー')
        raise CatalogToolException(
            'delete_ckan_user_detail_ServerIncompatibleError', 500)
    except AttributeError:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ削除 詳細検索用CKAN 属性エラー')
        raise CatalogToolException(
            'delete_ckan_user_detail_AttributeError', 500)
    except Exception:
        app.logger.error(traceback.format_exc())
        app.logger.error('CKANユーザ削除 詳細検索用CKAN 例外')
        raise CatalogToolException('delete_ckan_user_detail_Exception', 500)

    res['status'] = 'success'
    return res
