
##########
# 初期化 #
##########
tmpDirName="/_pycodetmp"
targetDir=$1
if [ "x$targetDir" = "x" ]; then
  targetDir="."
fi

#########
# pyc化 #
#########
# 元コードを一時避難するディレクトリを作成
mkdir -p $targetDir$tmpDirName

# ".py"コードを捜索してリスト化
for pyfile in `find $targetDir -type f -name "*.py"`; do
  filepath+=($pyfile)
done

# pythonコンパイル実行し".pyc"を作成
python3 -m compileall -b ${filepath[@]}

# ".py"元コードをすべて避難
for pyfile in ${filepath[@]}; do
  if [[ "$pyfile" == */* ]]; then
    mvFileName=(`echo $pyfile | tr -s '/' ' '`)
    lastIndex=`expr ${#mvFileName[@]} - 1`
  fi
  # パス変更コマンド実行
  mv $pyfile $targetDir"/"$tmpDirName"/"${mvFileName[${lastIndex}]}
done

