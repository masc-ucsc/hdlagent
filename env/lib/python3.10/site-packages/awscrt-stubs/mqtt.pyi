from concurrent.futures import Future
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Callable, Dict, Optional, Tuple, Union

from awscrt import NativeResource as NativeResource
from awscrt.exceptions import AwsCrtError
from awscrt.http import HttpProxyOptions as HttpProxyOptions
from awscrt.http import HttpRequest as HttpRequest
from awscrt.io import ClientBootstrap as ClientBootstrap
from awscrt.io import ClientTlsContext as ClientTlsContext
from awscrt.io import SocketOptions as SocketOptions
from awscrt.mqtt5 import QoS as Mqtt5QoS

class QoS(IntEnum):
    AT_MOST_ONCE: int
    AT_LEAST_ONCE: int
    EXACTLY_ONCE: int

    def to_mqtt5(self) -> Mqtt5QoS: ...

class ConnectReturnCode(IntEnum):
    ACCEPTED: int
    UNACCEPTABLE_PROTOCOL_VERSION: int
    IDENTIFIER_REJECTED: int
    SERVER_UNAVAILABLE: int
    BAD_USERNAME_OR_PASSWORD: int
    NOT_AUTHORIZED: int

class Will:
    def __init__(self, topic: str, qos: QoS, payload: bytes, retain: bool) -> None:
        self.topic: str
        self.qos: QoS
        self.payload: bytes
        self.retain: bool

@dataclass
class OnConnectionSuccessData:
    return_code: Optional[ConnectReturnCode] = ...
    session_present: bool = ...

@dataclass
class OnConnectionFailureData:
    error: Optional[AwsCrtError] = ...

@dataclass
class OnConnectionClosedData: ...

class Client(NativeResource):
    def __init__(
        self, bootstrap: Optional[ClientBootstrap] = ..., tls_ctx: Optional[ClientTlsContext] = ...
    ) -> None:
        self.tls_ctx: ClientTlsContext

@dataclass
class OperationStatisticsData:
    incomplete_operation_count: int = ...
    incomplete_operation_size: int = ...
    unacked_operation_count: int = ...
    unacked_operation_size: int = ...

class Connection(NativeResource):
    def __init__(
        self,
        client: Client,
        host_name: str,
        port: int,
        client_id: str,
        clean_session: bool = ...,
        on_connection_interrupted: Optional[Callable[[Connection, AwsCrtError], None]] = ...,
        on_connection_resumed: Optional[
            Callable[[Connection, ConnectReturnCode, bool], None]
        ] = ...,
        reconnect_min_timeout_secs: int = ...,
        reconnect_max_timeout_secs: int = ...,
        keep_alive_secs: int = ...,
        ping_timeout_ms: int = ...,
        protocol_operation_timeout_ms: int = ...,
        will: Optional[Will] = ...,
        username: Optional[str] = ...,
        password: Optional[str] = ...,
        socket_options: Optional[SocketOptions] = ...,
        use_websockets: bool = ...,
        websocket_proxy_options: Optional[HttpProxyOptions] = ...,
        websocket_handshake_transform: Optional[
            Callable[[WebsocketHandshakeTransformArgs], None]
        ] = ...,
        proxy_options: Optional[HttpProxyOptions] = ...,
        on_connection_success: Optional[Callable[[Connection], OnConnectionSuccessData]] = ...,
        on_connection_failure: Optional[Callable[[Connection], OnConnectionFailureData]] = ...,
        on_connection_closed: Optional[Callable[[Connection], OnConnectionClosedData]] = ...,
    ) -> None:
        self.client: Client
        self.client_id: str
        self.host_name: str
        self.port: int
        self.clean_session: bool
        self.reconnect_min_timeout_secs: int
        self.reconnect_max_timeout_secs: int
        self.keep_alive_secs: int
        self.ping_timeout_ms: int
        self.protocol_operation_timeout_ms: int
        self.will: Will
        self.username: str
        self.password: str
        self.socket_options: Optional[SocketOptions]
        self.proxy_options: Optional[HttpProxyOptions]

    def connect(self) -> Future[Optional[BaseException]]: ...
    def reconnect(self) -> Future[Optional[BaseException]]: ...
    def disconnect(self) -> Future[Optional[BaseException]]: ...
    def subscribe(
        self,
        topic: str,
        qos: QoS,
        callback: Optional[Callable[[str, bytes, bool, QoS, bool], None]] = ...,
    ) -> Tuple[Future[Optional[Dict[str, Any]]], int]: ...
    def on_message(self, callback: Callable[[str, bytes, bool, QoS, bool], None]) -> None: ...
    def unsubscribe(self, topic: str) -> Tuple[Future[Optional[Dict[str, Any]]], int]: ...
    def resubscribe_existing_topics(self) -> Tuple[Future[Optional[Dict[str, Any]]], int]: ...
    def publish(
        self, topic: str, payload: Union[str, bytes, bytearray], qos: QoS, retain: bool = ...
    ) -> Tuple[Future[Optional[Dict[str, Any]]], int]: ...
    def get_stats(self) -> OperationStatisticsData: ...

class WebsocketHandshakeTransformArgs:
    def __init__(
        self,
        mqtt_connection: Connection,
        http_request: HttpRequest,
        done_future: Future[Optional[BaseException]],
    ) -> None:
        self.mqtt_connection: Connection
        self.http_request: HttpRequest

    def set_done(self, exception: Optional[BaseException] = ...) -> None: ...

class SubscribeError(Exception): ...
