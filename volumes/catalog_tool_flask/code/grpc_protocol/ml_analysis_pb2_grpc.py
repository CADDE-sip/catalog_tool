# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from grpc_protocol import ml_analysis_pb2 as grpc__protocol_dot_ml__analysis__pb2


class AnalyseServiceStub(object):
    """サービスの定義
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ThemeKeywordAnalyseServer = channel.stream_stream(
            '/mlAnalysis.AnalyseService/ThemeKeywordAnalyseServer',
            request_serializer=grpc__protocol_dot_ml__analysis__pb2.AnalysisThemeKeyword.SerializeToString,
            response_deserializer=grpc__protocol_dot_ml__analysis__pb2.ReplyThemeKeyword.FromString,
        )
        self.TemporalAnalyseServer = channel.stream_stream(
            '/mlAnalysis.AnalyseService/TemporalAnalyseServer',
            request_serializer=grpc__protocol_dot_ml__analysis__pb2.AnalysisTemporal.SerializeToString,
            response_deserializer=grpc__protocol_dot_ml__analysis__pb2.ReplyTemporal.FromString,
        )
        self.SpatialAnalyseServer = channel.stream_stream(
            '/mlAnalysis.AnalyseService/SpatialAnalyseServer',
            request_serializer=grpc__protocol_dot_ml__analysis__pb2.AnalysisSpatial.SerializeToString,
            response_deserializer=grpc__protocol_dot_ml__analysis__pb2.ReplySpatial.FromString,
        )


class AnalyseServiceServicer(object):
    """サービスの定義
    """

    def ThemeKeywordAnalyseServer(self, request_iterator, context):
        """テーマ・キーワードのサービス
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TemporalAnalyseServer(self, request_iterator, context):
        """データセットの対象期間推測のサービス
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SpatialAnalyseServer(self, request_iterator, context):
        """データセットの対象地域推測のサービス
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AnalyseServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'ThemeKeywordAnalyseServer': grpc.stream_stream_rpc_method_handler(
            servicer.ThemeKeywordAnalyseServer,
            request_deserializer=grpc__protocol_dot_ml__analysis__pb2.AnalysisThemeKeyword.FromString,
            response_serializer=grpc__protocol_dot_ml__analysis__pb2.ReplyThemeKeyword.SerializeToString,
        ),
        'TemporalAnalyseServer': grpc.stream_stream_rpc_method_handler(
            servicer.TemporalAnalyseServer,
            request_deserializer=grpc__protocol_dot_ml__analysis__pb2.AnalysisTemporal.FromString,
            response_serializer=grpc__protocol_dot_ml__analysis__pb2.ReplyTemporal.SerializeToString,
        ),
        'SpatialAnalyseServer': grpc.stream_stream_rpc_method_handler(
            servicer.SpatialAnalyseServer,
            request_deserializer=grpc__protocol_dot_ml__analysis__pb2.AnalysisSpatial.FromString,
            response_serializer=grpc__protocol_dot_ml__analysis__pb2.ReplySpatial.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'mlAnalysis.AnalyseService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

 # This class is part of an EXPERIMENTAL API.


class AnalyseService(object):
    """サービスの定義
    """

    @staticmethod
    def ThemeKeywordAnalyseServer(request_iterator,
                                  target,
                                  options=(),
                                  channel_credentials=None,
                                  call_credentials=None,
                                  insecure=False,
                                  compression=None,
                                  wait_for_ready=None,
                                  timeout=None,
                                  metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/mlAnalysis.AnalyseService/ThemeKeywordAnalyseServer',
                                               grpc__protocol_dot_ml__analysis__pb2.AnalysisThemeKeyword.SerializeToString,
                                               grpc__protocol_dot_ml__analysis__pb2.ReplyThemeKeyword.FromString,
                                               options, channel_credentials,
                                               insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TemporalAnalyseServer(request_iterator,
                              target,
                              options=(),
                              channel_credentials=None,
                              call_credentials=None,
                              insecure=False,
                              compression=None,
                              wait_for_ready=None,
                              timeout=None,
                              metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/mlAnalysis.AnalyseService/TemporalAnalyseServer',
                                               grpc__protocol_dot_ml__analysis__pb2.AnalysisTemporal.SerializeToString,
                                               grpc__protocol_dot_ml__analysis__pb2.ReplyTemporal.FromString,
                                               options, channel_credentials,
                                               insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SpatialAnalyseServer(request_iterator,
                             target,
                             options=(),
                             channel_credentials=None,
                             call_credentials=None,
                             insecure=False,
                             compression=None,
                             wait_for_ready=None,
                             timeout=None,
                             metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/mlAnalysis.AnalyseService/SpatialAnalyseServer',
                                               grpc__protocol_dot_ml__analysis__pb2.AnalysisSpatial.SerializeToString,
                                               grpc__protocol_dot_ml__analysis__pb2.ReplySpatial.FromString,
                                               options, channel_credentials,
                                               insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
