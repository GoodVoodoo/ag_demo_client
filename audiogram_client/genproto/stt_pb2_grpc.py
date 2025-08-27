"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import stt_pb2 as stt__pb2

class STTStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.FileRecognize = channel.unary_unary('/mts.ai.audiogram.stt.v3.STT/FileRecognize', request_serializer=stt__pb2.FileRecognizeRequest.SerializeToString, response_deserializer=stt__pb2.FileRecognizeResponse.FromString)
        self.Recognize = channel.stream_stream('/mts.ai.audiogram.stt.v3.STT/Recognize', request_serializer=stt__pb2.RecognizeRequest.SerializeToString, response_deserializer=stt__pb2.RecognizeResponse.FromString)
        self.GetModelsInfo = channel.unary_unary('/mts.ai.audiogram.stt.v3.STT/GetModelsInfo', request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString, response_deserializer=stt__pb2.ModelsInfo.FromString)

class STTServicer(object):
    """Missing associated documentation comment in .proto file."""

    def FileRecognize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Recognize(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetModelsInfo(self, request, context):
        """rpc LongRunningRecognize(LongRunningRecognizeRequest) returns (mts.ai.audiogram.v1.Task);
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_STTServicer_to_server(servicer, server):
    rpc_method_handlers = {'FileRecognize': grpc.unary_unary_rpc_method_handler(servicer.FileRecognize, request_deserializer=stt__pb2.FileRecognizeRequest.FromString, response_serializer=stt__pb2.FileRecognizeResponse.SerializeToString), 'Recognize': grpc.stream_stream_rpc_method_handler(servicer.Recognize, request_deserializer=stt__pb2.RecognizeRequest.FromString, response_serializer=stt__pb2.RecognizeResponse.SerializeToString), 'GetModelsInfo': grpc.unary_unary_rpc_method_handler(servicer.GetModelsInfo, request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, response_serializer=stt__pb2.ModelsInfo.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('mts.ai.audiogram.stt.v3.STT', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class STT(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def FileRecognize(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mts.ai.audiogram.stt.v3.STT/FileRecognize', stt__pb2.FileRecognizeRequest.SerializeToString, stt__pb2.FileRecognizeResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Recognize(request_iterator, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/mts.ai.audiogram.stt.v3.STT/Recognize', stt__pb2.RecognizeRequest.SerializeToString, stt__pb2.RecognizeResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetModelsInfo(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mts.ai.audiogram.stt.v3.STT/GetModelsInfo', google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString, stt__pb2.ModelsInfo.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)