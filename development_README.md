■「データカタログ作成支援ツール」の設定ファイル・ツール起動手順について

# 1．ファイル
##  1-1. ファイル構成
ディレクトリ名：cti-catalog-regist-tool
```
|- README.md
|- images
|- start.sh
|- docker-compose.yml
|- development_README.md
|- stop.sh
|- tool
   |- catalog_export.py
   |- catalog_import.py
   |- README.md
|- volumes
   |- catalog_tool_authentication_oauth2
   |- catalog_tool_flask
   |- catalog_tool_ngsi
   |- dev_ui
   |- nginx
   |- postgres
```

##  1-2．ファイル概要
  - tool/catalog_export.py：カタログエクスポートツール
  - tool/catalog_import.py：カタログインポートツール
  - volumes/catalog_tool_authentication_oauth2：認証CKAN連携用Dockerコンテナ
  - volumes/catalog_tool_flask：アプリサーバ用Dockerコンテナ
  - volumes/catalog_tool_ngsi：NGSI連携用Dockerコンテナ
  - volumes/nginx：Webサーバ＆リバースプロキシ用Dockerコンテナ
  - volumes/postgres：ユーザ情報格納DB用Dockerコンテナ
  - volumes/dev_ui：画面開発用フォルダ

# 2. 画面変更時の起動手順
  ①以下のコマンドを実行する
  ```
  cd /home/centos/cti-catalog-regist-tool/
  ./stop.sh
  ```
  ②以下のコマンドを実行する
  ```
  cd /home/centos/cti-catalog-regist-tool/volumes/dev_ui/
  ./web_build.sh build
  ```
  ③以下のコマンドを実行する
  ```
  cd /home/centos/cti-catalog-regist-tool/
  .start.sh
  ```

