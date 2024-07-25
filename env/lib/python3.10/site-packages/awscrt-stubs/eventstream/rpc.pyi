import abc
from abc import ABC, abstractmethod
from concurrent.futures import Future
from enum import IntEnum
from typing import Any, Callable, Optional, Sequence

from awscrt import NativeResource
from awscrt.eventstream import Header
from awscrt.http import HttpClientConnection
from awscrt.io import ClientBootstrap, SocketOptions, TlsConnectionOptions

class MessageType(IntEnum):
    APPLICATION_MESSAGE: int
    APPLICATION_ERROR: int
    PING: int
    PING_RESPONSE: int
    CONNECT: int
    CONNECT_ACK: int
    PROTOCOL_ERROR: int
    INTERNAL_ERROR: int
    def __format__(self, format_spec: str) -> str: ...

class MessageFlag:
    NONE: int
    CONNECTION_ACCEPTED: int
    TERMINATE_STREAM: int
    def __format__(self, format_spec: str) -> str: ...

class ClientConnectionHandler(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def on_connection_setup(
        self,
        connection: Optional[HttpClientConnection],
        error: Optional[BaseException],
        **kwargs: Any,
    ) -> None: ...
    @abstractmethod
    def on_connection_shutdown(self, reason: Optional[BaseException], **kwargs: Any) -> None: ...
    @abstractmethod
    def on_protocol_message(
        self,
        headers: Sequence[Header],
        payload: bytes,
        message_type: MessageType,
        flags: int,
        **kwargs: Any,
    ) -> None: ...

class ClientConnection(NativeResource):
    def __init__(self, host_name: str, port: int, handler: ClientConnectionHandler) -> None:
        self.host_name: str
        self.port: int
        self.shutdown_future: Future[None]

    @classmethod
    def connect(
        cls,
        *,
        handler: ClientConnectionHandler,
        host_name: str,
        port: int,
        bootstrap: Optional[ClientBootstrap] = ...,
        socket_options: Optional[SocketOptions] = ...,
        tls_connection_options: Optional[TlsConnectionOptions] = ...,
    ) -> Future[Optional[BaseException]]: ...
    def close(self) -> Future[Optional[BaseException]]: ...
    def is_open(self) -> bool: ...
    def send_protocol_message(
        self,
        *,
        headers: Optional[Sequence[Header]] = ...,
        payload: Optional[bytes] = ...,
        message_type: MessageType,
        flags: Optional[int] = ...,
        on_flush: Optional[Callable[..., Any]] = ...,
    ) -> Future[Optional[BaseException]]: ...
    def new_stream(self, handler: ClientContinuationHandler) -> ClientContinuation: ...

class ClientContinuation(NativeResource):
    def __init__(self, handler: ClientConnectionHandler, connection: ClientConnection) -> None:
        self.connection: ClientConnection
        closed_future: Future[None]

    def activate(
        self,
        *,
        operation: str,
        headers: Optional[Sequence[Header]] = ...,
        payload: Optional[bytes] = ...,
        message_type: MessageType,
        flags: Optional[int] = ...,
        on_flush: Optional[Callable[..., Any]] = ...,
    ) -> Future[Optional[BaseException]]: ...
    def send_message(
        self,
        *,
        headers: Optional[Sequence[Header]] = ...,
        payload: Optional[bytes] = ...,
        message_type: MessageType,
        flags: Optional[int] = ...,
        on_flush: Optional[Callable[..., Any]] = ...,
    ) -> Future[Optional[BaseException]]: ...
    def is_closed(self) -> bool: ...

class ClientContinuationHandler(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def on_continuation_message(
        self,
        headers: Sequence[Header],
        payload: bytes,
        message_type: MessageType,
        flags: int,
        **kwargs: Any,
    ) -> None: ...
    @abstractmethod
    def on_continuation_closed(self, **kwargs: Any) -> None: ...
