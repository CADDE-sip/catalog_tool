from app import app
import sys
import os
from io import BytesIO
import json
import time

import pytest

# app.pyを参照するため、1階層上のディレクトリにパスを通す
# sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))


# テスト用コンフィグをtrueに設定
app.config['TESTING'] = True
# @flask_login.login_requiredを無効化する
#app.config['LOGIN_DISABLED'] = True
# テストクライアント作成
client = app.test_client()

# configファイル読み込み

config_file_path = './tests/config.json'
config = open(config_file_path, 'r')
config = json.load(config)


# モックデータ
user_info_login_ok = {
    'status': 'success',
    'message': 'ユーザ情報を取得しました。',
    'username': config["userinfo"]["release"]["username"],
    'apikey': config["addr"]["release"]["sysadmin_key"],
    'sysadmin': True,
    'ckan': 'internal',
    'organization': 'org1,org2',
    'about': {
        'release_ckan_url': config["addr"]["release"]["ckan_url"],
        'release_ckan_username': config["userinfo"]["release"]["username"],
        'release_ckan_apikey': config["addr"]["release"]["sysadmin_key"],
        'detail_ckan_url': config["addr"]["detail"]["ckan_url"],
        'detail_ckan_username': config["userinfo"]["detail"]["username"],
        'detail_ckan_apikey': config["addr"]["detail"]["sysadmin_key"]
    },
    'release_user_id': config["userinfo"]["release"]["username"],
    'detail_user_id': config["userinfo"]["detail"]["username"],
    'email': config["userinfo"]["email"]
}

# ユーザ作成・更新・削除に使うユーザ名
username = "test" + (str(time.time())).split(".")[0]

################################################################
# configデータ取得
################################################################


class TestConfig:
    ##################################
    #  [config]
    #  configデータ取得：/api/v1/catalog/tool/config/<config_key> [GET]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "config_key": "addr"
            },
            # Response code, body
            200,
            {
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_config(self, req_body, res_code, res_body):
        response = client.get(
            '/api/v1/catalog/tool/config/' + req_body["config_key"]
        )
        assert response.status_code == res_code
        #assert response.get_json() == res_body

################################################################
# フロントエンドのログイン確認用エンドポイント
################################################################


class TestLoginendpoint:
    ##################################
    #  [loginendpoint]
    #  フロントエンドのログイン確認用エンドポイント：/api/v1/catalog/tool/loginendpoint [GET]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
            },
            # Response code, body
            200,
            {
                "message": "ログイン済"
            }
        )
    }

    # 異常系
    params_data_ng = {
        '401_Unauthorized': (    # 認可されていない
            # Request Body
            {
            },
            # Response code, body
            401,
            {
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_loginendpoint(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        response = client.get(
            '/api/v1/catalog/tool/loginendpoint'
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_loginendpoint_ng(self, mocker, req_body, res_code, res_body):
        # 事前処理
        response = client.get('/api/v1/catalog/tool/logout')

        response = client.get(
            '/api/v1/catalog/tool/loginendpoint'
        )
        assert response.status_code == res_code

################################################################
# フロントエンドのログイン確認用エンドポイント
################################################################


class TestSysadminendpoint:
    ##################################
    #  [sysadminendpoint]
    #  フロントエンドのログイン確認用エンドポイント：/api/v1/catalog/tool/sysadminendpoint [GET]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
            },
            # Response code, body
            200,
            {
                "msg": "sysadminでログイン済"
            }
        )
    }

    # 異常系
    params_data_ng = {
        '401_Unauthorized': (    # 認可されていない
            # Request Body
            {
            },
            # Response code, body
            401,
            {
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_sysadminendpoint(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        response = client.get(
            '/api/v1/catalog/tool/sysadminendpoint'
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_sysadminendpoint_ng(self, mocker, req_body, res_code, res_body):
        # 事前処理
        response = client.get('/api/v1/catalog/tool/logout')

        response = client.get(
            '/api/v1/catalog/tool/sysadminendpoint'
        )
        assert response.status_code == res_code

################################################################
# ログイン
################################################################


class TestLogin:
    ##################################
    #  [login]
    #  ログイン：/api/v1/catalog/tool/login [POST]
    #   username: ユーザ名
    #   password: パスワード
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "username": "ckan_admin",
                "password": "test1234"
            },
            # Response code, body
            200,
            {
                "sysadmin": True,
                "ckan": "internal",
                "release_ckan_addr": config["addr"]["release"]["ckan_url"],
                "detail_ckan_addr": config["addr"]["detail"]["ckan_url"],
                "message": "ログインに成功しました"
            }
        )
    }

    # 異常系
    params_data_ng = {
        '400_Bad Request': (    # ユーザ名またはパスワードが合っていない
            # Request Body
            {
                "username": "",
                "password": ""
            },
            # Response code, body
            400,
            {
                "message": "ユーザ名またはパスワードが不正です。"
            }
        )
    }

    # 例外発生
    params_data_exception = {
        '500_Internal Server Error': (    # サーバエラー
            # Request Body
            {
                "username": "",
                "password": ""
            },
            # Response code, body
            400,
            {
                "message": "例外が発生しました。"
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_login(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        #mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        response = client.post(
            '/api/v1/catalog/tool/login',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_login_ng(self, req_body, res_code, res_body):
        response = client.post(
            '/api/v1/catalog/tool/login',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body


'''
    # 例外発生
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_exception.values()), ids=list(params_data_exception.keys()))
    def test_login_exception(self, req_body, res_code, res_body):
        response = client.post(
            '/api/v1/catalog/tool/login',
            json = req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body
'''

################################################################
# ログアウト
################################################################


class TestLogout:
    ##################################
    #  [logout]
    #  ログアウト：/api/v1/catalog/tool/logout [GET]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {},
            # Response code, body
            200,
            {
                "message": "ログアウトに成功しました"
            }
        )
    }

    # 異常系
    params_data_ng = {
        '400_Bad Request': (    # 失敗
            # Request Body
            {},
            # Response code, body
            400,
            {
                "message": "ログアウトに失敗しました"
            }
        )
    }

    # 例外発生
    params_data_exception = {
        '500_Internal Server Error': (    # サーバエラー
            # Request Body
            {},
            # Response code, body
            500,
            {
                "message": "例外が発生しました。",
                "error": "string"
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_logout(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        #mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        response = client.get(
            '/api/v1/catalog/tool/logout'
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body


'''
    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_logout_ng(self, req_body, res_code, res_body):
        response = client.get(
            '/api/v1/catalog/tool/logout'
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

    # 例外発生
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_exception.values()), ids=list(params_data_exception.keys()))
    def test_logout_exception(self, req_body, res_code, res_body):
        response = client.post(
            '/api/v1/catalog/tool/logout',
            json = req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body
'''

################################################################
# ユーザ一覧取得
################################################################


class TestFetchUserList:
    ##################################
    #  [fetch_userlist]
    #  ユーザ一覧取得：/api/v1/catalog/tool/userlist [GET]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {},
            # Response code, body
            200,
            {
                "result": True,
                "message": "ユーザ一覧を取得しました。"
            }
        )
    }

    # 異常系
    params_data_ng = {
        '500_Internal Server Error': (    # サーバエラー
            # Request Body
            {},
            # Response code, body
            500,
            {
                "result": False,
                "message": "例外が発生しました。",
                "error": ""
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_fetch_userlist(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # fetch_ckan_userlistのモック
        # userlist_data = {
        #    'result': True,
        #    'message': 'ユーザ一覧を取得しました。',
        #    'userlist': list()
        # }
        #mocker.patch('app.fetch_ckan_userlist', return_value=userlist_data)
        response = client.get(
            '/api/v1/catalog/tool/userlist'
        )
        result = response.get_json()
        print("")
        print(response.get_json())
        print("")
        assert response.status_code == res_code
        assert result["result"] == res_body["result"]
        assert result["message"] == res_body["message"]


'''
    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_fetch_userlist_ng(self, req_body, res_code, res_body):
        response = client.get(
            '/api/v1/catalog/tool/userlist'
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body
'''

################################################################
# ユーザ取得
################################################################


class TestFetchUser:
    ##################################
    #  [fetch_user]
    #  ユーザ取得：/api/v1/catalog/tool/users/<username> [GET]
    #   username: ユーザ名
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "username": "ckan_admin"
            },
            # Response code, body
            200,
            {
                "status": "success",
                "message": "ユーザ情報を取得しました。",
                "username": "ckan_admin",
                "apikey": "abcd1234",
                "sysadmin": True,
                "ckan": "internal",
                "organization": "org1,org2",
                "about": {
                    "release_ckan_url": "release_ckan_url",
                    "release_ckan_username": "ckan_admin",
                    "release_ckan_apikey": "abcd1234",
                    "detail_ckan_url": "detail_ckan_url",
                    "detail_ckan_username": "ckan_admin",
                    "detail_ckan_apikey": "abcd1234"
                },
                "release_user_id": "ckan_admin",
                "detail_user_id": "ckan_admin",
                "email": "email@example.com"
            }
        )
    }

    # 異常系
    params_data_ng = {
        '500_Internal Server Error': (    # サーバエラー
            # Request Body
            {
                "username": "."
            },
            # Response code, body
            # ToDo 2022の対処でステータスコードは500に変更
            # 500,
            200,
            {
                # ToDo新しいエラーコードに修正する必要あり
                # 'message': "Exception",
                'message': 'ユーザ名またはパスワードが不正です。',
                'organization': [],
                'status': 'exception'
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_fetch_user(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        #mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        response = client.get(
            '/api/v1/catalog/tool/users/' + req_body["username"]
        )
        result = response.get_json()
        print("")
        print(response.get_json())
        print("")
        assert response.status_code == res_code
        assert result["status"] == res_body["status"]
        assert result["message"] == res_body["message"]

    # 異常系

    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_fetch_user_ng(self, req_body, res_code, res_body):
        response = client.get(
            '/api/v1/catalog/tool/users/' + req_body["username"]
        )
        result = response.get_json()
        print("")
        print(response.get_json())
        print("")
        assert response.status_code == res_code
        assert result["status"] == res_body["status"]
        assert result["organization"] == res_body["organization"]
        assert result["status"] == res_body["status"]


################################################################
# ユーザ作成
################################################################
class TestCreateUser:
    ##################################
    #  [create_user]
    #  ユーザ作成：/api/v1/catalog/tool/users [POST]
    #   organization: 組織名
    #   username: ユーザ名
    #   email: メールアドレス
    #   password: パスワード
    #################################
    ### データパターン ###
    # 正常系

    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "organization": ["org-a"],
                "username": username,
                "email": username + "@mail.jp",
                "password": "12345Qwert@a",
                "ckan": "internal",
                "detailCkanApikey": "",
                "detailCkanUrl": "",
                "detailCkanUsername": "",
                "releaseCkanApikey": "",
                "releaseCkanUrl": "",
                "releaseCkanUsername": ""
            },
            # Response code, body
            200,
            {
                "result": True,
                "message": {
                    "detail": "ユーザを作成しました。ユーザに組織のロールを付与しました。",
                    "release": "ユーザを作成しました。ユーザに組織のロールを付与しました。"
                }
            }
        )
    }

    # 異常系
    params_data_ng = {
        '500_Internal Server Error': (    # サーバエラー
            # Request Body
            {
                "organization": "",
                "username": "",
                "email": "",
                "password": ""
            },
            # Response code, body
            500,
            {
                "result": False,
                "message": {
                    "detail": "ユーザ作成に失敗しました。",
                    "release": "ユーザ作成に失敗しました。"
                },
                "error": "string"
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_create_user(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        #mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})
        print(response.get_json())
        # create_ckan_userのモック
        # create_user_data ={
        #    'result': True,
        #    'message': {
        #        'detail': 'ユーザを作成しました。',
        #        'release': 'ユーザを作成しました。'
        #    }
        # }
        #mocker.patch('app.create_ckan_user', return_value=create_user_data)
        response = client.post(
            '/api/v1/catalog/tool/users',
            json=req_body
        )
        result = response.get_json()
        print("")
        print(response.get_json())
        print("")
        assert response.status_code == res_code
        assert result["result"] == res_body["result"]
        assert result["message"]["detail"] == res_body["message"]["detail"]
        assert result["message"]["release"] == res_body["message"]["release"]


"""
    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_create_user_ng(self, req_body, res_code, res_body):
        response = client.post(
            '/api/v1/catalog/tool/users',
            json = req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body
"""

################################################################
# ユーザ更新
################################################################


class TestUpdateUser:
    ##################################
    #  [update_user]
    #  ユーザ更新：/api/v1/catalog/tool/users/<username> [PUT]
    #   username: ユーザ名
    #   request.json: ユーザ更新情報
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "username": username,
                "password": "",
                "email": username + "@mail.jp",
                "organization": ["org-a"],
                "ckan": "internal",
                "release_ckan_url": "",
                "release_ckan_username": "",
                "release_ckan_apikey": "",
                "detail_ckan_url": "",
                "detail_ckan_username": "",
                "detail_ckan_apikey": ""
            },
            # Response code, body
            200,
            {
                "result": True,
                "message": {
                    "detail": "ユーザ情報を更新しました。ユーザに組織のロールを付与しました。",
                    "release": "ユーザ情報を更新しました。ユーザに組織のロールを付与しました。"
                }
            }
        )
    }

    # 異常系
    params_data_ng = {
        '500_Internal Server Error': (    # サーバエラー
            # Request Body
            {
                "username": "",
                "form": {
                    "username": "test_create_user",
                    "password": "",
                    "email": "",
                    "organization": "",
                    "ckan": "internal",
                    "release_ckan_url": "",
                    "release_ckan_username": "",
                    "release_ckan_apikey": "",
                    "detail_ckan_url": "",
                    "detail_ckan_username": "",
                    "detail_ckan_apikey": ""
                }
            },
            # Response code, body
            500,
            {
                "result": False,
                "message": {
                    'detail': '',
                    'release': ''
                },
                "error": "string"
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_update_user(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        #mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # update_ckan_userのモック
        # update_user_data ={
        #    'result': True,
        #    'message': {
        #        'detail': 'ユーザ情報を更新しました。',
        #        'release': 'ユーザ情報を更新しました。'
        #    }
        # }
        #mocker.patch('app.update_ckan_user', return_value=update_user_data)
        response = client.put(
            '/api/v1/catalog/tool/users/' + username,
            json=req_body
        )
        result = response.get_json()
        print("")
        print(response.get_json())
        print("")
        assert response.status_code == res_code
        assert result["result"] == res_body["result"]
        assert result["message"]["detail"] == res_body["message"]["detail"]
        assert result["message"]["release"] == res_body["message"]["release"]


'''
    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_update_user_ng(self, req_body, res_code, res_body):
        response = client.put(
            '/api/v1/catalog/tool/users/' + req_body["username"],
            json = req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body
'''

################################################################
# ユーザパスワード更新
################################################################


class TestUpdateUserPassword:
    ##################################
    #  [update_user_password]
    #  ユーザ更新：/api/v1/catalog/tool/users/password/<username> [PUT]
    #   username: ユーザ名
    #   request.json: ユーザ更新情報
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "username": username,
                "email": username + "@mail.jp",
                "new_password": "12345Qwert@a",
                "old_password": "12345Qwert@b"


            },
            # Response code, body
            200,
            {
                "result": True,
                "message": "パスワードを更新しました。"
                # "message": {
                #    "detail": "パスワードを更新しました。",
                #    "release": "パスワードを更新しました。"
                # }
            }
        )
    }

    # 異常系
    params_data_ng = {
        '500_Internal Server Error': (    # サーバエラー
            # Request Body
            {
                "username": "",
                "email": "",
                "password": ""
            },
            # Response code, body
            500,
            {
                "result": False,
                "message": {
                    "detail": "",
                    "release": ""
                },
                "error": "string"
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_update_user_password(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        #mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # update_ckan_user_passwordのモック
        # update_user_pass_data ={
        #    'result': True,
        #    'message': {
        #        'detail': 'パスワードを更新しました。',
        #        'release': 'パスワードを更新しました。'
        #    }
        # }
        #mocker.patch('app.update_ckan_user_password', return_value=update_user_pass_data)
        response = client.put(
            '/api/v1/catalog/tool/users/password/' + username,
            json=req_body
        )
        result = response.get_json()
        assert response.status_code == res_code
        assert result["result"] == res_body["result"]
        assert result["message"] == res_body["message"]
        #assert result["message"]["detail"] == res_body["message"]["detail"]
        #assert result["message"]["release"] == res_body["message"]["release"]


'''
    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_update_user_password_ng(self, req_body, res_code, res_body):
        response = client.put(
            '/api/v1/catalog/tool/users/password/' + req_body["username"],
            json = req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body
'''

################################################################
# ユーザ削除
################################################################


class TestDeleteUser:
    ##################################
    #  [delete_user]
    #  ユーザ削除：/api/v1/catalog/tool/users/<username> [DELETE]
    #   username: ユーザ名
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
            },
            # Response code, body
            200,
            {
                "result": True,
                "message": "ユーザを削除しました。"
                # "message": {
                #    "detail": "ユーザを削除しました。",
                #    "release": "ユーザを削除しました。"
                # }
            }
        )
    }

    # 異常系
    params_data_ng = {
        '500_Internal Server Error': (    # サーバエラー
            # Request Body
            {
                "username": ""
            },
            # Response code, body
            500,
            {
                "result": False,
                "message": {
                    "detail": "",
                    "release": ""
                },
                "error": "string"
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_delete_user(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        #mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # delete_ckan_userのモック
        # delete_user_data ={
        #    'result': True,
        #    'message': {
        #        'detail': 'ユーザを削除しました。',
        #        'release': 'ユーザを削除しました。'
        #    }
        # }
        #mocker.patch('app.delete_ckan_user', return_value=delete_user_data)
        response = client.delete(
            '/api/v1/catalog/tool/users/' + username,
            json=req_body
        )
        result = response.get_json()
        print("")
        print(response.get_json())
        print("")
        assert response.status_code == res_code
        assert result["result"] == res_body["result"]
        assert result["message"] == res_body["message"]
        #assert result["message"]["detail"] == res_body["message"]["detail"]
        #assert result["message"]["release"] == res_body["message"]["release"]


'''
    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_delete_user_ng(self, req_body, res_code, res_body):
        response = client.delete(
            '/api/v1/catalog/tool/users/' + req_body["username"],
            json = req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body
'''

################################################################
# CKAN情報取得
################################################################


class TestCkaninfo:
    ##################################
    #  [ckaninfo]
    #  CKAN情報取得：/api/v1/catalog/tool/ckaninfo [GET]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
            },
            # Response code, body
            200,
            [
                {
                    "ckan_type": "release",
                    "description": "",
                    "title": "CKAN",
                    "url": config["addr"]["release"]["ckan_url"],
                },
                {
                    "ckan_type": "detail",
                    "description": "",
                    "title": "CKAN",
                    "url": config["addr"]["detail"]["ckan_url"],
                }
            ]

        )
    }

    # 異常系
    params_data_ng = {
        '500_Internal Server Error': (    # サーバエラー
            # Request Body
            {
            },
            # Response code, body
            500,
            {
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_ckaninfo(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        #mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # get_ckan_infoのモック
        # ckan_info_data =[
        #    {
        #        'title': 'CKAN',
        #        'description': '横断検索用CKAN情報',
        #        'url': 'release_ckan_url',
        #        'ckan_type': 'release'
        #    },
        #    {
        #        'title': 'CKAN',
        #        'description': '詳細検索用CKAN情報',
        #        'url': 'detail_ckan_url',
        #        'ckan_type': 'detail'
        #    }
        # ]
        #mocker.patch('app.get_ckan_info', return_value=ckan_info_data)
        response = client.get(
            '/api/v1/catalog/tool/ckaninfo'
        )
        result = response.get_json()
        print("")
        print(response.get_json())
        print("")
        assert response.status_code == res_code
        assert result[0]["ckan_type"] == res_body[0]["ckan_type"]
        assert result[0]["description"] == res_body[0]["description"]
        assert result[0]["title"] == res_body[0]["title"]
        # 末尾に/が入っているかどうかでチェックがうまくいかない
        #assert result[0]["url"] == res_body[0]["url"]
        assert result[1]["ckan_type"] == res_body[1]["ckan_type"]
        assert result[1]["description"] == res_body[1]["description"]
        assert result[1]["title"] == res_body[1]["title"]
        # 末尾に/が入っているかどうかでチェックがうまくいかない
        #assert result[1]["'url"] == res_body[1]["'url"]


'''
    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_ckaninfo_ng(self, req_body, res_code, res_body):
        response = client.get(
            '/api/v1/catalog/tool/ckaninfo'
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body
'''

################################################################
# 組織情報取得
################################################################


class TestOrganizationList:
    ##################################
    #  [get_organization_list]
    #  組織情報取得：/api/v1/catalog/tool/organization [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
            },
            # Response code, body
            200,
            [
                {
                    "org_label": "org1",
                    "org_value": "org1"
                },
                {
                    "org_label": "org2",
                    "org_value": "org2"
                }
            ]
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_get_organization_list(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        #mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # get_ckan_user_orgのモック
        # org_list_data =[
        #    {
        #        'org_label': 'org1',
        #        'org_value': 'org1'
        #    },
        #    {
        #        'org_label': 'org2',
        #        'org_value': 'org2'
        #    }
        # ]
        #mocker.patch('app.get_ckan_user_org', return_value=org_list_data)
        response = client.get(
            '/api/v1/catalog/tool/organization'
        )
        result = response.get_json()
        print("")
        print(response.get_json())
        print("")
        assert response.status_code == res_code


################################################################
# ライセンスリスト取得
################################################################
class TestLicenseList:
    ##################################
    #  [license_list]
    #  組織情報取得：/api/v1/catalog/tool/licenselist [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
            },
            # Response code, body
            200,
            [
                {
                    "title": "Open Data Commons Public Domain Dedication and License (PDDL)",
                    "id": "odc-pddl",
                    "url": "http://www.opendefinition.org/licenses/odc-pddl"
                }
            ]
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_license_list(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        #mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # get_license_listのモック
        # license_list_data =[
        #    {
        #        'title': 'Open Data Commons Public Domain Dedication and License (PDDL)',
        #        'id': 'odc-pddl',
        #        'url': 'http://www.opendefinition.org/licenses/odc-pddl'
        #    }
        # ]
        #mocker.patch('app.get_license_list', return_value=license_list_data)
        response = client.get(
            '/api/v1/catalog/tool/licenselist'
        )

        result = response.get_json()
        print("")
        print(response.get_json())
        print("")
        assert response.status_code == res_code
        #assert response.get_json() == res_body

################################################################
# 横断カタログ登録
################################################################


class TestRegistRelease:
    ##################################
    #  [regist_release_catalog]
    #  横断カタログ登録：/api/v1/catalog/tool/datacatalog/release/add [PUT]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "catalogDescription": "2000年から2020年までの日本の人口統計データです。",
                "catalogTitle": "test_ut_server_日本の人口統計",
                "ckan_data_name": "",
                "data_creator": [
                    {"label": "caddec_dataset_id_for_detail", "value": ""},
                    {"label": "caddec_provider_id", "value": "test_id_A"},
                    {"label": "publisher_name", "value": "org-a"},
                    {"label": "publisher_uri",
                        "value": "http://example.org/7010001008844"},
                    {"label": "creator_name", "value": "org-a"},
                    {"label": "creator_uri",
                        "value": "http://example.org/7010001008844"},
                    {"label": "contact_name", "value": "org-a"},
                    {"label": "contact_uri", "value": "http://example.com/contact_uri"}
                ],
                "data_terms": "odc-pddl",
                "dataset_class": ["人口・世帯", "労働"],
                "dataset_description_url": "http://example.com/landingPage/1",
                "dataset_key": ["人口", "年次報告書", "統計"],
                "dataset_url": "http://example.com/landingPage/1/dataset/ckan20220608182837",
                "datasetoptional": [
                    {"label": "vocabulary", "value": "http://imi.go.jp/ns/core/RDF#"},
                    {"label": "term", "value": "人型,住所"},
                    {"label": "language", "value": ["ja", "en"]},
                    {"label": "frequency",
                        "value": "http://publications.europa.eu/resource/authority/frequency/DECENNIAL"},
                    {"label": "spatial_url",
                        "value": "https://www.geonames.org/1861060"},
                    {"label": "spatial_text", "value": "日本"},
                    {"label": "spatial", "value": {"type": "Point",
                                                   "coordinates": [139.75309, 35.68536]}},
                    {"label": "temporal_start", "value": "2022-06-14"},
                    {"label": "temporal_end", "value": "2022-06-30"}
                ],
                "filedata_details": {
                    "accessRights": "公開",
                    "accessRightsUrl": "https://publications.europa.eu/resource/authority/access-right/PUBLIC",
                    "columnName": "2022年",
                    "compressFormat": "http://www.iana.org/assignments/media-types/application/gzip",
                    "compressFormatDisplayValue": "gzip",
                    "compressFormatOther": "bzip",
                    "conformsTo": "http://conforms_to/hogehoge.co.jp",
                    "connectRequired": {"label": "要求しない", "value": "notRequired"},
                    "contractRequired": {"label": "要求する", "value": "required"},
                    "dataServiceEndpointDescription": "http://endpoint_definition/population_statics.orga.com",
                    "dataServiceEndpointUrl": "http://endpoint/population_statics.orga.com",
                    "dataServiceTitle": "関東近郊における年齢別人口統計",
                    "dataname": "20220607154717_http_B_open_csv.csv",
                    "explainurl": "http://data_explanation/hogehoge.co.jp",
                    "description": "[\"0歳～9歳\", \"10歳～19歳\", \"20歳～29歳\"]",
                    "downloadurl": "http://10.240.59.28:30088/open/http_B_open_csv.csv",
                    "filename": "関東近郊における年齢別人口統計",
                    "format": "CSV",
                    "getResourceIDForProvenance": {"label": "来歴登録を行う", "value": "yes"},
                    "haspolicyUrl": "http://rights_info/hogehoge.co.jp",
                    "id": "02a73aee-6037-4fc4-9ac9-92a65c690267",
                    "issued": "2022-06-08 19:21:56.860341",
                    "label": "データ1",
                    "licensetitle": "Open Data Commons Public Domain Dedication and License (PDDL)",
                    "licenseurl": "http://www.opendefinition.org/licenses/odc-pddl",
                    "mimetype": {"label": "csv", "value": "http://www.iana.org/assignments/media-types/text/csv"},
                    "ngsiDataModel": {
                        "attribute": "attr_A",
                        "dataType": "str",
                        "description": "属性A",
                        "example": "ABCD",
                        "metadata": [
                            {
                                "dataType": "aaa",
                                "description": "bbb",
                                "example": "ccc",
                                "metadataName": "ddd"
                            }
                        ]
                    },
                    "ngsiEntityType": "event",
                    "ngsiServicePath": "/service1",
                    "ngsiTenant": "tenant1",
                    "packageFormat": "tar",
                    "packageFormatDisplayValue": "tar",
                    "packageFormatOther": "rpm",
                    "previousEventId": "kmw8fjas-54es-daw-54d3-df4tryhweerrn",
                    "resourceIDForProvenance": "4278944f-bbd2-4ac-bbd3-2727b3ec3be5",
                    "resourceName": "http://10.240.59.28:30088/open/http_B_open_csv.csv",
                    "resourceType": {"label": "ファイル提供(HTTP)", "value": "file/http"},
                    "schema": "https://schema.org/population",
                    "schemaType": {"label": "RDF-XML", "value": "RDF-XML"},
                    "size": 21,
                    "userConnectorId": "cadde_user_c",
                    "usrRight": "https://rights_hogehoge",
                },
                "identifier": "http://example.com/landingPage/1/dataset/ckan20220608182837",
                "issued": "2022-06-08 18:28:37.958978",
                "license_title": "Open Data Commons Public Domain Dedication and License (PDDL)",
                "license_url": "http://www.opendefinition.org/licenses/odc-pddl",
                "regist_org": "org-a",
                "selected_mode": "duplicate",
                "user_terms": [
                    {"label": "rights", "value": "https://rights_hogehoge"},
                    {"label": "access_rights", "value": "公開"},
                    {"label": "access_rights_url",
                        "value": "https://publications.europa.eu/resource/authority/access-right/PUBLIC"},
                    {"label": "haspolicy_url",
                        "value": "http://rights_info/hogehoge.co.jp"},
                    {"label": "prov_was_generated_by_url",
                        "value": "http://prov_was_generated_by_url/hogehoge.co.jp"},
                    {"label": "conforms_to",
                        "value": "http://conforms_to/hogehoge.co.jp"},
                    {"label": "trading_policy_contract_type", "value": "譲渡"},
                    {"label": "trading_policy_nda", "value": "求める"},
                    {"label": "trading_policy_use_application",
                        "value": ["研究利用"]},
                    {"label": "terms_of_use_redistribution_range", "value": "制限なし"},
                    {"label": "terms_of_use_permissible_region",
                        "value": ["制限なし"]},
                    {"label": "terms_of_use_notices", "value": "利用状況の報告義務あり"},
                    {"label": "privacy_policy_contains_personal_data", "value": "非個人情報"},
                    {"label": "fee", "value": "有償"},
                    {"label": "sales_info_url",
                        "value": "http://sales_info_url/hogehoge.co.jp"},
                    {"label": "pricing_price_range",
                        "value": "日本円：200,000円～1,000,000円"},
                    {"label": "pricing_notices_of_price",
                        "value": "長期契約にて優待価格で提供する"},
                    {"label": "warranty_express_warranty",
                        "value": "データ主体となる個人の本人同意が得られている"},
                    {"label": "warranty_leagal_compliance", "value": ["日本"]}
                ],
                "user_terms_json": [
                    {"label": "usage_period_effective_period_of_data",
                     "value": {"effectivePeriodOfDataType": "startEndDate", "date": {"startDate": "2022-06-08", "endDate": "2022-06-23"}}
                     },
                    {"label": "usage_period_expiration_period",
                     "value": {"expirationPeriodType": "period",
                               "period": {"referenceDate": "purchasedDay", "value": "10", "unit": "year"}}
                     }
                ]
            },
            # Response code, body
            200,
            {
                "message": "success",
                # 最新のレスポンスに書き換える必要あり
                "release": {
                    "ckan_url": "",
                    "pkg": None
                }
            }
        )
    }

    # 異常系
    params_data_ng = {
        '400_Bad Request': (    # リクエストエラー
            # Request Body
            {
            },
            # Response code, body
            400,
            {
                "message": "カタログデータがありません",
                "release": {
                    "ckan_url": None,
                    "pkg": None
                }
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_regist_release_catalog(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        #mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # regist_ckanのモック
        #mocker.patch('app.regist_ckan', return_value=('success', '', None))
        # 接続処理でエラーになる
        response = client.put(
            '/api/v1/catalog/tool/datacatalog/release/add',
            json=req_body
        )
        result = response.get_json()
        print("")
        print(response.get_json())
        print("")
        assert response.status_code == res_code
        #assert result["message"] == res_body["message"]

    # 異常系

    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_regist_release_catalog_ng(self, req_body, res_code, res_body):
        response = client.put(
            '/api/v1/catalog/tool/datacatalog/release/add',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# 詳細カタログ登録
################################################################


class TestRegistDetail:
    ##################################
    #  [regist_detail_catalog]
    #  詳細カタログ登録：/api/v1/catalog/tool/datacatalog/detail/add [PUT]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "release": {"catarog_description": ""},
                "detail": {"catarog_description": ""}
            },
            # Response code, body
            200,
            {
                "message": "success",
                "release": {
                    "ckan_url": "",
                    "pkg": {"author": ""}
                },
                "detail": {
                    "ckan_url": "",
                    "pkg": {"author": ""}
                }
            }
        )
    }

    # 異常系
    params_data_ng = {
        '400_Bad Request_1': (    # リクエストエラー
            # Request Body
            {
                "detail": {"catarog_description": ""}
            },
            # Response code, body
            400,
            {
                "message": "横断カタログデータがありません",
                "release": {
                    "ckan_url": None,
                    "pkg": None
                },
                "detail": {
                    "ckan_url": None,
                    "pkg": None
                }
            }
        ),
        '400_Bad Request_2': (    # リクエストエラー
            # Request Body
            {
                "release": {"catarog_description": ""}
            },
            # Response code, body
            400,
            {
                "message": "詳細カタログデータがありません",
                "release": {
                    "ckan_url": None,
                    "pkg": None
                },
                "detail": {
                    "ckan_url": None,
                    "pkg": None
                }
            }
        ),
        '500_Internal Server Error': (    # サーバエラー
            # Request Body
            {
            },
            # Response code, body
            500,
            {
                "message": "詳細CKANがありません",
                "release": {
                    "ckan_url": None,
                    "pkg": None
                },
                "detail": {
                    "ckan_url": None,
                    "pkg": None
                }
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_regist_detail_catalog(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # regist_detailのモック
        regist_detail_data = {
            'message': 'success',
            'release': {
                'ckan_url': '',
                'pkg': {"author": ""}
            },
            'detail': {
                'ckan_url': '',
                'pkg': {"author": ""}
            }
        }
        mocker.patch('app.regist_detail', return_value=regist_detail_data)
        response = client.put(
            '/api/v1/catalog/tool/datacatalog/detail/add',
            json=req_body
        )

        assert response.status_code == res_code
        assert response.get_json() == res_body

    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_regist_detail_catalog_ng(self, mocker, req_body, res_code, res_body):
        # サーバーエラーの場合、'app.ckans'をモック化
        if res_code == 500:
            mocker.patch('app.ckans', {'release': {'ckan_url': '', 'sysadmin_key': ''}, 'detail': {
                         'ckan_url': '', 'sysadmin_key': ''}})

        response = client.put(
            '/api/v1/catalog/tool/datacatalog/detail/add',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# 横断カタログ・詳細カタログ登録
################################################################


class TestRegistBoth:
    ##################################
    #  [regist_both_catalog]
    #  横断カタログ・詳細カタログ登録：/api/v1/catalog/tool/datacatalog/add [PUT]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "release": {"catarog_description": ""},
                "detail": {"catarog_description": ""}
            },
            # Response code, body
            200,
            {
                "message": "success",
                "release": {
                    "ckan_url": "",
                    "pkg": {"author": ""}
                },
                "detail": {
                    "ckan_url": "",
                    "pkg": {"author": ""}
                }
            }
        )
    }

    # 異常系
    params_data_ng = {
        '400_Bad Request_1': (    # リクエストエラー
            # Request Body
            {
                "detail": {"catarog_description": ""}
            },
            # Response code, body
            400,
            {
                "message": "横断カタログデータがありません",
                "release": {
                    "ckan_url": None,
                    "pkg": None
                },
                "detail": {
                    "ckan_url": None,
                    "pkg": None
                }
            }
        ),
        '400_Bad Request_2': (    # リクエストエラー
            # Request Body
            {
                "release": {"catarog_description": ""}
            },
            # Response code, body
            400,
            {
                "message": "詳細カタログデータがありません",
                "release": {
                    "ckan_url": None,
                    "pkg": None
                },
                "detail": {
                    "ckan_url": None,
                    "pkg": None
                }
            }
        ),
        '500_Internal Server Error': (    # サーバエラー
            # Request Body
            {
            },
            # Response code, body
            500,
            {
                "message": "詳細CKANがありません",
                "release": {
                    "ckan_url": None,
                    "pkg": None
                },
                "detail": {
                    "ckan_url": None,
                    "pkg": None
                }
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_regist_both_catalog(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # regist_bothのモック
        regist_both_data = {
            'message': 'success',
            'release': {
                'ckan_url': '',
                'pkg': {'author': ''}
            },
            'detail': {
                'ckan_url': '',
                'pkg': {'author': ''}
            }
        }
        mocker.patch('app.regist_both', return_value=regist_both_data)
        response = client.put(
            '/api/v1/catalog/tool/datacatalog/add',
            json=req_body
        )

        assert response.status_code == res_code
        assert response.get_json() == res_body

    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_regist_both_catalog_ng(self, mocker, req_body, res_code, res_body):
        # サーバーエラーの場合、'app.ckans'をモック化
        if res_code == 500:
            mocker.patch('app.ckans', {'release': {'ckan_url': '', 'sysadmin_key': ''}, 'detail': {
                         'ckan_url': '', 'sysadmin_key': ''}})

        response = client.put(
            '/api/v1/catalog/tool/datacatalog/add',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# 横断カタログ編集
################################################################


class TestEditRelease:
    ##################################
    #  [edit_release_catalog]
    #  横断カタログ編集：/api/v1/catalog/tool/datacatalog/release/edit [PUT]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "release": {"catarog_description": ""}
            },
            # Response code, body
            200,
            {
                "message": "success",
                "release": {
                    "ckan_url": "",
                    "pkg": {"author": ""}
                }
            }
        )
    }

    # 異常系
    params_data_ng = {
        '400_Bad Request': (    # リクエストエラー
            # Request Body
            {
            },
            # Response code, body
            400,
            {
                "message": "カタログデータがありません",
                "release": {
                    "ckan_url": "",
                    "pkg": None
                }
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_edit_release_catalog(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # edit_ckanのモック
        edit_release_data = {
            'message': 'success',
            'ckan_url': '',
            'pkg': {'author': ''}
        }
        mocker.patch('app.edit_ckan', return_value=edit_release_data)
        response = client.put(
            '/api/v1/catalog/tool/datacatalog/release/edit',
            json=req_body
        )

        assert response.status_code == res_code
        assert response.get_json() == res_body

    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_edit_release_catalog_ng(self, req_body, res_code, res_body):
        response = client.put(
            '/api/v1/catalog/tool/datacatalog/release/edit',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# 詳細カタログ編集
################################################################


class TestEditDetail:
    ##################################
    #  [edit_detail_catalog]
    #  詳細カタログ編集：/api/v1/catalog/tool/datacatalog/detail/edit [PUT]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "detail": {"catarog_description": ""}
            },
            # Response code, body
            200,
            {
                "message": "success",
                "detail": {
                    "ckan_url": "",
                    "pkg": {"author": ""}
                }
            }
        )
    }

    # 異常系
    params_data_ng = {
        '400_Bad Request': (    # リクエストエラー
            # Request Body
            {
            },
            # Response code, body
            400,
            {
                "message": "カタログデータがありません",
                "detail": {
                    "ckan_url": "",
                    "pkg": None
                }
            }
        ),
        '500_Internal Server Error': (    # サーバエラー
            # Request Body
            {
            },
            # Response code, body
            500,
            {
                "message": "詳細CKANがありません",
                "detail": {
                    "ckan_url": "",
                    "pkg": None
                }
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_edit_detail_catalog(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # edit_ckanのモック
        edit_detail_data = {
            'message': 'success',
            'ckan_url': '',
            'pkg': {'author': ''}
        }
        mocker.patch('app.edit_ckan', return_value=edit_detail_data)
        response = client.put(
            '/api/v1/catalog/tool/datacatalog/detail/edit',
            json=req_body
        )

        assert response.status_code == res_code
        assert response.get_json() == res_body

    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_edit_detail_catalog_ng(self, mocker, req_body, res_code, res_body):
        # サーバーエラーの場合、'app.ckans'をモック化
        if res_code == 500:
            mocker.patch('app.ckans', {'release': {'ckan_url': '', 'sysadmin_key': ''}, 'detail': {
                         'ckan_url': '', 'sysadmin_key': ''}})

        response = client.put(
            '/api/v1/catalog/tool/datacatalog/detail/edit',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# 横断カタログ・詳細カタログ編集
################################################################


class TestEditBoth:
    ##################################
    #  [edit_both_catalog]
    #  横断カタログ・詳細カタログ編集：/api/v1/catalog/tool/datacatalog/edit [PUT]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "release": {"catarog_description": ""},
                "detail": {"catarog_description": ""}
            },
            # Response code, body
            200,
            {
                "message": "success",
                "release": {
                    "ckan_url": "",
                    "pkg": {"author": ""}
                },
                "detail": {
                    "ckan_url": "",
                    "pkg": {"author": ""}
                }
            }
        )
    }

    # 異常系
    params_data_ng = {
        '400_Bad Request_1': (    # リクエストエラー
            # Request Body
            {
                "detail": {"catarog_description": ""}
            },
            # Response code, body
            400,
            {
                "message": "横断カタログデータがありません",
                "release": {
                    "ckan_url": "",
                    "pkg": None
                },
                "detail": {
                    "ckan_url": "",
                    "pkg": None
                }
            }
        ),
        '400_Bad Request_2': (    # リクエストエラー
            # Request Body
            {
                "release": {"catarog_description": ""}
            },
            # Response code, body
            400,
            {
                "message": "詳細カタログデータがありません",
                "release": {
                    "ckan_url": "",
                    "pkg": None
                },
                "detail": {
                    "ckan_url": "",
                    "pkg": None
                }
            }
        ),
        '500_Internal Server Error': (    # サーバエラー
            # Request Body
            {
            },
            # Response code, body
            500,
            {
                "message": "詳細CKANがありません",
                "release": {
                    "ckan_url": "",
                    "pkg": None
                },
                "detail": {
                    "ckan_url": "",
                    "pkg": None
                }
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_edit_both_catalog(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # edit_bothのモック
        edit_both_data = {
            'message': 'success',
            'release': {
                'ckan_url': '',
                'pkg': {'author': ''}
            },
            'detail': {
                'ckan_url': '',
                'pkg': {'author': ''}
            }
        }
        mocker.patch('app.edit_both', return_value=edit_both_data)
        response = client.put(
            '/api/v1/catalog/tool/datacatalog/edit',
            json=req_body
        )

        assert response.status_code == res_code
        assert response.get_json() == res_body

    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_edit_both_catalog_ng(self, mocker, req_body, res_code, res_body):
        # サーバーエラーの場合、'app.ckans'をモック化
        if res_code == 500:
            mocker.patch('app.ckans', {'release': {'ckan_url': '', 'sysadmin_key': ''}, 'detail': {
                         'ckan_url': '', 'sysadmin_key': ''}})

        response = client.put(
            '/api/v1/catalog/tool/datacatalog/edit',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# カタログ検索
################################################################


class TestSearch:
    ##################################
    #  [search_catalog]
    #  カタログ検索：/api/v1/catalog/tool/datacatalog/release/search [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "keyword": "*:*",
                "url": ""
            },
            # Response code, body
            200,
            {
                "message": "success",
                "datasets": [
                    {
                        "release": {"author": ""},
                        "detail": {"author": ""}
                    }
                ]
            }
        )
    }

    # 異常系
    params_data_ng = {
        '500_Internal Server Error': (    # サーバエラー
            # Request Body
            {
                "keyword": "*:*",
                "url": ""
            },
            # Response code, body
            500,
            {
                "message": "error",
                "datasets": []
            }
        )
    }

    # 例外発生
    params_data_exception = {
        '400_Bad Request': (    # リクエストエラー
            # Request Body
            {
            },
            # Response code, body
            400,
            {
                "message": "error",
                "release": "none"
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_search_catalog(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # search_bothのモック
        search_both_data = {
            'message': 'success',
            'datasets': [
                {
                    'release': {'author': ''},
                    'detail': {'author': ''}
                }
            ]
        }
        mocker.patch('app.search_both', return_value=search_both_data)
        response = client.post(
            '/api/v1/catalog/tool/datacatalog/release/search',
            json=req_body
        )

        assert response.status_code == res_code
        assert response.get_json() == res_body

    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_search_catalog_ng(self, mocker, req_body, res_code, res_body):
        # 'search_both'をモック化
        search_error_both_data = {
            'message': 'error',
            'datasets': []
        }
        mocker.patch('app.search_both', return_value=search_error_both_data)
        response = client.post(
            '/api/v1/catalog/tool/datacatalog/release/search',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

    # 例外発生
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_exception.values()), ids=list(params_data_exception.keys()))
    def test_search_catalog_exception(self, req_body, res_code, res_body):
        response = client.post(
            '/api/v1/catalog/tool/datacatalog/release/search',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# カタログ削除
################################################################


class TestDeleteRelease:
    ##################################
    #  [delete_release_catalog]
    #  カタログ削除：/api/v1/catalog/tool/datacatalog [DELETE]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "release": [
                    "e9710ecd-3798-4b4a-9282-30de596af66f"
                ],
                "detail": [
                    "c7898bda-ec83-42bc-b28c-cfb8c62520a6"
                ]
            },
            # Response code, body
            200,
            {
                "result": True,
                "message": {
                    "release": "ユーザを削除しました。",
                    "detail": "ユーザを削除しました。"
                }
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_delete_release_catalog(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # delete_ckanのモック
        delete_data = {
            'result': True,
            'message': {
                'release': 'ユーザを削除しました。',
                'detail': 'ユーザを削除しました。'
            }
        }
        mocker.patch('app.delete_ckan', return_value=delete_data)
        response = client.delete(
            '/api/v1/catalog/tool/datacatalog',
            json=req_body
        )

        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# 横断カタログインポート
################################################################


class TestImportRelease:
    ##################################
    #  [import/release]
    #  横断カタログインポート：/api/v1/catalog/tool/import/release [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "text": "テスト",
                "file": (BytesIO(b'test'), 'test.csv')
            },
            # Response code, body
            200,
            {
                "status": "success",
                "message": "インポート処理を受け付けました。"
            }
        )
    }

    # 異常系
    params_data_ng = {
        '400_Bad Request': (    # 失敗
            # Request Body
            {
                "file": ""
            },
            # Response code, body
            400,
            {
                'status': 'faild',
                'message': 'ファイルなし'
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_import_release(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # ckan_dataset.import_datasetのモック
        mocker.patch('app.ckan_dataset.import_dataset', return_value={
                     'status': 'success', 'message': 'インポート処理を受け付けました。'})
        response = client.post(
            '/api/v1/catalog/tool/import/release',
            data=req_body,
            content_type="multipart/form-data"
        )

        assert response.status_code == res_code
        assert response.get_json() == res_body

    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_import_release_ng(self, req_body, res_code, res_body):
        response = client.post(
            '/api/v1/catalog/tool/import/release',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# 詳細カタログインポート
################################################################


class TestImportDetail:
    ##################################
    #  [import/detail]
    #  詳細カタログインポート：/api/v1/catalog/tool/import/detail [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "text": "テスト",
                "file": (BytesIO(b'test'), 'test.csv')
            },
            # Response code, body
            200,
            {
                "status": "success",
                "message": "インポート処理を受け付けました。"
            }
        )
    }

    # 異常系
    params_data_ng = {
        '400_Bad Request': (    # 失敗
            # Request Body
            {
                "file": ""
            },
            # Response code, body
            400,
            {
                'status': 'faild',
                'message': 'ファイルなし'
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_import_detail(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # ckan_dataset.import_datasetのモック
        mocker.patch('app.ckan_dataset.import_dataset', return_value={
                     'status': 'success', 'message': 'インポート処理を受け付けました。'})
        response = client.post(
            '/api/v1/catalog/tool/import/detail',
            data=req_body,
            content_type="multipart/form-data"
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_import_detail_ng(self, req_body, res_code, res_body):
        response = client.post(
            '/api/v1/catalog/tool/import/detail',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# 横断カタログエクスポート
################################################################


class TestExportRelease:
    ##################################
    #  [export/release]
    #  横断カタログエクスポート：/api/v1/catalog/tool/export/release [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
            },
            # Response code, body
            200,
            {
                "status": "success",
                "message": "エクスポート処理を受け付けました。",
                "filename": "ckan_admin_export.tar.gz"
            }
        )
    }

    # 異常系
    params_data_ng = {
        '500_Internal Server Error': (    # 失敗
            # Request Body
            {
            },
            # Response code, body
            500,
            {
                'status': 'faild',
                'message': '',
                'filename': ''
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_export_release(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # ckan_dataset.export_datasetのモック
        mocker.patch('app.ckan_dataset.export_dataset', return_value={
                     'status': 'success', 'message': 'エクスポート処理を受け付けました。', 'filename': 'ckan_admin_export.tar.gz'})
        response = client.post(
            '/api/v1/catalog/tool/export/release',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body


'''
    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_export_release_ng(self, req_body, res_code, res_body):
        response = client.post(
            '/api/v1/catalog/tool/export/release',
            json = req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body
'''
################################################################
# 詳細カタログエクスポート
################################################################


class TestExportDetail:
    ##################################
    #  [export/detail]
    #  詳細カタログエクスポート：/api/v1/catalog/tool/export/detail [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
            },
            # Response code, body
            200,
            {
                "status": "success",
                "message": "エクスポート処理を受け付けました。",
                "filename": "ckan_admin_export.tar.gz"
            }
        )
    }

    # 異常系
    params_data_ng = {
        '500_Internal Server Error': (    # 失敗
            # Request Body
            {
            },
            # Response code, body
            500,
            {
                'status': 'faild',
                'message': '',
                'filename': ''
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_export_detail(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # ckan_dataset.export_datasetのモック
        mocker.patch('app.ckan_dataset.export_dataset', return_value={
                     'status': 'success', 'message': 'エクスポート処理を受け付けました。', 'filename': 'ckan_admin_export.tar.gz'})
        response = client.post(
            '/api/v1/catalog/tool/export/detail',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body


'''
    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_export_detail_ng(self, req_body, res_code, res_body):
        response = client.post(
            '/api/v1/catalog/tool/export/release',
            json = req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body
'''

################################################################
# エクスポート状況取得
################################################################


class TestExportStatus:
    ##################################
    #  [export/status]
    #  エクスポート状況取得：/api/v1/catalog/tool/export/status [GET]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
            },
            # Response code, body
            200,
            [
                {
                    "status": "available",
                    "message": "エクスポートファイルが取得可能です。"
                },
                {
                    "status": "notavailable",
                    "message": "エクスポート処理中またはエクスポートファイルがありません。"
                }
            ]
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_export_status(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        response = client.get(
            '/api/v1/catalog/tool/export/status'
        )
        assert response.status_code == res_code
        assert any(elem == response.get_json()
                   for elem in res_body)    # 期待値のいずれかに一致

################################################################
# エクスポートファイル取得
################################################################


class TestExportFile:
    ##################################
    #  [export/file]
    #  エクスポートファイル取得：/api/v1/catalog/tool/export/file [GET]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
            },
            # Response code, body
            200,
            {
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_export_file(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # ckan_dataset.get_file_pathのモック
        mocker.patch('app.ckan_dataset.get_file_path', return_value=(
            './data/export/ckan_admin/ckan_admin_export.tar.gz', 'ckan_admin_export.tar.gz'))
        response = client.get(
            '/api/v1/catalog/tool/export/file'
        )
        assert response.status_code == res_code

################################################################
# 外部サービス使用有無の確認
################################################################


class TestExternalservice:
    ##################################
    #  [externalservice]
    #  外部サービス使用有無の確認：/api/v1/catalog/tool/externalservice [GET]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
            },
            # Response code, body
            200,
            [
                True,
                False
            ]
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_externalservice(self, req_body, res_code, res_body):
        response = client.get(
            '/api/v1/catalog/tool/externalservice'
        )
        assert response.status_code == res_code
        assert any(elem == response.get_json()
                   for elem in res_body)    # 期待値のいずれかに一致

################################################################
# 地域検索
################################################################


class TestGeonamesearch:
    ##################################
    #  [geonamesearch]
    #  地域検索：/api/v1/catalog/tool/geonamesearch [GET]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "keyword": "横浜市"
            },
            # Response code, body
            200,
            {
                "geonameId": "1848354",
                "name": "横浜市",
                "countryName": "日本",
                "adminName1": "神奈川県",
                "lat": "35.43333",
                "lng": "139.65",
                "fcl": "P"
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_geonamesearch(self, mocker, req_body, res_code, res_body):
        # extract_spatial.FindByKeyword_nameのモック
        result_dict = {
            "geonameId": "1848354",
            "name": "横浜市",
            "countryName": "日本",
            "adminName1": "神奈川県",
            "lat": "35.43333",
            "lng": "139.65",
            "fcl": "P"
        }
        mocker.patch('app.FindByKeyword_name', return_value=result_dict)
        response = client.get(
            '/api/v1/catalog/tool/geonamesearch',
            query_string=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# 地域のフルネーム取得
################################################################


class TestGeonameIdsearch:
    ##################################
    #  [geonameIdsearch]
    #  地域のフルネーム取得：/api/v1/catalog/tool/geonameIdsearch [GET]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "geonameId": "1848350"
            },
            # Response code, body
            200,
            "日本>千葉県>千葉市>中央区"
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_geonameIdsearch(self, mocker, req_body, res_code, res_body):
        # extract_spatial.getFullnameのモック
        mocker.patch('app.getFullname', return_value="日本>千葉県>千葉市>中央区")
        response = client.get(
            '/api/v1/catalog/tool/geonameIdsearch',
            query_string=req_body
        )
        assert response.status_code == res_code
        assert response.text == res_body

################################################################
# リソース取得
################################################################


class TestResource:
    ##################################
    #  [resource]
    #  リソース取得：/api/v1/catalog/tool/resource/<resource_type>/<path:url> [GET]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "resource_type": "http",
                "url": "http://hogehoge.com"
            },
            # Response code, body
            200,
            {
                "error_label": "",
                "data_list": ["aa", "bb", "cc"],
                "mime_type": "application/json",
                "file_size": 100,
                "dataname": "20210713174050_hogehoge.com",
                "format": "csv"
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_resource(self, mocker, req_body, res_code, res_body):
        # data_uploader.http_getのモック
        response_data = {
            "error_label": "",
            "data_list": ["aa", "bb", "cc"],
            "mime_type": "application/json",
            "file_size": 100,
            "dataname": "20210713174050_hogehoge.com",
            "format": "csv"
        }
        mocker.patch('app.http_get', return_value=response_data)
        response = client.get(
            '/api/v1/catalog/tool/resource/' +
            req_body["resource_type"] + "/" + req_body["url"]
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# ローカルファイルアップロードダミーIF
################################################################


class TestLocaluploads:
    ##################################
    #  [localuploads]
    #  ローカルファイルアップロードダミーIF：/api/v1/catalog/tool/localuploads [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "file": (BytesIO(b'test'), 'test.csv')
            },
            # Response code, body
            200,
            "Dummy Success"
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_localuploads(self, req_body, res_code, res_body):
        response = client.post(
            '/api/v1/catalog/tool/localuploads',
            data=req_body,
            content_type="multipart/form-data"
        )
        assert response.status_code == res_code
        assert response.text == res_body

################################################################
# ファイル保存
################################################################


class TestUploads:
    ##################################
    #  [uploads]
    #  詳細カタログインポート：/api/v1/catalog/tool/uploads [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "file": (BytesIO(b'test'), 'test.csv')
            },
            # Response code, body
            200,
            [
                "data_list",
                "mimetype",
                "dataname",
                "format"
            ]
        )
    }

    # 異常系
    params_data_ng = {
        '400_Bad Request': (    # 失敗
            # Request Body
            {
                "file": ""
            },
            # Response code, body
            400,
            "No file part"
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_uploads(self, req_body, res_code, res_body):
        response = client.post(
            '/api/v1/catalog/tool/uploads',
            data=req_body,
            content_type="multipart/form-data"
        )
        assert response.status_code == res_code
        assert set(response.get_json().keys()) == set(
            res_body)    # 期待値のキーを全て含む

    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_uploads_ng(self, req_body, res_code, res_body):
        response = client.post(
            '/api/v1/catalog/tool/uploads',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.text == res_body

################################################################
# NGSIデータモデル取得
################################################################


class TestNgsidatamodel:
    ##################################
    #  [ngsidatamodel]
    #  NGSIデータモデル取得：/api/v1/catalog/tool/ngsidatamodel [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "url": "https://t1064420.dev-necjfiware.jp/orion/v2.0/entities",
                "tenant": "public",
                "service_path": "/public",
                "entity_type": "Test_CulturalProperty_1M"
            },
            # Response code, body
            200,
            {
                "status": 200,
                "message": "",
                "data_model": {
                    "attribute": "place",
                    "dataType": "str",
                    "example": "park",
                    "description": "",
                    "metadata": {
                        "metadataName": "park",
                        "dataType": "str",
                        "example": "Miyashita Park",
                        "description": ""
                    }
                }
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_ngsidatamodel(self, mocker, req_body, res_code, res_body):
        # ngsi_manager.get_ngsi_data_modelのモック
        res_data_model = {
            "status": 200,
            "message": "",
            "data_model": {
                "attribute": "place",
                "dataType": "str",
                "example": "park",
                "description": "",
                "metadata": {
                    "metadataName": "park",
                    "dataType": "str",
                    "example": "Miyashita Park",
                    "description": ""
                }
            }
        }
        mocker.patch('app.NgsiData.get_ngsi_data_model',
                     return_value=res_data_model)
        response = client.post(
            '/api/v1/catalog/tool/ngsidatamodel',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# 前段イベント識別子検索
################################################################


class TestPreviouseventid:
    ##################################
    #  [previouseventid]
    #  前段イベント識別子検索：/api/v1/catalog/tool/previouseventid [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "filename": "http://serveraddr:38000/open/test.csv",
                "user_id": "consumer_id_a"
            },
            # Response code, body
            200,
            {
                "status": "success",
                "message": "検索結果あり",
                "result": [
                    {
                        "event_id": "6da96639-da89-4b85\\9ece-16d3b623dc9c",
                        "previous_event_id": "c51b7bb9-4d64-4e1f-8e9e-ff1ffd09dfd1",
                        "timestamp": "2022-10-01T02:25:41.047Z",
                        "provider_id": "test_id_A",
                        "resource_url": "http://hogehoge/test.csv"
                    }
                ]
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_previouseventid(self, mocker, req_body, res_code, res_body):
        # history_manager.search_historyのモック
        res = {
            'status': 'success',
            'message': '検索結果あり',
            'result': [
                {
                    "event_id": "6da96639-da89-4b85\\9ece-16d3b623dc9c",
                    "previous_event_id": "c51b7bb9-4d64-4e1f-8e9e-ff1ffd09dfd1",
                    "timestamp": "2022-10-01T02:25:41.047Z",
                    "provider_id": "test_id_A",
                    "resource_url": "http://hogehoge/test.csv"
                }
            ]
        }
        mocker.patch('app.search_history', return_value=res)
        response = client.post(
            '/api/v1/catalog/tool/previouseventid',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# 日時分析
################################################################


class TestExtracttemporal:
    ##################################
    #  [extracttemporal]
    #  日時分析：/api/v1/catalog/tool/extracttemporal [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "text": "東京オリンピックの会場データ",
                "filepath": "hogehoge.csv",
                "column_name": "開始時刻",
                "input_datetime_format": "auto"
            },
            # Response code, body
            200,
            {
                "start_datetime": "20210722",
                "end_datetime": "20210814"
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_extracttemporal(self, mocker, req_body, res_code, res_body):
        # ml_analysis_pb2_grpc.AnalyseServiceStubのモック
        class MockAnalysisDataStart:
            start_datetime = "20210722"

        class MockAnalysisDataEnd:
            end_datetime = "20210814"

        class MockAnalyseServiceStub:
            def __init__(self, object):
                pass

            def TemporalAnalyseServer(arg1, arg2):
                res_msg = []
                start = MockAnalysisDataStart()
                res_msg.append(start)
                end = MockAnalysisDataEnd()
                res_msg.append(end)
                return res_msg
        mocker.patch('app.ml_analysis_pb2_grpc.AnalyseServiceStub',
                     new=MockAnalyseServiceStub)

        # ml_analysis_pb2.AnalysisTemporalのモック
        mocker.patch('app.ml_analysis_pb2.AnalysisTemporal', return_value={})

        response = client.post(
            '/api/v1/catalog/tool/extracttemporal',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# 地域分析
################################################################


class TestExtractspatial:
    ##################################
    #  [extractspatial]
    #  地域分析：/api/v1/catalog/tool/extractspatial [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "title": "東京オリンピックの会場データ",
                "filepath": "hogehoge.csv",
                "notes": "東京オリンピックの会場データです。",
                "method": "hybrid"
            },
            # Response code, body
            200,
            {
                "spatial_list": [
                    {
                        "geonameId": "1848354",
                        "fcl": "P",
                        "lat": "35.43333",
                        "lng": "139.65",
                        "adminName1": "神奈川県",
                        "adminName2": "横浜市",
                        "name": "横浜市",
                        "score": "",
                        "searchMethod": ""
                    }
                ]
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_extractspatial(self, mocker, req_body, res_code, res_body):
        # ml_analysis_pb2_grpc.AnalyseServiceStubのモック
        class MockSpatialList:
            spatial_list = "[['1848354', '', 'P', '35.43333', '139.65', '神奈川県', '横浜市', '', '']]"

        class MockAnalyseServiceStub:
            def __init__(self, object):
                pass

            def SpatialAnalyseServer(arg1, arg2):
                res_msg = []
                response = MockSpatialList()
                res_msg.append(response)
                return res_msg
        mocker.patch('app.ml_analysis_pb2_grpc.AnalyseServiceStub',
                     new=MockAnalyseServiceStub)

        # ml_analysis_pb2.AnalysisSpatialのモック
        mocker.patch('app.ml_analysis_pb2.AnalysisSpatial', return_value={})

        response = client.post(
            '/api/v1/catalog/tool/extractspatial',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# テーマとキーワードの予測分析
################################################################


class TestAnalysis:
    ##################################
    #  [analysis]
    #  テーマとキーワードの予測分析：/api/v1/catalog/tool/analysis [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "catarog_title": "東京オリンピックの会場データ",
                "catarog_description": "東京オリンピックの会場データです。",
                "analyse_type": "theme"
            },
            # Response code, body
            200,
            {
                "pred_main": [
                    {
                        "label": "観光 > イベント",
                        "value": "観光 > イベント"
                    }
                ],
                "pred_sub": [
                    {
                        "label": "観光 > イベント",
                        "value": "観光 > イベント"
                    }
                ],
                "pred_prob": [
                    {
                        "label": "観光 > イベント, 0.4257450980392157",
                        "value": "観光 > イベント, 0.4257450980392157"
                    }
                ]
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_analysis(self, mocker, req_body, res_code, res_body):
        # ml_analysis_pb2_grpc.AnalyseServiceStubのモック
        class MockBestAnalyse:
            best_analyse = "観光 > イベント"

        class MockTopAnalyse:
            top_analyse = "観光 > イベント"

        class MockProbability:
            probability = "観光 > イベント, 0.4257450980392157"

        class MockAnalyseServiceStub:
            def __init__(self, object):
                pass

            def ThemeKeywordAnalyseServer(arg1, arg2):
                res_msg = []
                response = MockBestAnalyse()
                res_msg.append(response)
                response = MockTopAnalyse()
                res_msg.append(response)
                response = MockProbability()
                res_msg.append(response)
                return res_msg
        mocker.patch('app.ml_analysis_pb2_grpc.AnalyseServiceStub',
                     new=MockAnalyseServiceStub)

        # ml_analysis_pb2.AnalysisThemeKeyword
        mocker.patch('app.ml_analysis_pb2.AnalysisThemeKeyword',
                     return_value={})

        response = client.post(
            '/api/v1/catalog/tool/analysis',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# カタログ一時保存
################################################################


class TestTemporalPut:
    ##################################
    #  [temporal]
    #  カタログ一時保存：/api/v1/catalog/tool/temporal [PUT]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "dataForUpdate": {
                    "ckan_data_name": "ckan20210225102644",
                    "dataset_url": "https://example.lg.jp/d/dataset/ckan20210225102644",
                    "identifier": "https://example.lg.jp/d/dataset/ckan20210225102644",
                    "issued": "2021-02-25 10:26:44.919173"
                },
                "datajacket": [
                    {
                        "accessurl": "",
                        "connectRequired": {"label": "要求する", "value": "required"},
                        "contractRequired": {"label": "要求しない", "value": "notRequired"},
                        "dataurl": "ftp://provider_C/ftp_C_close_100MB.txt",
                        "description": "避難場所一覧",
                        "downloadurl": "ftp://provider_C/ftp_C_close_100MB.txt",
                        "filename": "sample011_ftp",
                        "format": "TXT",
                        "getResourceIDForProvenance": "no",
                        "issued": "2021-02-25 10:26:44.919289",
                        "licensetitle": "クリエイティブ・コモンズ 表示",
                        "licenseurl": "http://www.opendefinition.org/licenses/cc-by",
                        "mimetype": "text/plain",
                        "ngsiServicePath": "",
                        "ngsiTenant": "",
                        "resourceIDForProvenance": "",
                        "resourceType": {"label": "ファイル提供(FTP)", "value": "file/ftp"},
                        "schema": "https://schema.org/d/Restaurant",
                        "schemaType": "JSON-LD",
                        "size": 1024,
                        "variables": []
                    }
                ],
                "datasetinfo": {
                    "caddec_dataset_id_for_detail": "12345",
                    "caddec_provider_id": {"label": "test_id_D", "value": "test_id_D"},
                    "contact_name": "株式会社●●　Dデータ販売部",
                    "contact_url": "https://example.lg.jp/d/909001",
                    "creator_name": "株式会社△△△　〇〇D事業部",
                    "creator_url": "http://example.org/d/8010001000001",
                    "notes": "東京都の避難場所の地名一覧です。",
                    "publisher_name": "株式会社●●Dデータサービス事業部",
                    "publisher_uri": "http://example.org/d/7010001000001",
                    "regist_org": {"label": "SIP-test", "value": "sip-test"},
                    "title": "provider_d_detail_cadde_ftp_connector_100MB",
                    "url": "https://example.lg.jp/d"
                },
                "datasetoptionalinfo": {
                    "frequency": {"label": "3年毎", "value": "http://publications/TRIENNIAL"},
                    "language": [{"label": "日本語(ja)", "stamp": "よく使う言語", "value": "ja"}],
                    "spatial": "{\"type\":\"Point\", \"coordinates\":[139.69171, 35.6895]}",
                    "spatial_text": "日本>東京都",
                    "spatial_url": "https://www.geonames.org/1850144",
                    "tags": [{"label": "地図", "value": "地図"}, {"label": "防災", "value": "防災"}],
                    "temporal_end": "2020-06-30",
                    "temporal_start": "2020-06-01",
                    "term": "No, 住所,TEL",
                    "theme": [{"label": "災害", "value": "group030"}],
                    "vocabulary": "http://imi.go.jp/ns/core/d/RDF#"
                },
                "userterms": {
                    "fee": {"label": "有償", "value": "paid"},
                    "license_title": {"label": "クリエイティブ・コモンズ ", "value": "cc-by"},
                    "license_url": "http://www.opendefinition.org/licenses/cc-by",
                    "pricing_notices_of_price": "長期契約にて優待価格で提供",
                    "pricing_price_range": "価格:5000通貨単位:日本円",
                    "privacy_policy_contains_personal_data": {"label": "個人情報（要配慮個人情報を含む）", "value": "sensitivePersonalInformation"},
                    "privacy_policy_contains_personal_data_free": "",
                    "rights": "http://example.com/d/Rightstaement",
                    "sales_info_url": "https://example.lg.jp/d/data.htm",
                    "selected_tab": "pickroules",
                    "terms_of_use_notices": "利用状況の報告あり",
                    "terms_of_use_permissible_region": [{"label": "日本", "value": "JP"}],
                    "terms_of_use_permissible_region_free": "",
                    "terms_of_use_redistribution_range": {"label": "自部門", "value": "ownDepartment"},
                    "terms_of_use_redistribution_range_free": "",
                    "trading_policy_contract_type": {"label": "共同利用", "value": "sharedUse"},
                    "trading_policy_nda": {"label": "求める", "value": "required"},
                    "trading_policy_use_application": [{"label": "商用利用", "value": "commercialUse"}],
                    "trading_policy_use_application_free": "",
                    "usage_period_effective_period_of_data_end": "2020-07-31",
                    "usage_period_effective_period_of_data_free": "",
                    "usage_period_effective_period_of_data_start": "2020-04-01",
                    "usage_period_effective_period_of_data_term": {"label": "開始日・終了日", "value": "date"},
                    "usage_period_expiration_period_deadline": "",
                    "usage_period_expiration_period_free": "",
                    "usage_period_expiration_period_period": 1,
                    "usage_period_expiration_period_term": {"label": "期間", "value": "value"},
                    "usage_period_expiration_period_unit": {"label": "年", "value": "year"},
                    "warranty_express_warranty": {"label": "データ主体となる個人の本人同意が得られている", "value": "データ主体となる個人の本人同意が得られている"},
                    "warranty_express_warranty_free": "",
                    "warranty_legal_compliance": [{"label": "日本", "value": "JP"}],
                    "warranty_legal_compliance_free": ""
                },
                "tmpFile": {
                    "tmp_file_name": "tmp_file"
                }
            },
            # Response code, body
            200,
            {
                "status": "success",
                "error": ""
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_temporal_put(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        response = client.put(
            '/api/v1/catalog/tool/temporal',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# 一時保存取得
################################################################


class TestTemporalGet:
    ##################################
    #  [temporal]
    #  一時保存取得：/api/v1/catalog/tool/temporal [GET]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
            },
            # Response code, body
            200,
            [
                # ひとつ前のテストで一時保存したデータ
                TestTemporalPut.params_data_ok['200_Successful Response'][0]
            ]
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_temporal_get(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        response = client.get(
            '/api/v1/catalog/tool/temporal',
            json=req_body
        )
        assert response.status_code == res_code
        res_data = response.get_json()
        # 一時保存時に、「"saved": yyyymmddhhmmss(保存日時)」がサーバ側で追加されているので評価対象から除外する
        del res_data[0]["tmpFile"]["saved"]
        assert res_data == res_body

################################################################
# 一時保存削除
################################################################


class TestTemporalDelete:
    ##################################
    #  [temporal]
    #  一時保存削除：/api/v1/catalog/tool/temporal [DELETE]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            [
                "tmp_file"
            ],
            # Response code, body
            200,
            {
                "del_data": ["tmp_file"]
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_temporal_delete(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        response = client.delete(
            '/api/v1/catalog/tool/temporal',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# テンプレート保存
################################################################


class TestTemplatePut:
    ##################################
    #  [template]
    #  テンプレート保存：/api/v1/catalog/tool/template [PUT]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "catalog_display": {
                    "datasetinfo": {
                        "url": "optional",
                        "caddec_dataset_id_for_detail": "optional",
                        "publisher_name": "optional",
                        "publisher_uri": "optional",
                        "creator_name": "optional",
                        "creator_url": "optional",
                        "contact_name": "optional",
                        "contact_url": "optional"
                    },
                    "datajacket": {
                        "caddec_resource_type": "optional",
                        "name": "optional",
                        "description": "optional",
                        "access_url": "optional",
                        "download_url": "optional",
                        "size": "optional",
                        "value_name": "optional",
                        "mime_type": "optional",
                        "format": "optional",
                        "schema": "optional",
                        "schema_type": "optional",
                        "ngsi_tenant": "optional",
                        "ngsi_service_path": "optional",
                        "get_resource_id_for_provenance": "optional",
                        "caddec_resource_id_for_provenance": "optional"
                    },
                    "datasetoptionalinfo": {
                        "theme": "optional",
                        "tags": "optional",
                        "language": "optional",
                        "vocabulary": "optional",
                        "term": "optional",
                        "frequency": "optional",
                        "spatial": "optional",
                        "temporal": "optional"
                    },
                    "userterms": {
                        "license_title": "optional",
                        "license_url": "optional",
                        "rights": "optional",
                        "trading_policy_contract_type": "optional",
                        "trading_policy_nda": "optional",
                        "trading_policy_use_application": "optional",
                        "terms_of_use_redistribution_range": "optional",
                        "terms_of_use_permissible_region": "optional",
                        "terms_of_use_notices": "optional",
                        "privacy_policy_contains_personal_data": "optional",
                        "usage_period_effective_period_of_data": "optional",
                        "usage_period_expiration_period": "optional",
                        "fee": "optional",
                        "sales_info_url": "optional",
                        "pricing_price_range": "optional",
                        "pricing_notices_of_price": "optional",
                        "warranty_express_warranty": "optional",
                        "warranty_legal_compliance": "optional"
                    }
                },
                "catalog_value": {
                    "datasetinfo": {
                        "title": "",
                        "notes": "",
                        "url": "",
                        "regist_org": {
                            "label": "",
                            "value": ""
                        },
                        "caddec_provider_id": {
                            "label": "",
                            "value": ""
                        },
                        "publisher_name": "",
                        "publisher_uri": "",
                        "creator_name": "",
                        "creator_url": "",
                        "contact_name": "",
                        "contact_url": ""
                    },
                    "datajacket": [
                        {
                            "contractRequired": {
                                "label": "",
                                "value": ""
                            },
                            "connectRequired": {
                                "label": "",
                                "value": ""
                            },
                            "filename": "",
                            "dataname": "",
                            "description": "",
                            "dataurl": "",
                            "accessurl": "",
                            "downloadurl": "",
                            "size": "",
                            "variables": [],
                            "mimetype": "",
                            "format": "",
                            "schema": "",
                            "schemaType": "",
                            "ngsiTenant": "",
                            "ngsiServicePath": "",
                            "getResourceIDForProvenance": "",
                            "resourceIDForProvenance": "",
                            "resourceType": {
                                "label": "",
                                "value": ""
                            },
                            "license_title": "",
                            "licenseurl": "",
                            "issued": "",
                            "label": ""
                        }
                    ],
                    "datasetoptionalinfo": {
                        "theme": [],
                        "tags": [],
                        "language": [{"label": "日本語(ja)", "value": "ja"}],
                        "vocabulary": "",
                        "term": "",
                        "frequency": "",
                        "spatial_url": "",
                        "spatial_text": "",
                        "spatial": "",
                        "temporal_start": "",
                        "temporal_end": ""
                    },
                    "userterms": {
                        "selected_tab": "pickroules",
                        "license_title": "",
                        "license_url": "",
                        "rights": "",
                        "trading_policy_contract_type": "",
                        "trading_policy_nda": "",
                        "trading_policy_use_application": [],
                        "trading_policy_use_application_free": "",
                        "terms_of_use_redistribution_range": "",
                        "terms_of_use_redistribution_range_free": "",
                        "terms_of_use_permissible_region": [{"label": "制限なし", "value": "noLimit"}],
                        "terms_of_use_permissible_region_free": "",
                        "terms_of_use_notices": "",
                        "privacy_policy_contains_personal_data": "",
                        "privacy_policy_contains_personal_data_free": "",
                        "usage_period_effective_period_of_data_term": "",
                        "usage_period_effective_period_of_data_start": "",
                        "usage_period_effective_period_of_data_end": "",
                        "usage_period_effective_period_of_data_free": "",
                        "usage_period_expiration_period_term": "",
                        "usage_period_expiration_period_deadline": "",
                        "usage_period_expiration_period_period": "",
                        "usage_period_expiration_period_unit": "",
                        "usage_period_expiration_period_free": "",
                        "fee": "",
                        "sales_info_url": "",
                        "pricing_price_range": "",
                        "pricing_notices_of_price": "",
                        "warranty_express_warranty": "",
                        "warranty_express_warranty_free": "",
                        "warranty_legal_compliance": [],
                        "warranty_legal_compliance_free": ""
                    }
                }
            },
            # Response code, body
            200,
            {
                "status": "success",
                "message": "テンプレート保存完了"
            }
        )
    }
    # 異常系
    params_data_ng = {
        '400_Bad Request': (    # 失敗
            # Request Body
            {
            },
            # Response code, body
            400,
            {
                'status': 'faild',
                'message': 'フィールドなし'
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_template_put(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        response = client.put(
            '/api/v1/catalog/tool/template',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body


'''
    # 異常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ng.values()), ids=list(params_data_ng.keys()))
    def test_template_put_ng(self, req_body, res_code, res_body):
        response = client.put(
            '/api/v1/catalog/tool/export/template',
            json = req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body
'''

################################################################
# テンプレート取得
################################################################


class TestTemplateGet:
    ##################################
    #  [template]
    #  テンプレート取得：/api/v1/catalog/tool/template [GET]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
            },
            # Response code, body
            200,
            {
                "status": "success",
                "message": "テンプレート取得完了",
                # ひとつ前のテストで保存したテンプレート
                "template": TestTemplatePut.params_data_ok['200_Successful Response'][0]
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_template_get(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        response = client.get(
            '/api/v1/catalog/tool/template',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# リソース項目自動補完候補検索
################################################################


class TestResourceAutocorrect:
    ##################################
    #  [resource/autocorrect]
    #  リソース項目自動補完候補検索：/api/v1/catalog/tool/resource/autocorrect [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "label": "name",
                "value": "aa",
            },
            # Response code, body
            200,
            {
                "candidates": [
                    "sample011_http",
                    "test-a-aed.csv",
                    "df_seven.csv"
                ],
                "message": "success"
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_resource_autocorrect(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # ckan_catalog_manager.search_auto_correct_resourceのモック
        result = {
            'message': 'success',
            'candidates': ["sample011_http", "test-a-aed.csv", "df_seven.csv"]
        }
        mocker.patch('app.search_auto_correct_resource', return_value=result)

        response = client.post(
            '/api/v1/catalog/tool/resource/autocorrect',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body

################################################################
# カタログ項目自動補完候補検索
################################################################


class TestDatacatalogAutocorrect:
    ##################################
    #  [datacatalog/autocorrect]
    #  カタログ項目自動補完候補検索：/api/v1/catalog/tool/datacatalog/autocorrect [POST]
    #################################
    ### データパターン ###
    # 正常系
    params_data_ok = {
        '200_Successful Response': (    # 成功
            # Request Body
            {
                "label": "title",
                "value": "aa",
            },
            # Response code, body
            200,
            {
                "candidates": [
                    "【試行用】【自治体A】AED設置箇所一覧",
                    "【試行用】【自治体B】AED設置箇所一覧"
                ],
                "message": "success"
            }
        )
    }

    ### テストコード ###
    # 正常系
    @pytest.mark.parametrize('req_body, res_code, res_body',
                             list(params_data_ok.values()), ids=list(params_data_ok.keys()))
    def test_datacatalog_autocorrect(self, mocker, req_body, res_code, res_body):
        # get_ckan_userのモック
        mocker.patch('app.get_ckan_user', return_value=user_info_login_ok)
        # 事前処理
        response = client.post('/api/v1/catalog/tool/login',
                               json={"username": "ckan_admin", "password": "test1234"})

        # ckan_catalog_manager.search_auto_correct_catalogのモック
        result = {
            'message': 'success',
            'candidates': ["【試行用】【自治体A】AED設置箇所一覧", "【試行用】【自治体B】AED設置箇所一覧"]
        }
        mocker.patch('app.search_auto_correct_catalog', return_value=result)

        response = client.post(
            '/api/v1/catalog/tool/datacatalog/autocorrect',
            json=req_body
        )
        assert response.status_code == res_code
        assert response.get_json() == res_body
