from enum import IntEnum
from threading import Event
from typing import IO, Any, List, Optional, Type, TypeVar, Union

from awscrt import NativeResource as NativeResource

_R = TypeVar("_R")

class LogLevel(IntEnum):
    NoLogs: int
    Fatal: int
    Error: int
    Warn: int
    Info: int
    Debug: int
    Trace: int

def init_logging(log_level: int, file_name: str) -> None: ...

class EventLoopGroup(NativeResource):
    shutdown_event: Event
    def __init__(
        self, num_threads: Optional[int] = ..., cpu_group: Optional[int] = ...
    ) -> None: ...
    @staticmethod
    def get_or_create_static_default() -> EventLoopGroup: ...
    @staticmethod
    def release_static_default() -> None: ...

class HostResolverBase(NativeResource): ...

class DefaultHostResolver(HostResolverBase):
    def __init__(self, event_loop_group: EventLoopGroup, max_hosts: int = ...) -> None: ...
    @staticmethod
    def get_or_create_static_default() -> DefaultHostResolver: ...
    @staticmethod
    def release_static_default() -> None: ...

class ClientBootstrap(NativeResource):
    shutdown_event: Event
    def __init__(
        self, event_loop_group: EventLoopGroup, host_resolver: HostResolverBase
    ) -> None: ...
    @staticmethod
    def get_or_create_static_default() -> ClientBootstrap: ...
    @staticmethod
    def release_static_default() -> None: ...

class SocketDomain(IntEnum):
    IPv4: int
    IPv6: int
    Local: int

class SocketType(IntEnum):
    Stream: int
    DGram: int

class SocketOptions:
    domain: SocketDomain
    type: SocketType
    connect_timeout_ms: int
    keep_alive: bool
    keep_alive_interval_secs: int
    keep_alive_timeout_secs: int
    keep_alive_max_probes: int
    def __init__(self) -> None: ...

class TlsVersion(IntEnum):
    SSLv3: int
    TLSv1: int
    TLSv1_1: int
    TLSv1_2: int
    TLSv1_3: int
    DEFAULT: int

class TlsCipherPref(IntEnum):
    DEFAULT: int
    PQ_TLSv1_0_2021_05: int
    def is_supported(self) -> bool: ...

class TlsContextOptions:
    alpn_list: List[str]
    certificate_buffer: bytes
    pkcs12_filepath: str
    pkcs12_password: str
    private_key_buffer: bytes
    ca_dirpath: str
    ca_buffer: bytes
    def __init__(self) -> None:
        self.min_tls_ver: TlsVersion
        self.cipher_pref: TlsCipherPref
        self.verify_peer: bool

    @staticmethod
    def create_client_with_mtls_from_path(
        cert_filepath: str, pk_filepath: str
    ) -> TlsContextOptions: ...
    @staticmethod
    def create_client_with_mtls(cert_buffer: bytes, key_buffer: bytes) -> TlsContextOptions: ...
    @staticmethod
    def create_client_with_mtls_pkcs11(
        *,
        pkcs11_lib: Pkcs11Lib,
        user_pin: str,
        slot_id: Optional[int] = ...,
        token_label: Optional[str] = ...,
        private_key_label: Optional[str] = ...,
        cert_file_path: Optional[str] = ...,
        cert_file_contents: Optional[Union[str, bytes, bytearray]] = ...,
    ) -> TlsContextOptions: ...
    @staticmethod
    def create_client_with_mtls_pkcs12(
        pkcs12_filepath: str, pkcs12_password: str
    ) -> TlsContextOptions: ...
    @staticmethod
    def create_client_with_mtls_windows_cert_store_path(cert_path: str) -> TlsContextOptions: ...
    @staticmethod
    def create_server_from_path(cert_filepath: str, pk_filepath: str) -> TlsContextOptions: ...
    @staticmethod
    def create_server(cert_buffer: bytes, key_buffer: bytes) -> TlsContextOptions: ...
    @staticmethod
    def create_server_pkcs12(pkcs12_filepath: str, pkcs12_password: str) -> TlsContextOptions: ...
    def override_default_trust_store_from_path(
        self, ca_dirpath: Optional[str] = ..., ca_filepath: Optional[str] = ...
    ) -> None: ...
    def override_default_trust_store(self, rootca_buffer: bytes) -> None: ...

class ClientTlsContext(NativeResource):
    def __init__(self, options: TlsContextOptions) -> None: ...
    def new_connection_options(self) -> TlsContextOptions: ...

class TlsConnectionOptions(NativeResource):
    tls_ctx: ClientTlsContext
    def __init__(self, tls_ctx: ClientTlsContext) -> None: ...
    def set_alpn_list(self, alpn_list: List[str]) -> None: ...
    def set_server_name(self, server_name: str) -> None: ...

def is_alpn_available() -> bool: ...

class InputStream(NativeResource):
    def __init__(self, stream: IO[Any]) -> None: ...
    @classmethod
    def wrap(cls: Type[_R], stream: IO[Any], allow_none: bool = ...) -> _R: ...

class Pkcs11Lib(NativeResource):
    class InitializeFinalizeBehavior(IntEnum):
        DEFAULT: int
        OMIT: int
        STRICT: int

    def __init__(
        self, *, file: str, behavior: Optional[InitializeFinalizeBehavior] = ...
    ) -> None: ...
