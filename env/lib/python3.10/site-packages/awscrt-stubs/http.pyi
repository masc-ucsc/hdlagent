from concurrent.futures import Future
from enum import IntEnum
from typing import IO, Any, Callable, Iterator, List, Optional, Tuple, Type, TypeVar

from awscrt import NativeResource as NativeResource
from awscrt.io import ClientBootstrap as ClientBootstrap
from awscrt.io import InputStream as InputStream
from awscrt.io import SocketOptions as SocketOptions
from awscrt.io import TlsConnectionOptions as TlsConnectionOptions

_R = TypeVar("_R")

class HttpVersion(IntEnum):
    Unknown: int
    Http1_0: int
    Http1_1: int
    Http2: int

class HttpConnectionBase(NativeResource):
    def __init__(self) -> None: ...
    @property
    def shutdown_future(self) -> Future[None]: ...
    @property
    def version(self) -> str: ...
    def close(self) -> Future[None]: ...
    def is_open(self) -> bool: ...

class HttpClientConnection(HttpConnectionBase):
    @classmethod
    def new(
        cls: Type[_R],
        host_name: str,
        port: int,
        bootstrap: Optional[ClientBootstrap] = ...,
        socket_options: Optional[SocketOptions] = ...,
        tls_connection_options: Optional[TlsConnectionOptions] = ...,
        proxy_options: Optional[HttpProxyOptions] = ...,
    ) -> Future[_R]: ...
    @property
    def host_name(self) -> str: ...
    @property
    def port(self) -> int: ...
    def request(
        self,
        request: HttpRequest,
        on_response: Optional[Callable[[HttpClientStream, int, List[Tuple[str, str]]], None]] = ...,
        on_body: Optional[Callable[[HttpClientStream, bytes], None]] = ...,
    ) -> HttpClientStream: ...

class HttpStreamBase(NativeResource):
    def __init__(
        self,
        connection: HttpClientConnection,
        on_body: Optional[Callable[[HttpClientStream, bytes], None]] = ...,
    ) -> None: ...
    @property
    def connection(self) -> HttpClientConnection: ...
    @property
    def completion_future(self) -> Future[int]: ...

class HttpClientStream(HttpStreamBase):
    def __init__(
        self,
        connection: HttpClientConnection,
        request: HttpRequest,
        on_response: Optional[Callable[[HttpClientStream, int, List[Tuple[str, str]]], None]] = ...,
        on_body: Optional[Callable[[HttpClientStream, bytes], None]] = ...,
    ) -> None: ...
    @property
    def response_status_code(self) -> int: ...
    def activate(self) -> None: ...

class HttpMessageBase(NativeResource):
    def __init__(
        self, binding: Any, headers: HttpHeaders, body_stream: Optional[IO[Any]] = ...
    ) -> None: ...
    @property
    def headers(self) -> HttpHeaders: ...
    @property
    def body_stream(self) -> Optional[IO[Any]]: ...
    @body_stream.setter
    def body_stream(self, stream: IO[Any]) -> None: ...

class HttpRequest(HttpMessageBase):
    def __init__(
        self,
        method: str = ...,
        path: str = ...,
        headers: Optional[HttpHeaders] = ...,
        body_stream: Optional[IO[Any]] = ...,
    ) -> None: ...
    @property
    def method(self) -> str: ...
    @method.setter
    def method(self, method: str) -> None: ...
    @property
    def path(self) -> str: ...
    @path.setter
    def path(self, path: str) -> None: ...

class HttpHeaders(NativeResource):
    def __init__(self, name_value_pairs: Optional[List[Tuple[str, str]]] = ...) -> None: ...
    def add(self, name: str, value: str) -> None: ...
    def add_pairs(self, name_value_pairs: List[Tuple[str, str]]) -> None: ...
    def set(self, name: str, value: str) -> None: ...
    def get_values(self, name: str) -> Iterator[Tuple[str, str]]: ...
    def get(self, name: str, default: Optional[str] = ...) -> Optional[str]: ...
    def remove(self, name: str) -> None: ...
    def remove_value(self, name: str, value: str) -> None: ...
    def clear(self) -> None: ...
    def __iter__(self) -> Iterator[Tuple[str, str]]: ...

class HttpProxyConnectionType(IntEnum):
    Legacy: int
    Forwarding: int
    Tunneling: int

class HttpProxyAuthenticationType(IntEnum):
    Nothing: int
    Basic: int

class HttpProxyOptions:
    def __init__(
        self,
        host_name: str,
        port: int,
        tls_connection_options: Optional[TlsConnectionOptions] = ...,
        auth_type: HttpProxyAuthenticationType = ...,
        auth_username: Optional[str] = ...,
        auth_password: Optional[str] = ...,
        connection_type: Optional[HttpProxyConnectionType] = ...,
    ) -> None:
        self.host_name: str
        self.port: int
        self.tls_connection_options: Optional[TlsConnectionOptions]
        self.auth_type: HttpProxyAuthenticationType
        self.auth_username: Optional[str]
        self.auth_password: Optional[str]
        self.connection_type: HttpProxyConnectionType
