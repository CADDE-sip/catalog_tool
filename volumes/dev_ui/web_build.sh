#!/bin/bash

# 現状のプロセスを停止
# docker rm -f `docker ps -a -q`

build_type=$1
CONTAINER=dev-vue

docker rm -f  $CONTAINER 
# リリースビルド => vueファイルをリリースビルドして、nginxの公開ディレクトリに配置
if [ "$build_type" == "build" ]
then
    echo 'portal quasar build '
    docker compose -f docker-compose-dev.yml -p catalogtool_dev_ui up -d
    docker exec -it $CONTAINER /bin/sh -c 'cd app; quasar build'
    docker compose -f docker-compose-dev.yml -p catalogtool_dev_ui down 
    cp -pR app/dist/spa/* ../nginx/public

# デバッグ用ビルド => vueファイルをデバッグビルド、docker-compose-dev.ymlのポートで公開 9000
elif [ "$build_type" == "debug" ]
then
    echo '================================ '
    echo 'portal quasar dev'
    echo '================================ '
    docker compose -f docker-compose-dev.yml up -d
    docker exec -it $CONTAINER /bin/sh -c 'cd app; quasar dev'

# コンテナログイン => ビルド用コンテナにログイン
elif [ "$build_type" == "login" ]
then
    echo '================================ '
    docker compose -f docker-compose-dev.yml up -d
    docker exec -it $CONTAINER /bin/sh 

# 新規作成 => quasar プロジェクトを新規作成
elif [ "$build_type" == "create"  ]
then
    echo '================================ '
    echo 'quasar create'
    echo '================================ '
    docker compose -f docker-compose-dev.yml up -d
    docker exec -it $CONTAINER /bin/sh -c 'yarn create quasar'

elif [ "$build_type" == "upgrade" ]
then
    echo '================================ '
    echo 'quasar upgrade'
    echo '# you must have app folder'
    echo '================================ '
    docker compose -f docker-compose-dev.yml up -d
    docker exec -it $CONTAINER /bin/sh -c 'cd app; quasar upgrade --install'

else
  echo "[Debug Build Command]"
  echo "sh client_build.sh dev"
  echo ""
  echo "[Release Build Command]"
  echo "sh client_build.sh build"
fi

