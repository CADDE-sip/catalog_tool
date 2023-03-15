# CKAN のデータセットを管理する
# CKAN の操作をCLIで行う
import requests
import os
import json
import tarfile
import glob
import subprocess
import traceback
import threading
import datetime
from queue import Queue

from ckanapi import RemoteCKAN, NotAuthorized

from catalogtool_exception import CatalogToolException

IMPORT_EXPORT_DIR = './data/imexport/'
IMPORT_EVENT = 'import'
EXPORT_EVENT = 'export'
IMPORT_DIR = './data/import/'
EXPORT_DIR = './data/export/'


class GZFILETypeError(Exception):
    """ GZ形式のファイルでない時の例外エラー"""
    pass


class CkanDataset:
    """Ckan datasetを操作する処理

      Arguments:
        - url: (string), 処理する対象のCKAN URL
        - apikry: (string), 処理するユーザのAPIKEY(UUID)
        - process_num: (integer)(optional), 処理するプロセス数(Default: 3)
                       インポート処理のみ有効。
    """

    def __init__(self, app, process_num=3):
        self.__app = app
        self.__process_num = int(process_num)
        self.res_message = {'status': 'faild', 'message': ''}
        self.__active = True
        self.__state = 'idle'
        self.__running_event = None
        self.__queue = Queue()
        self.__event_thread = threading.Thread(
            name=self.__class__.__name__, target=self.event_loop)
        self.__lock = threading.Lock()

    # イベントスレッド開始メソッド
    def start(self):
        self.__app.logger.warning(self.__class__.__name__ + ' start')
        self.__event_thread.start()

    # イベントスレッド停止メソッド
    def stop(self):
        self.__app.logger.warning(self.__class__.__name__ + ' stop')
        self.__active = False
        self.__event_thread.join()

    # イベント設定
    def set_event(self, object, event):
        self.__app.logger.warning('set_event[' + event + ']')
        self.__queue.put({'object': object, 'event': event})

    # 実行状態取得
    def get_state(self):
        ret = {
            'state': self.__state,
            'item': self.__running_event
        }

        return ret

    def import_dataset(self, username, file, ckan_addr, ckan_apikey, organization, catalog_type, delete_catalog):
        """ カタログインポート

        指定されたファイルをCKANにインポートする。

        Args:
            - username: インポートするファイルのユーザ
            - file: インポートするファイル
            - ckan_addr: インポートするCKANアドレス
            - ckan_apikey: インポートするCKANアプリキー
            - organization: (str), 削除する場合のフィルターキーワード
            - catalog_type: (str), 削除するカタログサイト
            - delete_catalog: (bool), データカタログを削除判定

        Returns:
            ckanapiによる処理結果のログ
        """

        res_message = {
            'status': 'faild',
            'message': ''
        }

        try:
            save_dir = IMPORT_DIR + str(username) + '/'
            os.makedirs(save_dir, exist_ok=True)

            # ファイル保存(排他)
            self.__lock.acquire()
            filename = file.filename
            file.save(os.path.join(save_dir, filename))
            self.__lock.release()

        except OSError:
            self.__app.logger.error('インポートファイル保存エラー')
            raise CatalogToolException('import_dataset_FileSaveError', 500)

        # インポートイベント発行
        event_object = {
            'username': username,
            'filename': filename,
            'ckan_apikey': ckan_apikey,
            'ckan_addr': ckan_addr,
            'organization': organization,
            'catalog_type': catalog_type,
            'delete_catalog': delete_catalog
        }
        self.set_event(event_object, IMPORT_EVENT)

        res_message['status'] = 'success'
        res_message['message'] = 'インポート処理を受け付けました。'
        return res_message

    def export_dataset(self, username, organization, ckan_addr, ckan_apikey, ckan_type):
        """ カタログエクスポート

        CKANのデータセットを指定されたファイル名でエクスポートする。

        Args:
            - username: エクスポートするユーザ
            - organization: エクスポートするユーザの属する組織
            - ckan_addr: エクスポートするCKANアドレス
            - ckan_apikey: エクスポートするCKANアプリキー

        Returns:
            ckanapiによる処理結果のログ、エクスポートしたファイル名
        """

        res_message = {
            'status': 'faild',
            'message': '',
            'filename': ''
        }

        try:
            save_dir = EXPORT_DIR + str(username) + '/' + ckan_type + '/'
            os.makedirs(save_dir, exist_ok=True)

        except OSError:
            self.__app.logger.error('エクスポートフォルダ作成エラー')
            raise CatalogToolException('export_dataset_DirError', 500)

        # エクスポートイベント発行
        event_object = {
            'username': username,
            'organization': organization,
            'ckan_apikey': ckan_apikey,
            'ckan_addr': ckan_addr,
            'ckan_type': ckan_type
        }
        self.set_event(event_object, EXPORT_EVENT)

        res_message['status'] = 'success'
        res_message['message'] = 'エクスポート処理を受け付けました。'
        res_message['filename'] = str(username) + '_export.tar.gz'
        return res_message

    def available_export_file(self, username, ckan_type):
        """ エクスポートファイル取得判定

        Args:
            - username: 取得するファイルのユーザ

        Returns:
            True: エクスポートファイル取得可能
            False: エクスポートファイル取得不可
        """

        save_dir = EXPORT_DIR + str(username) + '/' + ckan_type + '/'
        export_file = save_dir + str(username) + '_export.tar.gz'
        if self.__state == 'processing':
            if self.__running_event:
                self.__app.logger.warning(self.__running_event)
                if (self.__running_event['event'] == EXPORT_EVENT
                   and self.__running_event['object']['username'] == username):
                    # エクスポート中
                    return False

        # インポートエクスポート処理待機中または別処理中
        if os.path.isfile(export_file):
            # ファイルあり
            return True

        # ファイルなし
        return False

    def get_file_path(self, username, ckan_type):
        """ エクスポートファイル名取得

        Args:
            - username: 取得するファイルのユーザ

        Returns:
            ckanapiによる処理結果のログ
        """

        save_dir = EXPORT_DIR + str(username) + '/' + ckan_type  + '/'
        filename = str(username) + '_export.tar.gz'
        export_file = save_dir + filename
        return export_file, filename

    # イベントメソッド処理メインメソッド
    def event_loop(self):
        while self.__active:
            try:
                # イベント受信処理実行
                item = self.__queue.get(timeout=1)
                self.__state = 'processing'
                self.__app.logger.warning(
                    self.__class__.__name__ + ' Event run')
                self.__app.logger.warning(item['event'])
                self.__app.logger.warning(item['object'])
                self.__running_event = item
                if item['event'] == IMPORT_EVENT:
                    self.__import(item['object']['username'],
                                  item['object']['filename'],
                                  item['object']['ckan_apikey'],
                                  item['object']['ckan_addr'],
                                  item['object']['organization'],
                                  item['object']['catalog_type'],
                                  item['object']['delete_catalog'])
                else:
                    self.__export(item['object']['username'],
                                  item['object']['organization'],
                                  item['object']['ckan_apikey'],
                                  item['object']['ckan_addr'],
                                  item['object']['ckan_type'])

                self.__state = 'idle'
                self.__running_event = None
            except Exception:
                continue

    # カタログ削除
    def __delete_catalog_ckan(self, addr, apikey, rows, organization):
        target_catalog_list = []

        # CKAN接続
        ckan_api = RemoteCKAN(addr, apikey=apikey)

        # すべての横断CKANのidをリストアップ
        # 条件に合うカタログを検索しリストアップ
        try:
            for org in organization:
                fq = 'organization:' + org
                result_catalog_list = ckan_api.action.package_search(
                    fq=fq, rows=rows)
                # ID(name)のみ抽出
                if result_catalog_list != []:
                    target_catalog_list.append(
                        [catalog['name'] for catalog in result_catalog_list['results']])

        except NotAuthorized:
            self.__app.logger.warning('カタログ検索 ユーザ承認エラー')
            self.__app.logger.warning(traceback.format_exc())
            return

        except AttributeError:
            self.__app.logger.warning('カタログ検索 変数の属性エラー')
            self.__app.logger.warning(traceback.format_exc())
            return

        except Exception:
            self.__app.logger.warning('カタログ検索 例外')
            self.__app.logger.warning(traceback.format_exc())
            return

        # カタログ削除
        catalog_id_list = [item for x in target_catalog_list for item in x]
        for catalog_id in catalog_id_list:
            self.__app.logger.warning('delete catalog : ' + catalog_id)
            try:
                ckan_api.action.package_delete(id=catalog_id)

            except NotAuthorized:
                self.__app.logger.warning('カタログ削除 ユーザ承認エラー')
                self.__app.logger.warning(traceback.format_exc())
                continue

            except AttributeError:
                self.__app.logger.warning('カタログ削除 変数の属性エラー')
                self.__app.logger.warning(traceback.format_exc())
                continue

            except Exception:
                self.__app.logger.warning('カタログ削除 例外')
                self.__app.logger.warning(traceback.format_exc())
                continue

    # 圧縮ファイルチェック
    def __gzfile_check(self, filename):
        if filename.split('.')[-1] == 'gz':
            return True
        else:
            return False

    # CKANインポート
    def __import(self,
                 username,
                 filename,
                 ckan_apikey,
                 ckan_addr,
                 organization,
                 catalog_type,
                 delete_catalog):

        self.__app.logger.warning('インポート処理を開始します')
        self.__app.logger.warning('username : ' + username)
        self.__app.logger.warning('filename : ' + filename)
        self.__app.logger.warning('ckan_addr : ' + ckan_addr)
        self.__app.logger.warning('ckan_apikey : ' + ckan_apikey)
        self.__app.logger.warning('organization : ')
        self.__app.logger.warning(organization)
        self.__app.logger.warning('catalog_type : ')
        self.__app.logger.warning(catalog_type)
        self.__app.logger.warning('delete_catalog : ')
        self.__app.logger.warning(delete_catalog)
        try:
            if not self.__gzfile_check(filename):
                raise GZFILETypeError('ファイルの拡張子が不正')

            # 古いインポートフォルダを削除
            save_dir = IMPORT_DIR + str(username) + '/'
            dirname = filename.split('.tar.gz')[0]
            remove_cmd = ['rm', '-rf', save_dir + dirname]
            proc_result = subprocess.run(
                remove_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.__app.logger.warning(proc_result)

            # インポートファイル解凍(排他)
            self.__lock.acquire()
            with tarfile.open(save_dir + filename, 'r:gz') as archive:
                archive.extractall(path=save_dir)

            self.__lock.release()

            # インポートファイル取得
            import_files = glob.glob(save_dir + dirname + '/*.json')
            self.__app.logger.warning('インポートファイル')
            self.__app.logger.warning(import_files)

            # カタログの削除処理
            if delete_catalog:
                self.__app.logger.warning('カタログ削除')
                rows = 1000
                self.__delete_catalog_ckan(
                    ckan_addr, ckan_apikey, rows, organization)

            # CKAN接続
            session = requests.Session()
            ckan_api = RemoteCKAN(
                ckan_addr, apikey=ckan_apikey, session=session)

            for file in import_files:
                # カタログ登録
                with open(file, mode='r') as f:
                    catalog_list = json.load(f)
                    for catalog in catalog_list:
                        # 現在日時の取得
                        current_datetime = datetime.datetime.now()
                        datetimestr = current_datetime.strftime(
                            '%Y%m%d%H%M%S%f')
                        new_ckan_url_name = 'ckan' + datetimestr

                        self.__app.logger.warning('CKANへカタログ情報をインポート')
                        self.__app.logger.warning(catalog['name'])
                        self.__app.logger.warning(catalog['title'])
                        group_list = [{'name': group['name']}
                                      for group in catalog['groups']]
                        ckan_api.action.package_create(name=new_ckan_url_name,
                                                       title=catalog['title'],
                                                       notes=catalog['notes'],
                                                       url=catalog['url'],
                                                       extras=catalog['extras'],
                                                       groups=group_list,
                                                       tags=catalog['tags'],
                                                       resources=catalog['resources'],
                                                       license_id=catalog['license_id'],
                                                       license_title=catalog['license_title'],
                                                       owner_org=catalog['organization']['name'])

            # 解凍したインポートフォルダを削除
            proc_result = subprocess.run(
                remove_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.__app.logger.warning(proc_result)

            # 解凍したインポートファイルを削除
            remove_cmd = ['rm', '-rf', save_dir + filename]
            proc_result = subprocess.run(
                remove_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.__app.logger.warning(proc_result)

        except GZFILETypeError:
            self.__app.logger.error(traceback.format_exc())
            self.res_message['message'] = 'GZ形式以外のファイルの時のエラー'

        except Exception:
            self.__app.logger.error(traceback.format_exc())
            self.res_message['message'] = 'その他のエラー'

        finally:
            self.__app.logger.warning('インポート処理を終了します')
            return self.res_message

    # CKANエクスポート
    def __export(self, username, organization, ckan_apikey, ckan_addr, ckan_type):

        save_dir = EXPORT_DIR + str(username) + \
            '/' + str(username) + '_export/'
        rows = 1000
        loop_cnt = 0

        try:
            # 古いエクスポートフォルダを削除
            remove_cmd = ['rm', '-rf', save_dir]
            proc_result = subprocess.run(
                remove_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.__app.logger.warning(proc_result)

            # エクスポートフォルダ作成
            os.makedirs(save_dir, exist_ok=True)

            # CKAN接続
            session = requests.Session()
            ckan_api = RemoteCKAN(
                ckan_addr, apikey=ckan_apikey, session=session)
            for __org in organization:
                filter = 'organization:' + __org
                start = 0
                while True:
                    release_datasets = ckan_api.action.package_search(
                        q='*:*', fq=filter, start=start, rows=rows)
                    if len(release_datasets['results']) == 0:
                        break

                    # ファイル保存
                    filename = str(username) + '_export' + \
                        str(loop_cnt) + '.json'
                    with open(save_dir + str(filename), mode='w') as f:
                        json.dump(
                            release_datasets['results'], f, ensure_ascii=False, indent=4)

                    start += rows
                    loop_cnt += 1

            # エクスポートフォルダ圧縮
            tar_name = EXPORT_DIR + \
                str(username) + '/' + ckan_type + '/' + str(username) + '_export.tar.gz'
            tar_save_dir = EXPORT_DIR + \
                str(username) + '/' + ckan_type + '/'
            with tarfile.open(tar_name, mode='w:gz') as archive:
                archive.add(save_dir, arcname=str(username) + '_export')

            # エクスポートフォルダ削除
            proc_result = subprocess.run(
                remove_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.__app.logger.warning(proc_result)

        except Exception:
            self.__app.logger.error(traceback.format_exc())
            self.res_message['message'] = 'その他のエラー'
            self.res_message['logs'] = str(traceback.format_exc())

        finally:
            return self.res_message
