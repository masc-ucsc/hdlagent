from concurrent.futures import Future
from dataclasses import dataclass
from enum import IntEnum
from threading import Event
from types import TracebackType
from typing import Any, Callable, List, Optional, Sequence, Tuple, Type

from awscrt import NativeResource as NativeResource
from awscrt.auth import AwsCredentialsProvider as AwsCredentialsProvider
from awscrt.auth import AwsSigningConfig
from awscrt.exceptions import AwsCrtError
from awscrt.http import HttpRequest as HttpRequest
from awscrt.io import ClientBootstrap as ClientBootstrap
from awscrt.io import TlsConnectionOptions

class CrossProcessLock(NativeResource):
    def __init__(self, lock_scope_name: str) -> None: ...
    def acquire(self) -> None: ...
    def __enter__(self) -> None: ...
    def release(self) -> None: ...
    def __exit__(
        self,
        exc_type: Optional[Type[Exception]],
        exc_value: Optional[Exception],
        exc_tb: Optional[TracebackType],
    ) -> None: ...

class S3RequestType(IntEnum):
    DEFAULT: int
    GET_OBJECT: int
    PUT_OBJECT: int

class S3RequestTlsMode(IntEnum):
    ENABLED: int
    DISABLED: int

class S3ChecksumAlgorithm(IntEnum):
    CRC32C: int
    CRC32: int
    SHA1: int
    SHA256: int

class S3ChecksumLocation(IntEnum):
    HEADER: int
    TRAILER: int

@dataclass
class S3ChecksumConfig:
    algorithm: Optional[S3ChecksumAlgorithm] = ...
    location: Optional[S3ChecksumLocation] = ...
    validate_response: bool = ...

class S3Client(NativeResource):
    shutdown_event: Event
    def __init__(
        self,
        *,
        bootstrap: Optional[ClientBootstrap] = ...,
        region: str,
        tls_mode: Optional[S3RequestTlsMode] = ...,
        signing_config: Optional[AwsSigningConfig] = ...,
        credential_provider: Optional[S3RequestTlsMode] = ...,
        tls_connection_options: Optional[TlsConnectionOptions] = ...,
        part_size: Optional[int] = ...,
        multipart_upload_threshold: Optional[int] = ...,
        throughput_target_gbps: Optional[float] = ...,
        enable_s3express: bool = ...,
        memory_limit: Optional[int] = ...,
        network_interface_names: Optional[Sequence[str]] = ...,
    ) -> None: ...
    def make_request(
        self,
        *,
        type: S3RequestType,
        request: HttpRequest,
        operation_name: Optional[str] = ...,
        signing_config: Optional[AwsSigningConfig] = ...,
        credential_provider: Optional[AwsCredentialsProvider] = ...,
        checksum_config: Optional[S3ChecksumConfig] = ...,
        part_size: Optional[int] = ...,
        multipart_upload_threshold: Optional[int] = ...,
        recv_filepath: Optional[str] = ...,
        send_filepath: Optional[str] = ...,
        on_headers: Optional[Callable[[int, List[Tuple[str, str]]], None]] = ...,
        on_body: Optional[Callable[[bytes, int], None]] = ...,
        on_done: Optional[
            Callable[
                [Optional[BaseException], Optional[List[Tuple[str, str]]], Optional[bytes]], None
            ]
        ] = ...,
        on_progress: Optional[Callable[[int], None]] = ...,
    ) -> S3Request: ...

class S3Request(NativeResource):
    shutdown_event: Event
    def __init__(
        self,
        *,
        client: S3Client,
        type: S3RequestType,
        request: HttpRequest,
        operation_name: Optional[str] = ...,
        signing_config: Optional[AwsSigningConfig] = ...,
        credential_provider: Optional[AwsCredentialsProvider] = ...,
        checksum_config: Optional[S3ChecksumConfig] = ...,
        part_size: Optional[int] = ...,
        multipart_upload_threshold: Optional[int] = ...,
        recv_filepath: Optional[str] = ...,
        send_filepath: Optional[str] = ...,
        on_headers: Optional[Callable[[int, List[Tuple[str, str]]], None]] = ...,
        on_body: Optional[Callable[[bytes, int], None]] = ...,
        on_done: Optional[
            Callable[
                [Optional[BaseException], Optional[List[Tuple[str, str]]], Optional[bytes]], None
            ]
        ] = ...,
        on_progress: Optional[Callable[[int], None]] = ...,
        region: Optional[str] = ...,
    ) -> None: ...
    @property
    def finished_future(self) -> Future[Optional[BaseException]]: ...
    def cancel(self) -> None: ...

class S3ResponseError(AwsCrtError):
    def __init__(
        self,
        *,
        code: int,
        name: str,
        message: str,
        status_code: Optional[List[Tuple[str, str]]] = ...,
        headers: Optional[List[Tuple[str, str]]] = ...,
        body: Optional[bytes] = ...,
        operation_name: Optional[str] = ...,
    ) -> None: ...

class _S3ClientCore:
    def __init__(
        self,
        bootstrap: ClientBootstrap,
        credential_provider: Optional[AwsCredentialsProvider] = ...,
        signing_config: Optional[AwsSigningConfig] = ...,
        tls_connection_options: Optional[TlsConnectionOptions] = ...,
    ) -> None: ...

class _S3RequestCore:
    def __init__(
        self,
        request: HttpRequest,
        finish_future: Future[Optional[BaseException]],
        shutdown_event: Event,
        signing_config: Optional[AwsSigningConfig] = ...,
        credential_provider: Optional[AwsCredentialsProvider] = ...,
        on_headers: Optional[Callable[[int, List[Tuple[str, str]]], None]] = ...,
        on_body: Optional[Callable[[bytes, int], None]] = ...,
        on_done: Optional[
            Callable[
                [Optional[BaseException], Optional[List[Tuple[str, str]]], Optional[bytes]], None
            ]
        ] = ...,
        on_progress: Optional[Callable[[int], None]] = ...,
    ) -> None: ...

def create_default_s3_signing_config(
    *, region: str, credential_provider: AwsCredentialsProvider, **kwargs: Any
) -> AwsSigningConfig: ...
def get_ec2_instance_type() -> str: ...
def is_optimized_for_system() -> bool: ...
def get_optimized_platforms() -> List[str]: ...
def get_recommended_throughput_target_gbps() -> Optional[float]: ...
