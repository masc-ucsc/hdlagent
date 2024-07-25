from concurrent.futures import Future
from datetime import datetime
from enum import IntEnum
from typing import Any, Callable, List, Optional, Sequence, Tuple, Type, TypeVar

from awscrt import NativeResource as NativeResource
from awscrt.http import HttpProxyOptions
from awscrt.http import HttpRequest as HttpRequest
from awscrt.io import ClientBootstrap as ClientBootstrap
from awscrt.io import ClientTlsContext

_R = TypeVar("_R")

class AwsCredentials(NativeResource):
    def __init__(
        self,
        access_key_id: str,
        secret_access_key: str,
        session_token: Optional[str] = ...,
        expiration: Optional[datetime] = ...,
    ) -> None: ...
    @property
    def access_key_id(self) -> str: ...
    @property
    def secret_access_key(self) -> str: ...
    @property
    def session_token(self) -> str: ...
    @property
    def expiration(self) -> Optional[datetime]: ...
    def __deepcopy__(self: _R, memo: Any) -> _R: ...

class AwsCredentialsProviderBase(NativeResource): ...

class AwsCredentialsProvider(AwsCredentialsProviderBase):
    def __init__(self, binding: Any) -> None: ...
    @classmethod
    def new_default_chain(
        cls: Type[_R], client_bootstrap: Optional[ClientBootstrap] = ...
    ) -> _R: ...
    @classmethod
    def new_static(
        cls: Type[_R],
        access_key_id: str,
        secret_access_key: str,
        session_token: Optional[str] = ...,
    ) -> _R: ...
    @classmethod
    def new_profile(
        cls: Type[_R],
        client_bootstrap: Optional[ClientBootstrap] = ...,
        profile_name: Optional[str] = ...,
        config_filepath: Optional[str] = ...,
        credentials_filepath: Optional[str] = ...,
    ) -> _R: ...
    @classmethod
    def new_process(cls: Type[_R], profile_to_use: Optional[str] = ...) -> _R: ...
    @classmethod
    def new_environment(cls: Type[_R]) -> _R: ...
    @classmethod
    def new_chain(cls: Type[_R], providers: List[AwsCredentialsProvider]) -> _R: ...
    @classmethod
    def new_delegate(cls: Type[_R], get_credentials: Callable[[], AwsCredentials]) -> _R: ...
    @classmethod
    def new_cognito(
        cls: Type[_R],
        *,
        endpoint: str,
        identity: str,
        tls_ctx: ClientTlsContext,
        logins: Optional[Sequence[Tuple[str, str]]] = ...,
        custom_role_arn: Optional[str] = ...,
        client_bootstrap: Optional[ClientBootstrap] = ...,
        http_proxy_options: Optional[HttpProxyOptions] = ...,
    ) -> _R: ...
    @classmethod
    def new_x509(
        cls: Type[_R],
        *,
        endpoint: str,
        thing_name: str,
        role_alias: str,
        tls_ctx: ClientTlsContext,
        client_bootstrap: Optional[ClientBootstrap] = ...,
        http_proxy_options: Optional[HttpProxyOptions] = ...,
    ) -> _R: ...
    def get_credentials(self) -> Future[AwsCredentials]: ...

class AwsSigningAlgorithm(IntEnum):
    V4: int
    V4_ASYMMETRIC: int
    V4_S3EXPRESS: int

class AwsSignatureType(IntEnum):
    HTTP_REQUEST_HEADERS: int
    HTTP_REQUEST_QUERY_PARAMS: int

class AwsSignedBodyValue:
    EMPTY_SHA256: str
    UNSIGNED_PAYLOAD: str
    STREAMING_AWS4_HMAC_SHA256_PAYLOAD: str
    STREAMING_AWS4_HMAC_SHA256_EVENTS: str

class AwsSignedBodyHeaderType(IntEnum):
    NONE: int
    X_AMZ_CONTENT_SHA_256: int

class AwsSigningConfig(NativeResource):
    def __init__(
        self,
        algorithm: AwsSigningAlgorithm = ...,
        signature_type: AwsSignatureType = ...,
        credentials_provider: Optional[AwsCredentialsProvider] = ...,
        region: str = ...,
        service: str = ...,
        date: Optional[datetime] = ...,
        should_sign_header: Optional[Callable[[str], bool]] = ...,
        use_double_uri_encode: bool = ...,
        should_normalize_uri_path: bool = ...,
        signed_body_value: Optional[str] = ...,
        signed_body_header_type: AwsSignedBodyHeaderType = ...,
        expiration_in_seconds: Optional[int] = ...,
        omit_session_token: bool = ...,
    ) -> None: ...
    def replace(self: _R, **kwargs: Any) -> _R: ...
    @property
    def algorithm(self) -> AwsSigningAlgorithm: ...
    @property
    def signature_type(self) -> AwsSignatureType: ...
    @property
    def credentials_provider(self) -> AwsCredentialsProvider: ...
    @property
    def region(self) -> str: ...
    @property
    def service(self) -> str: ...
    @property
    def date(self) -> datetime: ...
    @property
    def should_sign_header(self) -> Optional[Callable[[str], bool]]: ...
    @property
    def use_double_uri_encode(self) -> bool: ...
    @property
    def should_normalize_uri_path(self) -> bool: ...
    @property
    def signed_body_value(self) -> Optional[str]: ...
    @property
    def signed_body_header_type(self) -> AwsSignedBodyHeaderType: ...
    @property
    def expiration_in_seconds(self) -> Optional[int]: ...
    @property
    def omit_session_token(self) -> bool: ...

def aws_sign_request(
    http_request: HttpRequest, signing_config: AwsSigningConfig
) -> Future[HttpRequest]: ...
