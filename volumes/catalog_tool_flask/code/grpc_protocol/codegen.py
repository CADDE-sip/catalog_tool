# Protocol Buffer変換
# 指定された.protoファイルをprotocol bufferへ変換する
#
# 実行方法:
#   python ./proto/codegen.py
# 出力ファイル:
#   - [protocol_filename]_pb2.py
#   - [protocol_filename]_pb2_grpc.py

from grpc.tools import protoc

# 変換対象のファイル名
dir_name = './grpc_protocol'
protocol_filename = 'ml_analysis.proto'

protoc.main(
    (
        '',
        '-I.',
        '--python_out=.',
        '--grpc_python_out=.',
        dir_name + '/' + protocol_filename,
    )
)
