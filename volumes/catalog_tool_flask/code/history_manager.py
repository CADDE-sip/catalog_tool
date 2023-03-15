# -*- coding: utf-8 -*-
import traceback
import json
import requests
import mimetypes
import base64
import urllib.parse

from catalogtool_exception import CatalogToolException

API_EVENTWITHHASH = 'eventwithhash'
API_SEARCHEVENTS = 'searchevents'
API_LINEAGE = 'lineage'

LINEAGE_DIRECTION = 'BOTH'
LINEAGE_DEPTH = '-1'

CDL_DATAMODEL_VER = '2.0'
CDL_EVENT_TYPE_CREATE = 'Create'
CDL_EVENT_TYPE_PUBLISH = 'Publish'
CDL_EVENT_TYPE_RECEIVED = 'Received'
CDL_TAG_SCOPE = 'global'
BOUNDARY_STRING = '3bc42ba6256f786f'

# 拡張子取得
def allowed_file(file_name):
    return file_name.rsplit('.', 1)[1].lower()


# 新規来歴登録
def regist_new_record(app, history_url, cdluri, file_name, publisher_id, token):

    app.logger.warning('新規来歴登録開始')
    # 新規来歴登録API URL設定
    url = str(history_url) + API_EVENTWITHHASH

    # ヘッダ設定
    headers = {
        'Accept': 'application/json',
        'Authorization': token
    }

    # ボディ設定
    body = {
        'cdldatamodelversion': CDL_DATAMODEL_VER,
        'cdleventtype': CDL_EVENT_TYPE_CREATE,
        'cdltagscope': CDL_TAG_SCOPE,
        'dataprovider': publisher_id,
        'cdleventid': '',
        'cdlpreviousevents': [],
        'cdldatatags': [{
            'cdluri': cdluri
        }]
    }
    request_body = json.dumps(body, indent=2).encode()

    # ファイル読み込み
    bytes_data = open(file_name, 'rb').read()
    content_data = base64.b64encode(bytes_data)

    # メディアタイプ取得
    ext = allowed_file(file_name)
    try:
        mimetype = mimetypes.types_map[f'.{ext}']
    except:
        mimetype = 'application/octet-stream'

    # ファイルアップロードリクエスト設定
    up_file = {
        'request': ('', request_body, 'application/json'),
        'upfile': (file_name, base64.b64decode(content_data), mimetype)
    }

    try:
        response = requests.post(url,headers=headers,files=up_file)
        app.logger.warning(response.status_code)
        app.logger.warning(response.content.decode())
        resource_id_for_provenance = json.loads(response.content.decode())['cdleventid']
        mes = 'success'

    except Exception:
        app.logger.warning(traceback.format_exc())
        resource_id_for_provenance = ''
        mes = 'get resource error'

    return resource_id_for_provenance, str(mes)


# 公開履歴登録
def regist_history_record(app, history_url, cdluri, file_name, publisher_id, previous_event_id, token):

    app.logger.warning('公開履歴登録開始')
    # 公開履歴登録API URL設定
    url = str(history_url) + API_EVENTWITHHASH

    # ヘッダ設定
    headers = {
        'Accept': 'application/json',
        'Authorization': token
    }

    # jsonデータ設定
    body = {
        'cdldatamodelversion': CDL_DATAMODEL_VER,
        'cdleventtype': CDL_EVENT_TYPE_PUBLISH,
        'cdltagscope': CDL_TAG_SCOPE,
        'dataprovider': publisher_id,
        'cdleventid': '',
        'cdlpreviousevents': [previous_event_id],
        'cdldatatags': [{
            'cdluri': cdluri
        }]
    }
    request_body = json.dumps(body, indent=2).encode()

    # ファイル読み込み
    bytes_data = open(file_name, 'rb').read()
    content_data = base64.b64encode(bytes_data)

    # メディアタイプ取得
    ext = allowed_file(file_name)
    try:
        mimetype = mimetypes.types_map[f'.{ext}']
    except:
        mimetype = 'application/octet-stream'

    # ファイルアップロードリクエスト設定
    up_file = {
        'request': ('', request_body, 'application/json'),
        'upfile': (file_name, base64.b64decode(content_data), mimetype)
    }

    try:
        response = requests.post(url,headers=headers,files=up_file)
        app.logger.warning(response.status_code)
        app.logger.warning(response.content.decode())
        resource_id_for_provenance = json.loads(response.content.decode())['cdleventid']
        mes = 'success'

    except Exception:
        app.logger.warning(traceback.format_exc())
        resource_id_for_provenance = ''
        mes = 'get resource error'

    return resource_id_for_provenance, str(mes)


# 前段イベント識別子検索
def search_history(app, search_key, history_url, token):

    app.logger.warning('前段イベント識別子検索開始')
    res = {
        'status': '',
        'message': '',
        'result': []
    }

    resource_url = search_key['resource_url']
    provider_id = search_key['provider_id']
    user_id = search_key['user_id']

    # 来歴検索API URL設定
    searchevents_url = str(history_url) + API_SEARCHEVENTS

    # ヘッダ設定
    headers = {
        'Accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': token
    }

    if resource_url:
        # リソースURLが指定されている場合、cdluriを指定しCreatedの来歴履歴を検索する
        # 来歴検索の結果から得た交換実績記録用リソースIDでさらに来歴確認を行う

        # 来歴にはエンコードURLが登録されているためエンコーディングする
        resource_url = urllib.parse.quote(resource_url)

        # リソースURLが指定されている場合、cdluriを指定しCreatedの来歴履歴を検索する
        # ボディ設定（cdluriを指定するとcdleventtypeがCreateの結果のみ取得する）
        payload = {
            'selector': {
                'cdldatamodelversion': CDL_DATAMODEL_VER,
                'dataprovider': provider_id,
                'cdldatatags': {
                    '$elemMatch': {
                        'cdluri': {
                            '$regex': resource_url
                        }
                    }
                }
            }
        }

        try:
            response = requests.post(searchevents_url, headers=headers, data=json.dumps(payload))
            app.logger.warning(response.status_code)
            app.logger.warning(response.content.decode())
            search_response = json.loads(response.content.decode())
            if search_response == []:
                res['status'] = 'success'
                res['message'] = '検索結果0件'
                return res
       
        except Exception:
            app.logger.error(traceback.format_exc())
            app.logger.warning('来歴管理サーバエラー')
            raise CatalogToolException('search_history_Exception', 500)

        lineage_result = []
        for record in search_response:            
            # 来歴確認API URL設定
            lineage_url = str(history_url) + API_LINEAGE + '/' + record['cdleventid'] + '?direction=' + LINEAGE_DIRECTION + '&depth=' + LINEAGE_DEPTH

            try:
                response = requests.get(lineage_url, headers=headers)
                app.logger.warning(response.status_code)
                app.logger.warning(response.content.decode())
                lineage_response = json.loads(response.content.decode())
                lineage_result.extend(lineage_response)                   
 
            except Exception:
                app.logger.error(traceback.format_exc())
                app.logger.warning('来歴管理サーバエラー')
                raise CatalogToolException('search_history_Exception', 500)

        if lineage_result == []:
            res['status'] = 'success'
            res['message'] = '検索結果0件'
            return res

        received_event_list = []
        for record in lineage_result:
            if not record['cdleventtype'] == CDL_EVENT_TYPE_RECEIVED:
                # イベントタイプが'Received'のみを抽出
                continue
            if not record['dataprovider'] == provider_id:
                # 提供者IDの一致を確認
                continue
            if user_id and not record['datauser'] == user_id:
                # CADDEユーザIDも指定されている場合は、CADDEユーザIDの一致を確認
                continue
            received_event_list.append(record)

        if lineage_result == []:
            res['status'] = 'success'
            res['message'] = '検索結果0件'
            return res

    else:
        # リソースURLが未指定の場合は、イベントタイプにReceivedを指定して来歴検索をする

        # ボディ設定
        if user_id:
            # CADDEユーザIDの指定あり
            payload = {
                'selector': {
                    'cdldatamodelversion': CDL_DATAMODEL_VER,
                    'cdleventtype': CDL_EVENT_TYPE_RECEIVED,
                    'dataprovider': provider_id,
                    'datauser': user_id
                }
            }

        else:
            payload = {
                'selector': {
                    'cdldatamodelversion': CDL_DATAMODEL_VER,
                    'cdleventtype': CDL_EVENT_TYPE_RECEIVED,
                    'dataprovider': provider_id,
                }
            }

        received_event_list = []
        try:
            response = requests.post(searchevents_url, headers=headers, data=json.dumps(payload))
            app.logger.warning(response.status_code)
            app.logger.warning(response.content.decode())
            received_event_list = json.loads(response.content.decode())
            if received_event_list == []:
                res['status'] = 'success'
                res['message'] = '検索結果0件'
                return res

        except Exception:
            app.logger.error(traceback.format_exc())
            app.logger.warning('来歴管理サーバエラー')
            raise CatalogToolException('search_history_Exception', 500)

    previous_event_id_list = []
    for val in received_event_list:
        event = {}
        event['event_id'] = val['cdleventid']
        event['timestamp'] = val['cdltimestamp']
        event['provider_id'] = val['dataprovider']
        event['user_id'] = val['datauser']
        previous_event_id_list.append(event)
    res['status'] = 'success'
    res['message'] = '検索結果あり'
    res['result'] = previous_event_id_list

    return res

