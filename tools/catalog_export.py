#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import json
import tarfile
import subprocess
import traceback

from ckanapi import RemoteCKAN, NotAuthorized

# CKANエクスポート
def export_dataset(filename, organization, ckan_addr, ckan_apikey):
    """ カタログエクスポート

    CKANのデータセットを指定されたファイル名でエクスポートする。

    Args:
        - filename: エクスポートファイル名
        - organization: エクスポートするユーザの属する組織
        - ckan_addr: エクスポートするCKANアドレス
        - ckan_apikey: エクスポートするCKANアプリキー
    """

    print('エクスポートファイル名 ：', filename)
    print('エクスポート対象の組織 ：', organization)
    print('エクスポート対象のCKAN ：', ckan_addr)
    print('対象となるCKANのAPIキー：', ckan_apikey)

    start = 0
    rows = 1000
    loop_cnt = 0
    try:
        print('古いエクスポートフォルダを削除します。')
        dirname = filename.split('.')[0]
        remove_cmd = ['rm', '-rf', dirname]
        proc_result = subprocess.run(remove_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # エクスポートフォルダ作成
        print('エクスポートフォルダを作成します。')
        os.makedirs(dirname, exist_ok=True)

        # CKAN接続
        print('CKANに接続します。')
        ckan_api = RemoteCKAN(ckan_addr, apikey=ckan_apikey)

        print('CKANからカタログをエクスポートします。')
        filter = 'organization:' + organization
        while True:
            release_datasets = ckan_api.action.package_search(q='*:*', fq=filter, start=start, rows=rows)
            if len(release_datasets['results']) == 0:
                break

            # ファイル保存
            tmpfile = 'export' + str(loop_cnt) + '.json'
            print('...エクスポート結果(最大1000件)保存', tmpfile)
            with open(dirname + '/' + tmpfile, mode='w') as f:
                json.dump(release_datasets['results'], f, ensure_ascii=False, indent=4)

            start += rows
            loop_cnt += 1

        # エクスポートフォルダ圧縮
        print('エクスポートフォルダを圧縮します。')
        with tarfile.open(filename, mode='w:gz') as archive:
            archive.add(dirname, arcname=dirname)

        # エクスポートフォルダ削除
        print('エクスポートフォルダを削除します。')
        proc_result = subprocess.run(remove_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('CKANからのエクスポートに成功しました。')

    except Exception as e:
        print('CKANからのエクスポートに失敗しました。')
        print(traceback.format_exc())

if __name__ == '__main__':
    # プログラム引数
    parser = argparse.ArgumentParser(description='catalog import.')
    parser.add_argument('-f', '--file', default='export.tar.gz', type=str, help='export file name.')
    parser.add_argument('-o', '--organization', type=str, help='organization for catalog.')
    parser.add_argument('-u', '--url', type=str, help='CKAN access URL. ex:http://localhost:5000/')
    parser.add_argument('-k', '--apikey', type=str, help='CKAN access apikey.')
    args = parser.parse_args()

    if not args.url:
        print('CKANアクセスURLを指定してください。')
        exit(0)

    if not args.apikey:
        print('CKANアクセスキーを指定してください。')
        exit(0)

    if not args.organization:
        print('エクスポート対象となる組織を指定してください。')
        exit(0)

    if not args.file.endswith('tar.gz'):
        print('サポート外のエクスポートファイル名です。')
        print('エクスポートファイル名はtar.gz形式のファイル名を指定してください。')
        exit(0)

    # インポート処理実行
    export_dataset(args.file, args.organization, args.url, args.apikey);
