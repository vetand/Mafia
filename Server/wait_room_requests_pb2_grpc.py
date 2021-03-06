# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import wait_room_requests_pb2 as wait__room__requests__pb2


class WaitRoomReqtestsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AskProgress = channel.unary_unary(
                '/wait_room_requests.WaitRoomReqtests/AskProgress',
                request_serializer=wait__room__requests__pb2.AskProgressRequest.SerializeToString,
                response_deserializer=wait__room__requests__pb2.SessionLoadProgress.FromString,
                )
        self.Register = channel.unary_unary(
                '/wait_room_requests.WaitRoomReqtests/Register',
                request_serializer=wait__room__requests__pb2.RegisterRequest.SerializeToString,
                response_deserializer=wait__room__requests__pb2.RegisterResponse.FromString,
                )
        self.AskPlayPort = channel.unary_unary(
                '/wait_room_requests.WaitRoomReqtests/AskPlayPort',
                request_serializer=wait__room__requests__pb2.PortRequest.SerializeToString,
                response_deserializer=wait__room__requests__pb2.PortResponse.FromString,
                )
        self.ReturnRoom = channel.unary_unary(
                '/wait_room_requests.WaitRoomReqtests/ReturnRoom',
                request_serializer=wait__room__requests__pb2.EndSession.SerializeToString,
                response_deserializer=wait__room__requests__pb2.EndSession.FromString,
                )


class WaitRoomReqtestsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AskProgress(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Register(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AskPlayPort(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReturnRoom(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WaitRoomReqtestsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AskProgress': grpc.unary_unary_rpc_method_handler(
                    servicer.AskProgress,
                    request_deserializer=wait__room__requests__pb2.AskProgressRequest.FromString,
                    response_serializer=wait__room__requests__pb2.SessionLoadProgress.SerializeToString,
            ),
            'Register': grpc.unary_unary_rpc_method_handler(
                    servicer.Register,
                    request_deserializer=wait__room__requests__pb2.RegisterRequest.FromString,
                    response_serializer=wait__room__requests__pb2.RegisterResponse.SerializeToString,
            ),
            'AskPlayPort': grpc.unary_unary_rpc_method_handler(
                    servicer.AskPlayPort,
                    request_deserializer=wait__room__requests__pb2.PortRequest.FromString,
                    response_serializer=wait__room__requests__pb2.PortResponse.SerializeToString,
            ),
            'ReturnRoom': grpc.unary_unary_rpc_method_handler(
                    servicer.ReturnRoom,
                    request_deserializer=wait__room__requests__pb2.EndSession.FromString,
                    response_serializer=wait__room__requests__pb2.EndSession.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'wait_room_requests.WaitRoomReqtests', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WaitRoomReqtests(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AskProgress(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/wait_room_requests.WaitRoomReqtests/AskProgress',
            wait__room__requests__pb2.AskProgressRequest.SerializeToString,
            wait__room__requests__pb2.SessionLoadProgress.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/wait_room_requests.WaitRoomReqtests/Register',
            wait__room__requests__pb2.RegisterRequest.SerializeToString,
            wait__room__requests__pb2.RegisterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AskPlayPort(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/wait_room_requests.WaitRoomReqtests/AskPlayPort',
            wait__room__requests__pb2.PortRequest.SerializeToString,
            wait__room__requests__pb2.PortResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReturnRoom(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/wait_room_requests.WaitRoomReqtests/ReturnRoom',
            wait__room__requests__pb2.EndSession.SerializeToString,
            wait__room__requests__pb2.EndSession.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
