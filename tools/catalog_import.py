#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import json
import tarfile
import glob
import subprocess
import traceback

from ckanapi import RemoteCKAN, NotAuthorized

# CKANインポート
def import_dataset(filename, ckan_addr, ckan_apikey, clear_flag=False, organization=None):
    """ カタログインポート

    指定されたファイルをCKANにインポートする。

    Args:
        - file: インポートするファイル
        - ckan_addr: インポートするCKANアドレス
        - ckan_apikey: インポートするCKANアプリキー
    """

    print('インポートファイル名   ：', filename)
    print('インポート対象のCKAN   ：', ckan_addr)
    print('対象となるCKANのAPIキー：', ckan_apikey)
    print('インポート先CKANの登録カタログ削除フラグ：', clear_flag)
    print('削除するカタログの組織：', organization)

    try:
        print('古いインポートフォルダを削除します。')
        dirname = filename.split('.')[0]
        remove_cmd = ['rm', '-rf', dirname]
        proc_result = subprocess.run(remove_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # インポートファイル解凍
        print('インポートファイルを解凍します。')
        with tarfile.open(filename, 'r:gz') as archive:
            archive.extractall(path='.')

        # インポートファイル取得
        import_files = glob.glob(dirname + '/*.json')

        # CKAN接続
        print('CKANに接続します。')
        ckan_api = RemoteCKAN(ckan_addr, apikey=ckan_apikey)

        # 削除対象のカタログを検索
        if clear_flag:
            search_catalog_list = ckan_api.action.package_search(fq=fq)
            app.logger.warning('カタログ検索結果')
            app.logger.warning(search_catalog_list)

        print('CKANにカタログをインポートします。')
        """
        for file in import_files:
            # カタログ登録
            with open(file, mode='r') as f:
                catalog_list = json.load(f)
                for catalog in catalog_list:
                    print('...カタログ[', catalog['title'], ']をインポートします。')
                    group_list = [ { 'name': group['name'] } for group in catalog['groups'] ]
                    pkg = ckan_api.action.package_create(name=catalog['name'],
                                                         title=catalog['title'],
                                                         notes=catalog['notes'],
                                                         url=catalog['url'],
                                                         extras = catalog['extras'],
                                                         groups=group_list,
                                                         tags=catalog['tags'],
                                                         resources=catalog['resources'],
                                                         license_id=catalog['license_id'],
                                                         license_title=catalog['license_title'],
                                                         owner_org=catalog['organization']['name'])

        print('解凍したインポートフォルダを削除します。')
        proc_result = subprocess.run(remove_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        """
        print('CKANへのインポートに成功しました。')

    except Exception as e:
        print('CKANへのインポートに失敗しました。')
        print(traceback.format_exc())

if __name__ == '__main__':
    # プログラム引数
    parser = argparse.ArgumentParser(description='catalog import name.')
    parser.add_argument('-f', '--file', type=str, help='import file.')
    parser.add_argument('-u', '--url', type=str, help='CKAN access URL. ex:http://localhost:5000/')
    parser.add_argument('-k', '--apikey', type=str, help='CKAN access apikey.')
    parser.add_argument('-c', '--clear', type=str, help='CKAN access apikey.')
    parser.add_argument('-o', '--organization', type=str, help='CKAN access apikey.')
    args = parser.parse_args()

    if not args.file:
        print('インポートファイルを指定してください。')
        exit(0)

    if not args.url:
        print('CKANアクセスURLを指定してください。')
        exit(0)

    if not args.apikey:
        print('CKANアクセスキーを指定してください。')
        exit(0)

    if args.clear and not args.organization:
        print('カタログを削除する場合は、削除対象のカタログの組織を指定してください。')
        exit(0)

    # インポートファイルチェック
    if not os.path.isfile(args.file):
        print('指定されたインポートファイルが存在しません。')
        exit(0)

    if not args.file.endswith('tar.gz'):
        print('サポート外のインポートファイル名です。')
        print('インポートファイル名はエクスポートにて出力されたtar.gz形式のファイル名を指定してください。')
        exit(0)

    # インポート処理実行
    import_dataset(args.file, args.url, args.apikey, args.clear, args.organization);

