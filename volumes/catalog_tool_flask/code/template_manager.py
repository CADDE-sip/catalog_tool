import os
import shutil
import json
import traceback

from catalogtool_exception import CatalogToolException


class CatalogTemplate:

    TEMPLATE_DIR = './data/template/'
    DEFAULT_TEMPLATE = 'template_default.json'
    TEMPLATE_FILENAME = 'template.json'

    def __init__(self, app, username):
        self.__app = app
        self.__username = username
        self.__template_filedir = self.TEMPLATE_DIR + username
        self.__template_filename = self.__template_filedir + '/' + self.TEMPLATE_FILENAME
        self.__template_default_filename = self.TEMPLATE_DIR + self.DEFAULT_TEMPLATE

        # フォルダが無かったら作成する
        if not os.path.isdir(self.__template_filedir):
            os.makedirs(self.__template_filedir)

        # ファイルが無かったらデフォルトファイルをコピーする
        if not os.path.isfile(self.__template_filename):
            shutil.copyfile(self.TEMPLATE_DIR
                            + self.DEFAULT_TEMPLATE, self.__template_filename)

    def save_template(self, template):
        """ テンプレート保存

        ユーザごとのディレクトリ配下にテンプレートを保存する

        Args:
            Dict: 保存するテンプレート
              - catalog_display: 画面表示制御用設定
              - catalog_value: フィールドデフォルト値

        Returns:
            Dict: テンプレート保存結果
              - status: テンプレート保存結果
              - message: メッセージ

        """
        ret = {
            'status': 'failed',
            'message': ''
        }
        try:
            with open(self.__template_filename, mode='w') as f:
                json.dump(template, f, ensure_ascii=False, indent=4)

            ret['message'] = 'テンプレート保存完了'
            ret['status'] = 'success'
        except OSError:
            self.__app.logger.error(traceback.format_exc())
            raise CatalogToolException('get_template_FileSaveError', 500)

        return ret

    def get_template(self):
        """ テンプレート取得

        ユーザごとのディレクトリ配下からテンプレートを取得する

        Returns:
            Dict: テンプレート保存結果
              - status: テンプレート保存結果
              - message: メッセージ
              - template: テンプレート
                - catalog_display: 画面表示制御用設定
                - catalog_value: フィールドデフォルト値

        """
        ret = {
            'status': 'failed',
            'message': '',
            'template': None
        }
        try:
            with open(self.__template_filename, mode='r') as f:
                ret['template'] = json.load(f)

            ret['message'] = 'テンプレート取得完了'
            ret['status'] = 'success'
        except OSError:
            self.__app.logger.error(traceback.format_exc())
            raise CatalogToolException('get_template_FileOpenError', 500)

        return ret
