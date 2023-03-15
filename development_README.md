■「データカタログ作成支援ツール」の設定ファイル・ツール起動手順について

# 1．ファイル
##  1-1. ファイル構成
 ディレクトリ名：cti-catalog-regist-tool
   |
   |- README.md
   |- images
   |- start.sh
   |- volumes
        |- catalog_tool_flask
        |- catalog_tool_ml
        |- dev_catalog_web
        |- nginx
   |- docker-compose.y
   |- internal_README.md
   |- stop.sh

##  1-2．ファイル概要
  ・catalog_tool_flask：アプリサーバ用Docker
  ・catalog_tool_ml：機械学習サーバ用Docke
  ・nginx：Webサーバ用Docker
  ・dev_catalog_web：画面開発用フォルダ

# 2. 画面変更時の起動手順
  ①以下のコマンドを実行する
  ```
  cd /home/centos/cti-catalog-regist-tool/
  ./stop.sh
  ```
  ②以下のコマンドを実行する
  ```
  cd /home/centos/cti-catalog-regist-tool/volumes/dev_catalog_web/
  ./web_build.sh build
  ```
  ③以下のコマンドを実行する
  ```
  cd /home/centos/cti-catalog-regist-tool/
  .start.sh
  ```
