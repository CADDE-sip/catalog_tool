# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import analyse_data_pb2 as analyse__data__pb2


class AnalyseServiceStub(object):
    # missing associated documentation comment in .proto file
    pass

    def __init__(self, channel):
        """Constructor.

        Args:
          channel: A grpc.Channel.
        """
        self.AnalyseServer = channel.stream_stream(
            '/analysis.AnalyseService/AnalyseServer',
            request_serializer=analyse__data__pb2.RequestMessage.SerializeToString,
            response_deserializer=analyse__data__pb2.ReplyMessage.FromString,
        )


class AnalyseServiceServicer(object):
    # missing associated documentation comment in .proto file
    pass

    def AnalyseServer(self, request_iterator, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AnalyseServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'AnalyseServer': grpc.stream_stream_rpc_method_handler(
            servicer.AnalyseServer,
            request_deserializer=analyse__data__pb2.RequestMessage.FromString,
            response_serializer=analyse__data__pb2.ReplyMessage.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'analysis.AnalyseService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
