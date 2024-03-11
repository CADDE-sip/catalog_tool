# カタログ作成ツール OAuth2認証拡張コンテナ

## 概要
 - OAuth2認証拡張コンテナはカタログ作成ツールの認証拡張機能として提供します。
 - OAuth2認証拡張コンテナはOAuth2認証サーバと連携したCKANのユーザ認証を行います。
 - カタログ作成ツールでOAuth2認証拡張コンテナを利用する構成は、カタログサイトとしてCKANにCKAN OAuth2 Extension(※)を適用している環境を想定しています。

(※) https://github.com/conwetlab/ckanext-oauth2

<br>
本機能はカタログ作成ツールの一部であるため、本機能を使用する場合は、カタログ作成ツールの構築時に本機能も構築する必要があります。

## システム構成図
OAuth2認証拡張コンテナを使用したカタログツールのシステム構成を下記に示します。
![Alt text](catalog_authentication_oauth2.png?raw=true "Title")<br>

## 前提条件
OAuth2認証拡張コンテナの前提条件を示します。<br>

 - OAuth2認証拡張コンテナはカタログ作成ツールを構成するコンテナの１つであり、カタログ作成ツールと同じホストで起動してください。


## 構築手順
本機能はカタログ作成ツールの構築時に同時に構築されます。<br>

1. ソースの構成 <br>
OAuth2認証拡張コンテナのソースを展開し、カタログ作成ツールの volumesディレクトリにコピーしてください。
```
tar -xvf catalog_tool_authentication_oauth2.tar.gz 
cp -a catalog_tool_authentication_oauth2 cti-catalog-regist-tool/volumes/
```

2. Dockerファイルの修正 <br>
OAuth2認証拡張コンテナを起動するために、docker-compose.ymlを修正します。<br>
docker-compose.ymlファイルの末尾に以下の記載を追加してください。
```
  catalog_tool_authentication_oauth2:
    build: ./volumes/catalog_tool_authentication_oauth2
    image: authentication-oauth2
    hostname: catalog-tool-authentication-oauth2
    container_name: catalog-tool-authentication-oauth2
    restart: always
    #ports:
    #  - "28080:28080"
    tty: true
    volumes:
      - "./volumes/catalog_tool_authentication_oauth2:/code"
    command: ['python3', '-m', 'swagger_server']
```

3. コンフィグファイルの設定
OAuth2認証サーバへアクセスするための設定をコンフィグファイルに記載します。コンフィグファイルの設定の詳細は「コンフィグファイル」を参照してください。

4. カタログ作成ツールを起動します。

## コンフィグファイル
本機能で使用するコンフィグファイルの詳細を記載します。<br>
コンフィグファイルでは、OAuth2認証サーバの認証方法の設定を行います。<br>
コンフィグファイルは以下に格納されています。<br>

- config.json
  <br>catalog_tool_authentication_oauth2/swagger_server/configs<br>

(1) OAuth2認証サーバの認証方法の設定<br>
  (1-1) OAuth2認証サーバに対してClient Credentials Grant認証する場合

  | 設定パラメータ     | 概要                                                                                                         |
  | :----------------- | :------------------------------------------------------------------------------------------------------------ |
  | oauth2_auth        | 以下の設定パラメータを配列で保持                                                                              |
  | ckan_url           | CKANのURLを設定                                                                                               |
  | username           | CKANのログインユーザ名を設定                                                                                  |
  | auth_type          | 認証方式を設定<br>  Client Credentials Grant認証の場合は"client_credential"を設定                             |
  | authentication_url | 認証サーバのAPIエンドポイントのURLを設定                                                                      |
  | client_id          | 認証サーバでCKANログインユーザ名に紐づいたクライアントIDを設定                                                |
  | client_secret      | 認証サーバでCKANログインユーザ名に紐づいたクライアントシークレットを設定                                      |
  
  (1-2) OAuth2認証サーバに対してResource Owner Password Credentials Grant認証する場合

  | 設定パラメータ     | 概要                                                                                                         |
  | :----------------- | :------------------------------------------------------------------------------------------------------------ |
  | oauth2_auth        | 以下の設定パラメータを配列で保持                                                                              |
  | ckan_url           | CKANのURLを設定                                                                                               |
  | username           | CKANのログインユーザ名を設定                                                                                  |
  | auth_type          | 認証方式を設定<br>  Resource Owner Password Credentials Grant認証する場合は"password"を設定                   |
  | authentication_url | 認証サーバのAPIエンドポイントのURLを設定                                                                      |
  | password           | CKANのログインパスワードを設定                                                                                |
  | client_id          | 認証サーバでCKANログインユーザ名に紐づいたクライアントIDを設定                                                |
  | client_secret      | 認証サーバでCKANログインユーザ名に紐づいたクライアントシークレットを設定                                      |
  

