import os
import json
import datetime
import traceback
import glob

from catalogtool_exception import CatalogToolException

TMP_SAVE_DIR = './data/tmp_save/'

# カタログデータの一時保存


def write_tmp_data(app, data, username):
    res = {
        'status': 'failed',
        'message': ''
    }

    save_dir = TMP_SAVE_DIR + str(username) + '/'
    now = datetime.datetime.now()
    now = now.strftime('%Y%m%d%H%M%S')
    data['tmpFile'].update({'saved': now})

    file_name = data['tmpFile']['tmp_file_name'] + '.json'

    try:
        os.makedirs(save_dir, exist_ok=True)
        with open(save_dir + str(file_name), mode='w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            res['status'] = 'success'
            res['message'] = 'カタログの一時保存に成功しました。'

    except OSError as e:
        app.logger.error(e)
        app.logger.error(traceback.format_exc())
        raise CatalogToolException('write_tmp_data_FileSaveError', 500)

    return res

# 一時保存データの取得


def get_tmp_data_files(app, username):
    save_dir = TMP_SAVE_DIR + str(username)
    tmp_files = glob.glob(save_dir + '/*.json')

    tmp_data_list = []
    try:
        for file in tmp_files:
            with open(file, mode='r') as f:
                json_load = json.load(f)
                tmp_data_list.append(json_load)

    except OSError as e:
        app.logger.error(e)
        app.logger.error(traceback.format_exc())
        raise CatalogToolException('get_tmp_data_files_FileOpenError', 500)

    return tmp_data_list

# 一時保存データの削除


def delete_tmp_data(app, data, username):
    res = {
        'status': 'failed',
        'message': '',
        'del_data': []
    }

    for title in data:
        del_data_path = TMP_SAVE_DIR + \
            str(username) + '/' + str(title) + '.json'
        try:
            os.remove(del_data_path)
            if not os.path.exists(del_data_path):
                res['del_data'].append(title)
        except OSError:
            app.logger.error('一時保存データ[' + title + ']の削除に失敗しました。')
            raise CatalogToolException('get_tmp_data_files_FileOpenError', 500)

    res['status'] = 'success'
    res['message'] = 'カタログの削除に成功しました。'
    return res
