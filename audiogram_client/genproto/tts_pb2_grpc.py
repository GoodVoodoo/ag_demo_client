"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import tts_pb2 as tts__pb2

class TTSStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StreamingSynthesize = channel.unary_stream('/mts.ai.audiogram.tts.v2.TTS/StreamingSynthesize', request_serializer=tts__pb2.SynthesizeSpeechRequest.SerializeToString, response_deserializer=tts__pb2.StreamingSynthesizeSpeechResponse.FromString)
        self.Synthesize = channel.unary_unary('/mts.ai.audiogram.tts.v2.TTS/Synthesize', request_serializer=tts__pb2.SynthesizeSpeechRequest.SerializeToString, response_deserializer=tts__pb2.SynthesizeSpeechResponse.FromString)
        self.GetModelsInfo = channel.unary_unary('/mts.ai.audiogram.tts.v2.TTS/GetModelsInfo', request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString, response_deserializer=tts__pb2.ModelsInfo.FromString)

class TTSServicer(object):
    """Missing associated documentation comment in .proto file."""

    def StreamingSynthesize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Synthesize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetModelsInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_TTSServicer_to_server(servicer, server):
    rpc_method_handlers = {'StreamingSynthesize': grpc.unary_stream_rpc_method_handler(servicer.StreamingSynthesize, request_deserializer=tts__pb2.SynthesizeSpeechRequest.FromString, response_serializer=tts__pb2.StreamingSynthesizeSpeechResponse.SerializeToString), 'Synthesize': grpc.unary_unary_rpc_method_handler(servicer.Synthesize, request_deserializer=tts__pb2.SynthesizeSpeechRequest.FromString, response_serializer=tts__pb2.SynthesizeSpeechResponse.SerializeToString), 'GetModelsInfo': grpc.unary_unary_rpc_method_handler(servicer.GetModelsInfo, request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, response_serializer=tts__pb2.ModelsInfo.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('mts.ai.audiogram.tts.v2.TTS', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class TTS(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def StreamingSynthesize(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_stream(request, target, '/mts.ai.audiogram.tts.v2.TTS/StreamingSynthesize', tts__pb2.SynthesizeSpeechRequest.SerializeToString, tts__pb2.StreamingSynthesizeSpeechResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Synthesize(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mts.ai.audiogram.tts.v2.TTS/Synthesize', tts__pb2.SynthesizeSpeechRequest.SerializeToString, tts__pb2.SynthesizeSpeechResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetModelsInfo(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mts.ai.audiogram.tts.v2.TTS/GetModelsInfo', google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString, tts__pb2.ModelsInfo.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)