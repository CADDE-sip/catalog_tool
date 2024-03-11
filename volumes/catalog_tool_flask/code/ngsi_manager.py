import json
import os
import traceback
import requests
import datetime
import mimetypes

from data_uploader import read_file
from catalogtool_exception import CatalogToolException


class NgsiData:

    # NGSI連携コンテナAPI
    __DATA_URL = '/api/v1/ngsi/entities/data'
    __ORIGINAL_DATA_URL = '/api/v1/ngsi/entities/originaldata'
    __DATAMODEL_URL = '/api/v1/ngsi/entities/datamodel'

    # ファイル保存先パス
    __SAVE_DIR_PATH = 'data/'

    def __init__(self, app, ngsi_server):
        self.__app = app
        self.__ngsi_server = str(ngsi_server)

    def get_ngsi_data(self, data):
        self.__app.logger.warning(data)
        res_data = {
            'status': '',
            'message': '',
            'dataname': '',
            'format': '',
            'mime_type': '',
            'file_size': '',
            'data_list': []
        }

        headers = {
            'X-CATALOGTOOL-NGSI-URL': '',
            'Fiware-Service': '',
            'Fiware-ServicePath': ''
        }

        headers['X-CATALOGTOOL-NGSI-URL'] = data['url']
        headers['Fiware-Service'] = data['tenant']
        headers['Fiware-ServicePath'] = data['service_path']
        self.__app.logger.warning(headers)

        # NGSIデータ取得
        try:
            # NGSIデータ種別取得
            querys = data['url'].split('?')[1]
            query_list = querys.split('&')
            entity_type = ''
            for q in query_list:
                if q.startswith('type='):
                    entity_type = q
            if not entity_type:
                raise CatalogToolException('ngsi_RequestError', 400)

            target_url = 'http://' + self.__ngsi_server + \
                self.__DATA_URL + '?' + entity_type
            response = requests.get(target_url, headers=headers)

        except Exception:
            self.__app.logger.warning(traceback.format_exc())
            raise CatalogToolException('ngsi_ServerException', 500)

        # NGSIデータ取得失敗
        if response.status_code == 400:
            result = json.loads(response.content.decode())
            self.__app.logger.error(result['detail'])
            raise CatalogToolException('ngsi_RequestError', 400)
        if response.status_code == 408:
            result = json.loads(response.content.decode())
            self.__app.logger.error(result['detail'])
            raise CatalogToolException('ngsi_TimeoutError', 408)
        if response.status_code >= 300:
            result = json.loads(response.content.decode())
            self.__app.logger.error(result['detail'])
            raise CatalogToolException('ngsi_ServerError', 500)

        # NGSIデータ取得成功
        self.__app.logger.warning('NGSIデータ取得成功')

        # NGSIデータ情報取得
        filename = data['url'].split('/')[2]
        current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        dataname = current_time + '_' + filename
        mime_type = 'json' if response.headers['Content-Type'] == 'application/json' else ''
        file_size = response.headers['Content-Length']

        # NGSIデータ読み込み用にNGSIデータファイル作成
        self.__app.logger.warning('NGSIデータ保存')
        try:
            data = response.content.decode()
            with open(self.__SAVE_DIR_PATH + dataname, 'w') as f:
                f.write(data)
        except Exception:
            self.__app.logger.error(traceback.format_exc())
            raise CatalogToolException('ngsi_FileSaveError', 500)

        # NGSI原本データ取得
        try:
            target_url = 'http://' + self.__ngsi_server + \
                self.__ORIGINAL_DATA_URL + '?' + entity_type
            response = requests.get(target_url, headers=headers)

        except Exception:
            self.__app.logger.error(traceback.format_exc())
            raise CatalogToolException('ngsi_original_ServerException', 500)

        # NGSI原本データ取得失敗
        if response.status_code == 400:
            result = json.loads(response.content.decode())
            self.__app.logger.error(result['detail'])
            raise CatalogToolException('ngsi_original_RequestError', 400)
        if response.status_code == 408:
            result = json.loads(response.content.decode())
            self.__app.logger.error(result['detail'])
            raise CatalogToolException('ngsi_original_TimeoutError', 408)
        if response.status_code >= 300:
            result = json.loads(response.content.decode())
            self.__app.logger.error(result['detail'])
            raise CatalogToolException('ngsi_original_ServerError', 500)

        # NGSI原本データ取得成功
        self.__app.logger.warning('NGSI原本データ取得成功')

        # NGSI原本データファイル保存
        self.__app.logger.warning('NGSI原本データ保存')
        try:
            data = response.content.decode()
            with open(self.__SAVE_DIR_PATH + dataname, 'w') as f:
                f.write(data)
        except Exception:
            self.__app.logger.error(traceback.format_exc())
            raise CatalogToolException('ngsi_original_FileSaveError', 500)

        res_data['status'] = 'success'
        res_data['message'] = ''
        # NGSIデータ情報をレスポンスに設定
        res_data['dataname'] = dataname
        res_data['mime_type'] = mime_type
        res_data['file_size'] = file_size

        return res_data

    def get_ngsi_data_model(self, data):
        self.__app.logger.warning(data)
        res_data_model = {
            'status': '',
            'message': '',
            'data_model': []
        }

        headers = {
            'X-CATALOGTOOL-NGSI-URL': '',
            'Fiware-Service': '',
            'Fiware-ServicePath': ''
        }

        headers['X-CATALOGTOOL-NGSI-URL'] = data['url']
        headers['Fiware-Service'] = data['tenant']
        headers['Fiware-ServicePath'] = data['service_path']

        try:
            target_url = 'http://' + self.__ngsi_server + \
                self.__DATAMODEL_URL + '?type=' + str(data['entity_type'])
            response = requests.get(target_url, headers=headers)
            self.__app.logger.warning(response)

        except Exception:
            self.__app.logger.error(traceback.format_exc())
            raise CatalogToolException(
                'get_ngsi_data_model_ServerException', 500)

        if response.status_code == 400:
            result = json.loads(response.content.decode())
            self.__app.logger.error(result['detail'])
            raise CatalogToolException('get_ngsi_data_model_RequestError', 400)
        if response.status_code == 408:
            result = json.loads(response.content.decode())
            self.__app.logger.error(result['detail'])
            raise CatalogToolException('get_ngsi_data_model_TimeoutError', 408)
        if response.status_code >= 300:
            result = json.loads(response.content.decode())
            self.__app.logger.error(result['detail'])
            raise CatalogToolException('get_ngsi_data_model_ServerError', 500)

        result = json.loads(response.content.decode())
        for model_key, model_value in result.items():
            row = {}
            row['attribute'] = model_key
            row['dataType'] = model_value['type'] if 'type' in model_value else ''
            row['example'] = model_value['value'] if 'value' in model_value else ''
            # descriptionはAPIから取得しない値
            row['description'] = ''
            row['metadata'] = []
            for meta_key, meta_value in model_value['metadata'].items():
                row['metadata'].append({
                    'metadataName': meta_key,
                    'dataType': meta_value['type'] if 'type' in meta_value else '',
                    'example': meta_value['value'] if 'value' in meta_value else '',
                    # descriptionはAPIから取得しない値
                    'description': ''
                })
            res_data_model['data_model'].append(row)

        res_data_model['status'] = 200
        res_data_model['message'] = 'success'

        return res_data_model
