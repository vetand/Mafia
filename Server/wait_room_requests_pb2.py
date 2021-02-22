# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: wait_room_requests.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='wait_room_requests.proto',
  package='wait_room_requests',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x18wait_room_requests.proto\x12\x12wait_room_requests\"\x1a\n\nEndSession\x12\x0c\n\x04port\x18\x01 \x01(\x05\"\"\n\x12\x41skProgressRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x1f\n\x0fRegisterRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"@\n\x10RegisterResponse\x12\x12\n\nvalid_name\x18\x01 \x01(\x08\x12\x18\n\x10\x61vailable_server\x18\x02 \x01(\x08\">\n\x13SessionLoadProgress\x12\x19\n\x11players_remaining\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x03(\t\"\x1b\n\x0bPortRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x1c\n\x0cPortResponse\x12\x0c\n\x04port\x18\x01 \x01(\x05\x32\xf1\x02\n\x10WaitRoomReqtests\x12`\n\x0b\x41skProgress\x12&.wait_room_requests.AskProgressRequest\x1a\'.wait_room_requests.SessionLoadProgress\"\x00\x12W\n\x08Register\x12#.wait_room_requests.RegisterRequest\x1a$.wait_room_requests.RegisterResponse\"\x00\x12R\n\x0b\x41skPlayPort\x12\x1f.wait_room_requests.PortRequest\x1a .wait_room_requests.PortResponse\"\x00\x12N\n\nReturnRoom\x12\x1e.wait_room_requests.EndSession\x1a\x1e.wait_room_requests.EndSession\"\x00\x62\x06proto3'
)




_ENDSESSION = _descriptor.Descriptor(
  name='EndSession',
  full_name='wait_room_requests.EndSession',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='port', full_name='wait_room_requests.EndSession.port', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=48,
  serialized_end=74,
)


_ASKPROGRESSREQUEST = _descriptor.Descriptor(
  name='AskProgressRequest',
  full_name='wait_room_requests.AskProgressRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='wait_room_requests.AskProgressRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=76,
  serialized_end=110,
)


_REGISTERREQUEST = _descriptor.Descriptor(
  name='RegisterRequest',
  full_name='wait_room_requests.RegisterRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='wait_room_requests.RegisterRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=112,
  serialized_end=143,
)


_REGISTERRESPONSE = _descriptor.Descriptor(
  name='RegisterResponse',
  full_name='wait_room_requests.RegisterResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='valid_name', full_name='wait_room_requests.RegisterResponse.valid_name', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='available_server', full_name='wait_room_requests.RegisterResponse.available_server', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=145,
  serialized_end=209,
)


_SESSIONLOADPROGRESS = _descriptor.Descriptor(
  name='SessionLoadProgress',
  full_name='wait_room_requests.SessionLoadProgress',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='players_remaining', full_name='wait_room_requests.SessionLoadProgress.players_remaining', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='wait_room_requests.SessionLoadProgress.name', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=211,
  serialized_end=273,
)


_PORTREQUEST = _descriptor.Descriptor(
  name='PortRequest',
  full_name='wait_room_requests.PortRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='wait_room_requests.PortRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=275,
  serialized_end=302,
)


_PORTRESPONSE = _descriptor.Descriptor(
  name='PortResponse',
  full_name='wait_room_requests.PortResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='port', full_name='wait_room_requests.PortResponse.port', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=304,
  serialized_end=332,
)

DESCRIPTOR.message_types_by_name['EndSession'] = _ENDSESSION
DESCRIPTOR.message_types_by_name['AskProgressRequest'] = _ASKPROGRESSREQUEST
DESCRIPTOR.message_types_by_name['RegisterRequest'] = _REGISTERREQUEST
DESCRIPTOR.message_types_by_name['RegisterResponse'] = _REGISTERRESPONSE
DESCRIPTOR.message_types_by_name['SessionLoadProgress'] = _SESSIONLOADPROGRESS
DESCRIPTOR.message_types_by_name['PortRequest'] = _PORTREQUEST
DESCRIPTOR.message_types_by_name['PortResponse'] = _PORTRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EndSession = _reflection.GeneratedProtocolMessageType('EndSession', (_message.Message,), {
  'DESCRIPTOR' : _ENDSESSION,
  '__module__' : 'wait_room_requests_pb2'
  # @@protoc_insertion_point(class_scope:wait_room_requests.EndSession)
  })
_sym_db.RegisterMessage(EndSession)

AskProgressRequest = _reflection.GeneratedProtocolMessageType('AskProgressRequest', (_message.Message,), {
  'DESCRIPTOR' : _ASKPROGRESSREQUEST,
  '__module__' : 'wait_room_requests_pb2'
  # @@protoc_insertion_point(class_scope:wait_room_requests.AskProgressRequest)
  })
_sym_db.RegisterMessage(AskProgressRequest)

RegisterRequest = _reflection.GeneratedProtocolMessageType('RegisterRequest', (_message.Message,), {
  'DESCRIPTOR' : _REGISTERREQUEST,
  '__module__' : 'wait_room_requests_pb2'
  # @@protoc_insertion_point(class_scope:wait_room_requests.RegisterRequest)
  })
_sym_db.RegisterMessage(RegisterRequest)

RegisterResponse = _reflection.GeneratedProtocolMessageType('RegisterResponse', (_message.Message,), {
  'DESCRIPTOR' : _REGISTERRESPONSE,
  '__module__' : 'wait_room_requests_pb2'
  # @@protoc_insertion_point(class_scope:wait_room_requests.RegisterResponse)
  })
_sym_db.RegisterMessage(RegisterResponse)

SessionLoadProgress = _reflection.GeneratedProtocolMessageType('SessionLoadProgress', (_message.Message,), {
  'DESCRIPTOR' : _SESSIONLOADPROGRESS,
  '__module__' : 'wait_room_requests_pb2'
  # @@protoc_insertion_point(class_scope:wait_room_requests.SessionLoadProgress)
  })
_sym_db.RegisterMessage(SessionLoadProgress)

PortRequest = _reflection.GeneratedProtocolMessageType('PortRequest', (_message.Message,), {
  'DESCRIPTOR' : _PORTREQUEST,
  '__module__' : 'wait_room_requests_pb2'
  # @@protoc_insertion_point(class_scope:wait_room_requests.PortRequest)
  })
_sym_db.RegisterMessage(PortRequest)

PortResponse = _reflection.GeneratedProtocolMessageType('PortResponse', (_message.Message,), {
  'DESCRIPTOR' : _PORTRESPONSE,
  '__module__' : 'wait_room_requests_pb2'
  # @@protoc_insertion_point(class_scope:wait_room_requests.PortResponse)
  })
_sym_db.RegisterMessage(PortResponse)



_WAITROOMREQTESTS = _descriptor.ServiceDescriptor(
  name='WaitRoomReqtests',
  full_name='wait_room_requests.WaitRoomReqtests',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=335,
  serialized_end=704,
  methods=[
  _descriptor.MethodDescriptor(
    name='AskProgress',
    full_name='wait_room_requests.WaitRoomReqtests.AskProgress',
    index=0,
    containing_service=None,
    input_type=_ASKPROGRESSREQUEST,
    output_type=_SESSIONLOADPROGRESS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Register',
    full_name='wait_room_requests.WaitRoomReqtests.Register',
    index=1,
    containing_service=None,
    input_type=_REGISTERREQUEST,
    output_type=_REGISTERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='AskPlayPort',
    full_name='wait_room_requests.WaitRoomReqtests.AskPlayPort',
    index=2,
    containing_service=None,
    input_type=_PORTREQUEST,
    output_type=_PORTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ReturnRoom',
    full_name='wait_room_requests.WaitRoomReqtests.ReturnRoom',
    index=3,
    containing_service=None,
    input_type=_ENDSESSION,
    output_type=_ENDSESSION,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_WAITROOMREQTESTS)

DESCRIPTOR.services_by_name['WaitRoomReqtests'] = _WAITROOMREQTESTS

# @@protoc_insertion_point(module_scope)