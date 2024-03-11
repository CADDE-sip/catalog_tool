# データ提供者用インポートツール・エクスポートツールの使い方

# 1. 前提条件
Python3インストール

```
yum install python3
```

clanapiインストール
```
pip3 install ckanapi
```

# 2．インポートツール

```
$ python3 catalog_import.py -f {インポートファイル名} -u {CKANアクセスURL} -k {CKANアクセスキー}
```
コマンド結果

```
$ python3 catalog_import.py -f import_trial.tar.gz -u http://localhost:5500/ -k 04c76dfa-0adb-4fd8-941a-5c57926a3009
インポートファイル名   ： import_trial.tar.gz
インポート対象のCKAN   ： http://localhost:5500/
対象となるCKANのAPIキー： 04c76dfa-0adb-4fd8-941a-5c57926a3009
古いインポートフォルダを削除します。
インポートファイルを解凍します。
CKANに接続します。
CKANにカタログをインポートします。
...カタログ[ 横断複製 ]をインポートします。
解凍したインポートフォルダを削除します。
CKANへのインポートに成功しました。
```

# 3．エクスポートツール

```
$ python3 catalog_export.py -a {CKANのユーザ名} -u {CKANアクセスURL} -k {CKANアクセスキー}
```
コマンド結果

```
$ python3 catalog_export.py -u http://localhost:5000/ -k 04c76dfa-0adb-4fd8-941a-5c57926a3009 -o sip-test
エクスポートファイル名 ： export.tar.gz
エクスポート対象の組織 ： sip-test
エクスポート対象のCKAN ： http://localhost:5000/
対象となるCKANのAPIキー： 04c76dfa-0adb-4fd8-941a-5c57926a3009
古いエクスポートフォルダを削除します。
エクスポートフォルダを作成します。
CKANに接続します。
CKANからカタログをエクスポートします。
...エクスポート結果(最大1000件)保存 export0.json
エクスポートフォルダを圧縮します。
エクスポートフォルダを削除します。
CKANからのエクスポートに成功しました。
```
