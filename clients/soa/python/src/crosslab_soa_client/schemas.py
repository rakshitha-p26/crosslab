# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = authentication_message_from_dict(json.loads(json_string))
#     result = close_peerconnection_message_from_dict(json.loads(json_string))
#     result = command_message_from_dict(json.loads(json_string))
#     result = create_peerconnection_message_from_dict(json.loads(json_string))
#     result = message_from_dict(json.loads(json_string))
#     result = signaling_message_from_dict(json.loads(json_string))

from enum import Enum
from typing import Optional, Any, List, Dict, TypeVar, Type, Callable, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


class AuthenticationMessageMessageType(Enum):
    AUTHENTICATE = "authenticate"


class AuthenticationMessage:
    message_type: AuthenticationMessageMessageType
    authenticated: Optional[bool]
    device_url: str
    token: Optional[str]

    def __init__(self, message_type: AuthenticationMessageMessageType, authenticated: Optional[bool], device_url: str, token: Optional[str]) -> None:
        self.message_type = message_type
        self.authenticated = authenticated
        self.device_url = device_url
        self.token = token

    @staticmethod
    def from_dict(obj: Any) -> 'AuthenticationMessage':
        assert isinstance(obj, dict)
        message_type = AuthenticationMessageMessageType(obj.get("messageType"))
        authenticated = from_union([from_bool, from_none], obj.get("authenticated"))
        device_url = from_str(obj.get("deviceUrl"))
        token = from_union([from_str, from_none], obj.get("token"))
        return AuthenticationMessage(message_type, authenticated, device_url, token)

    def to_dict(self) -> dict:
        result: dict = {}
        result["messageType"] = to_enum(AuthenticationMessageMessageType, self.message_type)
        result["authenticated"] = from_union([from_bool, from_none], self.authenticated)
        result["deviceUrl"] = from_str(self.device_url)
        result["token"] = from_union([from_str, from_none], self.token)
        return result


class ClosePeerconnectionMessageCommand(Enum):
    CLOSE_PEERCONNECTION = "closePeerconnection"


class ClosePeerconnectionMessageMessageType(Enum):
    COMMAND = "command"


class ClosePeerconnectionMessage:
    message_type: ClosePeerconnectionMessageMessageType
    command: ClosePeerconnectionMessageCommand
    connection_url: str

    def __init__(self, message_type: ClosePeerconnectionMessageMessageType, command: ClosePeerconnectionMessageCommand, connection_url: str) -> None:
        self.message_type = message_type
        self.command = command
        self.connection_url = connection_url

    @staticmethod
    def from_dict(obj: Any) -> 'ClosePeerconnectionMessage':
        assert isinstance(obj, dict)
        message_type = ClosePeerconnectionMessageMessageType(obj.get("messageType"))
        command = ClosePeerconnectionMessageCommand(obj.get("command"))
        connection_url = from_str(obj.get("connectionUrl"))
        return ClosePeerconnectionMessage(message_type, command, connection_url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["messageType"] = to_enum(ClosePeerconnectionMessageMessageType, self.message_type)
        result["command"] = to_enum(ClosePeerconnectionMessageCommand, self.command)
        result["connectionUrl"] = from_str(self.connection_url)
        return result


class CommandMessage:
    message_type: ClosePeerconnectionMessageMessageType
    command: str

    def __init__(self, message_type: ClosePeerconnectionMessageMessageType, command: str) -> None:
        self.message_type = message_type
        self.command = command

    @staticmethod
    def from_dict(obj: Any) -> 'CommandMessage':
        assert isinstance(obj, dict)
        message_type = ClosePeerconnectionMessageMessageType(obj.get("messageType"))
        command = from_str(obj.get("command"))
        return CommandMessage(message_type, command)

    def to_dict(self) -> dict:
        result: dict = {}
        result["messageType"] = to_enum(ClosePeerconnectionMessageMessageType, self.message_type)
        result["command"] = from_str(self.command)
        return result


class CreatePeerconnectionMessageCommand(Enum):
    CREATE_PEERCONNECTION = "createPeerconnection"


class ConnectionType(Enum):
    WEBRTC = "webrtc"
    WEBSOCKET = "websocket"


class ServiceConfig:
    remote_service_id: Optional[str]
    service_id: Optional[str]
    service_type: Optional[str]

    def __init__(self, remote_service_id: Optional[str], service_id: Optional[str], service_type: Optional[str]) -> None:
        self.remote_service_id = remote_service_id
        self.service_id = service_id
        self.service_type = service_type

    @staticmethod
    def from_dict(obj: Any) -> 'ServiceConfig':
        assert isinstance(obj, dict)
        remote_service_id = from_union([from_str, from_none], obj.get("remoteServiceId"))
        service_id = from_union([from_str, from_none], obj.get("serviceId"))
        service_type = from_union([from_str, from_none], obj.get("serviceType"))
        return ServiceConfig(remote_service_id, service_id, service_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["remoteServiceId"] = from_union([from_str, from_none], self.remote_service_id)
        result["serviceId"] = from_union([from_str, from_none], self.service_id)
        result["serviceType"] = from_union([from_str, from_none], self.service_type)
        return result


class CreatePeerconnectionMessage:
    message_type: ClosePeerconnectionMessageMessageType
    command: CreatePeerconnectionMessageCommand
    connection_type: ConnectionType
    connection_url: str
    services: List[ServiceConfig]
    tiebreaker: bool

    def __init__(self, message_type: ClosePeerconnectionMessageMessageType, command: CreatePeerconnectionMessageCommand, connection_type: ConnectionType, connection_url: str, services: List[ServiceConfig], tiebreaker: bool) -> None:
        self.message_type = message_type
        self.command = command
        self.connection_type = connection_type
        self.connection_url = connection_url
        self.services = services
        self.tiebreaker = tiebreaker

    @staticmethod
    def from_dict(obj: Any) -> 'CreatePeerconnectionMessage':
        assert isinstance(obj, dict)
        message_type = ClosePeerconnectionMessageMessageType(obj.get("messageType"))
        command = CreatePeerconnectionMessageCommand(obj.get("command"))
        connection_type = ConnectionType(obj.get("connectionType"))
        connection_url = from_str(obj.get("connectionUrl"))
        services = from_list(ServiceConfig.from_dict, obj.get("services"))
        tiebreaker = from_bool(obj.get("tiebreaker"))
        return CreatePeerconnectionMessage(message_type, command, connection_type, connection_url, services, tiebreaker)

    def to_dict(self) -> dict:
        result: dict = {}
        result["messageType"] = to_enum(ClosePeerconnectionMessageMessageType, self.message_type)
        result["command"] = to_enum(CreatePeerconnectionMessageCommand, self.command)
        result["connectionType"] = to_enum(ConnectionType, self.connection_type)
        result["connectionUrl"] = from_str(self.connection_url)
        result["services"] = from_list(lambda x: to_class(ServiceConfig, x), self.services)
        result["tiebreaker"] = from_bool(self.tiebreaker)
        return result


class Message:
    message_type: str

    def __init__(self, message_type: str) -> None:
        self.message_type = message_type

    @staticmethod
    def from_dict(obj: Any) -> 'Message':
        assert isinstance(obj, dict)
        message_type = from_str(obj.get("messageType"))
        return Message(message_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["messageType"] = from_str(self.message_type)
        return result


class SignalingMessageMessageType(Enum):
    SIGNALING = "signaling"


class SignalingType(Enum):
    ANSWER = "answer"
    CANDIDATE = "candidate"
    OFFER = "offer"


class SignalingMessage:
    message_type: SignalingMessageMessageType
    connection_url: str
    content: Dict[str, Any]
    signaling_type: SignalingType

    def __init__(self, message_type: SignalingMessageMessageType, connection_url: str, content: Dict[str, Any], signaling_type: SignalingType) -> None:
        self.message_type = message_type
        self.connection_url = connection_url
        self.content = content
        self.signaling_type = signaling_type

    @staticmethod
    def from_dict(obj: Any) -> 'SignalingMessage':
        assert isinstance(obj, dict)
        message_type = SignalingMessageMessageType(obj.get("messageType"))
        connection_url = from_str(obj.get("connectionUrl"))
        content = from_dict(lambda x: x, obj.get("content"))
        signaling_type = SignalingType(obj.get("signalingType"))
        return SignalingMessage(message_type, connection_url, content, signaling_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["messageType"] = to_enum(SignalingMessageMessageType, self.message_type)
        result["connectionUrl"] = from_str(self.connection_url)
        result["content"] = from_dict(lambda x: x, self.content)
        result["signalingType"] = to_enum(SignalingType, self.signaling_type)
        return result


def authentication_message_from_dict(s: Any) -> AuthenticationMessage:
    return AuthenticationMessage.from_dict(s)


def authentication_message_to_dict(x: AuthenticationMessage) -> Any:
    return to_class(AuthenticationMessage, x)


def close_peerconnection_message_from_dict(s: Any) -> ClosePeerconnectionMessage:
    return ClosePeerconnectionMessage.from_dict(s)


def close_peerconnection_message_to_dict(x: ClosePeerconnectionMessage) -> Any:
    return to_class(ClosePeerconnectionMessage, x)


def command_message_from_dict(s: Any) -> CommandMessage:
    return CommandMessage.from_dict(s)


def command_message_to_dict(x: CommandMessage) -> Any:
    return to_class(CommandMessage, x)


def create_peerconnection_message_from_dict(s: Any) -> CreatePeerconnectionMessage:
    return CreatePeerconnectionMessage.from_dict(s)


def create_peerconnection_message_to_dict(x: CreatePeerconnectionMessage) -> Any:
    return to_class(CreatePeerconnectionMessage, x)


def message_from_dict(s: Any) -> Message:
    return Message.from_dict(s)


def message_to_dict(x: Message) -> Any:
    return to_class(Message, x)


def signaling_message_from_dict(s: Any) -> SignalingMessage:
    return SignalingMessage.from_dict(s)


def signaling_message_to_dict(x: SignalingMessage) -> Any:
    return to_class(SignalingMessage, x)


class PartialSignalingMessage:
    content: Dict[str, Any]
    signaling_type: SignalingType

    def __init__(self, content: Dict[str, Any], signaling_type: SignalingType) -> None:
        self.content = content
        self.signaling_type = signaling_type

    @staticmethod
    def from_dict(obj: Any) -> 'PartialSignalingMessage':
        assert isinstance(obj, dict)
        content = from_dict(lambda x: x, obj.get("content"))
        signaling_type = SignalingType(obj.get("signalingType"))
        return PartialSignalingMessage(content, signaling_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["content"] = from_dict(lambda x: x, self.content)
        result["signalingType"] = to_enum(SignalingType, self.signaling_type)
        return result
