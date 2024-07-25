from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Callable, Optional, Sequence, Tuple, Union

from awscrt import NativeResource as NativeResource
from awscrt.http import HttpProxyOptions as HttpProxyOptions
from awscrt.http import HttpRequest as HttpRequest
from awscrt.io import ClientBootstrap as ClientBootstrap
from awscrt.io import SocketOptions as SocketOptions
from awscrt.io import TlsConnectionOptions as TlsConnectionOptions

class Opcode(IntEnum):
    CONTINUATION: int
    TEXT: int
    BINARY: int
    CLOSE: int
    PING: int
    PONG: int
    def is_data_frame(self) -> bool: ...

MAX_PAYLOAD_LENGTH: int

@dataclass
class OnConnectionSetupData:
    exception: Optional[Exception] = ...
    websocket: Optional["WebSocket"] = ...
    handshake_response_status: Optional[int] = ...
    handshake_response_headers: Optional[Sequence[Tuple[str, str]]] = ...
    handshake_response_body: Optional[bytes] = ...

@dataclass
class OnConnectionShutdownData:
    exception: Optional[Exception] = ...

@dataclass
class IncomingFrame:
    opcode: Opcode
    payload_length: int
    fin: bool
    def is_data_frame(self) -> bool: ...

@dataclass
class OnIncomingFrameBeginData:
    frame: IncomingFrame

@dataclass
class OnIncomingFramePayloadData:
    frame: IncomingFrame
    data: bytes

@dataclass
class OnIncomingFrameCompleteData:
    frame: IncomingFrame
    exception: Optional[Exception] = ...

@dataclass
class OnSendFrameCompleteData:
    exception: Optional[Exception] = ...

class WebSocket(NativeResource):
    def __init__(self, binding: Any) -> None: ...
    def close(self) -> None: ...
    def send_frame(
        self,
        opcode: Opcode,
        payload: Optional[Union[str, bytes, bytearray, memoryview]] = ...,
        *,
        fin: bool = ...,
        on_complete: Optional[Callable[[OnSendFrameCompleteData], None]] = ...,
    ) -> None: ...
    def increment_read_window(self, size: int) -> None: ...

class _WebSocketCore(NativeResource):
    def __init__(
        self,
        on_connection_setup: Callable[[OnConnectionSetupData], None],
        on_connection_shutdown: Optional[Callable[[OnConnectionShutdownData], None]],
        on_incoming_frame_begin: Optional[Callable[[OnIncomingFrameBeginData], None]],
        on_incoming_frame_payload: Optional[Callable[[OnIncomingFramePayloadData], None]],
        on_incoming_frame_complete: Optional[Callable[[OnIncomingFrameCompleteData], None]],
    ) -> None: ...

def connect(
    *,
    host: str,
    port: Optional[int] = ...,
    handshake_request: HttpRequest,
    bootstrap: Optional[ClientBootstrap] = ...,
    socket_options: Optional[SocketOptions] = ...,
    tls_connection_options: Optional[TlsConnectionOptions] = ...,
    proxy_options: Optional[HttpProxyOptions] = ...,
    manage_read_window: bool = ...,
    initial_read_window: Optional[int] = ...,
    on_connection_setup: Callable[[OnConnectionSetupData], None],
    on_connection_shutdown: Optional[Callable[[OnConnectionShutdownData], None]] = ...,
    on_incoming_frame_begin: Optional[Callable[[OnIncomingFrameBeginData], None]] = ...,
    on_incoming_frame_payload: Optional[Callable[[OnIncomingFramePayloadData], None]] = ...,
    on_incoming_frame_complete: Optional[Callable[[OnIncomingFrameCompleteData], None]] = ...,
) -> None: ...
def create_handshake_request(*, host: str, path: str = ...) -> HttpRequest: ...
