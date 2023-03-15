# -*- coding: utf-8 -*-
import requests
from logging import getLogger
from io import BytesIO
import ftplib
import ssl
import urllib.request
import os
import traceback
from werkzeug.utils import secure_filename
from chardet.universaldetector import UniversalDetector

from requests.exceptions import Timeout
from timeout_decorator import timeout
from timeout_decorator import TimeoutError
import json
import pandas as pd
import mimetypes
import datetime
import csv

from catalogtool_exception import CatalogToolException

logger = getLogger(__name__)

__CONFIG_KEY_FILE_URL = 'url'
__CONFIG_KEY_FILE_ID = 'id'
__CONFIG_KEY_FILE_PASS = 'pass'
__CONFIG_KEY_FILE_PROXY = 'proxy'

__URL_SPLIT_CHR = '/'
__ACCESS_POINT_SPLIT_CHR = ':'
__FTP_DEFAULT_PORT = 21

__HTTP_CONNECT_TIMEOUT = 10
__HTTP_READ_TIMEOUT = 60
__FTP_TIMEOUT = 10


class FTP_IgnoreHost(ftplib.FTP):
    def makepasv(self):
        _, port = super().makepasv()
        return self.host, port


# 現在時刻取得(ローカル時刻)
def get_datetime():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d%H%M%S%f')


# ファイル拡張子取得
def allowed_file(filename):
    return filename.rsplit('.', 1)[1].lower()


# リソースURLのidとpass取得
def __get_auth(url: list, auth_list: list):
    id = ''
    pwd = ''
    for i in auth_list:
        if url.startswith(i[__CONFIG_KEY_FILE_URL]):
            if __CONFIG_KEY_FILE_ID in i:
                id = i[__CONFIG_KEY_FILE_ID]
            if __CONFIG_KEY_FILE_PASS in i:
                pwd = i[__CONFIG_KEY_FILE_PASS]

    return id, pwd


# ファイル読み込み
def read_file(app, SAVE_DIR_PATH, dataname: str, fileformat: str, file_code: str = 'utf-8'):

    if fileformat == 'csv':
        app.logger.warning('CSV')
        app.logger.warning(SAVE_DIR_PATH + dataname)
        try:
            with open(SAVE_DIR_PATH + dataname, 'r', encoding=file_code) as f:
                reader = csv.reader(f)

                if reader is None:
                    data_list = 'not variable'
                    app.logger.warning('no variable')
                else:
                    for rf in reader:
                        data_list = rf
                        app.logger.warning(data_list)
                        break

        except Exception:
            app.logger.error('CSVファイル読み込みエラー')
            app.logger.error(traceback.format_exc())
            raise CatalogToolException('read_file_CSVFileReadError', 500)

    elif fileformat == 'xlsx' or fileformat == 'xls':
        app.logger.warning('EXEL')
        app.logger.warning(SAVE_DIR_PATH + dataname)
        # 全てのシートを読み込む
        try:
            reader = pd.read_excel(SAVE_DIR_PATH + dataname, sheet_name=None)

            data_list = []
            data_list = [list(reader[sheet].head(1)) for sheet in reader]
            data_list = [line for inner in data_list for line in inner]
            app.logger.warning(data_list)

        except Exception:
            app.logger.error('XLSX,XLSファイル読み込みエラー')
            app.logger.error(traceback.format_exc())
            raise CatalogToolException('read_file_ExcelFileReadError', 500)

    else:
        app.logger.warning('その他のファイル形式')
        data_list = ''

    if data_list:
        data_list = json.dumps(data_list)

    return data_list


# HTTPファイル取得・保存
def http_get(
        app,
        SAVE_DIR_PATH,
        target_url: str,
        auth_list: list,
        headers: dict = None):
    """
    Args:
            app: flaskのアプリケーションオブジェクト
            target_url str : 接続するURL
            auth_list : ベーシック認証時のurlに対するidとpassのリスト
            headers : 設定するheader {ヘッダー名:パラメータ}

    Returns:
        response : get通信のレスポンス
    """
    data_list = []
    mime_type = ''
    file_size = ''
    error_label = ''
    dataname = ''
    fileformat = ''

    response_data = {
        'error_label': '',
        'data_list': [],
        'mime_type': '',
        'file_size': '',
        'dataname': '',
        'format': ''
    }

    if not headers:
        headers = {}

    headers['Cache-Control'] = 'no-cache'

    auth_id, auth_pass = __get_auth(target_url, auth_list)
    auth = (auth_id, auth_pass)

    for i in auth_list:
        if target_url.startswith(i[__CONFIG_KEY_FILE_URL]):
            if not i[__CONFIG_KEY_FILE_PROXY]:
                os.environ['NO_PROXY'] = i[__CONFIG_KEY_FILE_URL]

    try:
        response = requests.get(
            target_url,
            headers=headers,
            timeout=(
                __HTTP_CONNECT_TIMEOUT,
                __HTTP_READ_TIMEOUT),
            auth=auth)

    except Timeout:
        app.logger.error('HTTPリソースファイル取得タイムアウト')
        raise CatalogToolException('http_get_Timeout', 408)

    except Exception:
        app.logger.error('HTTPリソースファイル取得例外')
        app.logger.error(traceback.format_exc())
        raise CatalogToolException('http_get_Exception', 500)

    if response.status_code == 401:
        app.logger.error('HTTPリソースファイル取得エラー(401)')
        raise CatalogToolException('http_get_NotAuthorized', 401)
    elif response.status_code == 404:
        app.logger.error('HTTPリソースファイル取得エラー(404)')
        raise CatalogToolException('http_get_NotFound', 404)
    elif response.status_code == 408:
        app.logger.error('HTTPリソースファイル取得エラー(408)')
        raise CatalogToolException('http_get_Timeout', 408)
    elif response.status_code >= 300:
        app.logger.error('HTTPリソースファイル取得エラー')
        app.logger.error(response.status_code)
        raise CatalogToolException('http_get_HttpError', 500)

    filename = target_url.split('/')[-1]
    fileformat = allowed_file(filename)
    current_time = get_datetime()
    dataname = current_time + '_' + filename
    mime_type = allowed_file(filename)
    file_size = response.headers['Content-length']

    # ファイル保存
    try:
        with open(SAVE_DIR_PATH + dataname, 'wb') as f:
            f.write(response.content)
    except OSError:
        app.logger.error('HTTPリソースファイル保存エラー')
        raise CatalogToolException('http_get_FileSaveError', 500)

    # ファイル読み込み
    data_list = read_file(app, SAVE_DIR_PATH, dataname, fileformat)

    response_data['error_label'] = error_label
    response_data['data_list'] = data_list
    response_data['mime_type'] = mime_type
    response_data['file_size'] = file_size
    response_data['dataname'] = dataname
    response_data['format'] = fileformat
    app.logger.warning(response_data)

    return response_data

# リソースURL解析


def __url_analysis(url: str) -> dict:
    """
    Args:
        url str : 解析するURL

    Returns:
        dict :解析後データ {'access_point':(接続先), 'port_no':(ポート番号) 'directory':(ディレクトリ), 'file_name':(ファイル名)}
    """
    split_url = url.split(__URL_SPLIT_CHR)
    domain = split_url[2]
    split_domain = domain.split(__ACCESS_POINT_SPLIT_CHR)
    access_point = split_domain[0]
    port_no = __FTP_DEFAULT_PORT

    if len(split_domain) == 2:
        port_no = int(split_domain[1])

    directory = ''

    if len(split_url) > 3:
        directory_last_element = len(split_url) - 1
        for element in split_url[3:directory_last_element]:
            directory = directory + element + __URL_SPLIT_CHR

    file_name = split_url[-1]

    return {
        'access_point': access_point,
        'port_no': port_no,
        'directory': directory,
        'file_name': file_name}


# FTPファイル取得・保存
@timeout(60, use_signals=False)
def ftp_get(
        app,
        SAVE_DIR_PATH,
        target_url: str,
        auth_list: list):

    data_list = []
    mime_type = ''
    file_size = ''
    error_label = ''
    dataname = ''
    fileformat = ''

    response_data = {
        'error_label': '',
        'data_list': [],
        'mime_type': '',
        'file_size': '',
        'dataname': '',
        'format': ''
    }

    ftp_id, ftp_pass = __get_auth(target_url, auth_list)

    parsed_resource_url = __url_analysis(target_url)
    app.logger.warning(parsed_resource_url)

    current_time = get_datetime()
    filename = parsed_resource_url['file_name']
    dataname = current_time + '_' + filename

    try:
        with FTP_IgnoreHost() as ftp:
            ftp.connect(
                parsed_resource_url['access_point'],
                parsed_resource_url['port_no'],
            )
            ftp.login(user=ftp_id, passwd=ftp_pass)
            if len(parsed_resource_url['directory']) > 0:
                ftp.cwd(parsed_resource_url['directory'])

            # ファイルを取得して保存
            with open(SAVE_DIR_PATH + dataname, 'wb') as f:
                ftp.retrbinary(
                    'RETR '
                    + filename,
                    f.write)

    except OSError:
        app.logger.error('FTPリソースファイル保存エラー')
        app.logger.error(traceback.format_exc())
        raise CatalogToolException('ftp_get_FileSaveError', 500)
    except TimeoutError:
        app.logger.error('FTPリソースファイル取得タイムアウト')
        app.logger.error(traceback.format_exc())
        raise CatalogToolException('ftp_get_Timeout', 408)
    except Exception as e:
        error_message = str(e)
        error_code = error_message.split(' ')[0]
        if error_code == '530':
            app.logger.error(traceback.format_exc())
            app.logger.error('FTPリソースファイル取得エラー(530)')
            raise CatalogToolException('ftp_get_NotAuthorized', 401)
        elif error_code == '550':
            app.logger.error(traceback.format_exc())
            app.logger.error('FTPリソースファイル取得エラー(550)')
            raise CatalogToolException('ftp_get_NotFound', 404)
        elif error_message == 'timed out':
            app.logger.error(traceback.format_exc())
            app.logger.error('FTPリソースファイル取得エラー(408)')
            raise CatalogToolException('ftp_get_Timeout', 408)
        else:
            app.logger.error('FTPリソースファイル取得エラー')
            app.logger.error(traceback.format_exc())
            raise CatalogToolException('ftp_get_FTPError', 500)

    fileformat = allowed_file(filename)
    mime_type = allowed_file(filename)

    data_list = read_file(app, SAVE_DIR_PATH, dataname, fileformat)

    response_data['error_label'] = error_label
    response_data['data_list'] = data_list
    response_data['mime_type'] = mime_type
    response_data['file_size'] = file_size
    response_data['dataname'] = dataname
    response_data['format'] = fileformat
    app.logger.warning(response_data)

    return response_data


# URLデータ保存
def url_upload(app, SAVE_DIR_PATH, file):
    data_list = []
    mime_type = ''
    dataname = ''
    fileformat = ''

    response_json = {
        'data_list': data_list,
        'mimetype': mime_type,
        'format': fileformat,
        'dataname': dataname
    }

    fileformat = allowed_file(file.filename)
    current_time = get_datetime()
    dataname = current_time + '_' + secure_filename(file.filename)
    mime_type = allowed_file(file.filename)

    try:
        # ファイル保存
        file.save(os.path.join(SAVE_DIR_PATH, dataname))

        # ファイルの文字コード判定
        file_code = ''
        detector = UniversalDetector()
        with open(SAVE_DIR_PATH + dataname, 'rb') as f:
            detector.reset()
            for line in f.readlines():
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
            file_code = detector.result['encoding']
            if file_code is None:
                app.logger.warning('### 不明の文字コード ###')
                file_code = 'utf-8'
    except OSError:
        app.logger.error('アップロードファイル保存エラー')
        raise CatalogToolException('url_upload_FileSaveError', 500)

    data_list = read_file(app, SAVE_DIR_PATH, dataname, fileformat, file_code)

    response_json['data_list'] = data_list
    response_json['mimetype'] = mime_type
    response_json['format'] = fileformat
    response_json['dataname'] = dataname
    app.logger.warning(response_json)

    return response_json
