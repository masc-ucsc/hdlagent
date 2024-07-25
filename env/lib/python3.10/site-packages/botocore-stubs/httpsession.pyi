from logging import Logger
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union

from botocore.awsrequest import AWSPreparedRequest, AWSRequest, AWSResponse
from botocore.compat import IPV6_ADDRZ_RE as IPV6_ADDRZ_RE
from botocore.compat import filter_ssl_warnings as filter_ssl_warnings
from botocore.compat import urlparse as urlparse
from botocore.exceptions import ConnectionClosedError as ConnectionClosedError
from botocore.exceptions import ConnectTimeoutError as ConnectTimeoutError
from botocore.exceptions import EndpointConnectionError as EndpointConnectionError
from botocore.exceptions import HTTPClientError as HTTPClientError
from botocore.exceptions import InvalidProxiesConfigError as InvalidProxiesConfigError
from botocore.exceptions import ProxyConnectionError as ProxyConnectionError
from botocore.exceptions import ReadTimeoutError as ReadTimeoutError
from botocore.exceptions import SSLError as SSLError

logger: Logger = ...

DEFAULT_TIMEOUT: int = ...
MAX_POOL_CONNECTIONS: int = ...
DEFAULT_CA_BUNDLE: str = ...
DEFAULT_CIPHERS: Optional[str] = ...

def where() -> str: ...
def get_cert_path(verify: bool) -> Optional[str]: ...
def create_urllib3_context(
    ssl_version: Optional[int] = ...,
    cert_reqs: Optional[bool] = ...,
    options: Optional[int] = ...,
    ciphers: Optional[str] = ...,
) -> Any: ...
def ensure_boolean(val: Any) -> bool: ...
def mask_proxy_url(proxy_url: str) -> str: ...

class ProxyConfiguration:
    def __init__(
        self,
        proxies: Optional[Mapping[str, Any]] = ...,
        proxies_settings: Optional[Mapping[str, Any]] = ...,
    ) -> None: ...
    def proxy_url_for(self, url: str) -> str: ...
    def proxy_headers_for(self, proxy_url: str) -> Dict[str, Any]: ...
    @property
    def settings(self) -> Dict[str, Any]: ...

class URLLib3Session:
    def __init__(
        self,
        verify: bool = ...,
        proxies: Optional[Mapping[str, Any]] = ...,
        timeout: Optional[int] = ...,
        max_pool_connections: int = ...,
        socket_options: Optional[List[str]] = ...,
        client_cert: Optional[Union[str, Tuple[str, str]]] = ...,
        proxies_config: Optional[Mapping[str, Any]] = ...,
    ) -> None: ...
    def close(self) -> None: ...
    def send(self, request: Union[AWSRequest, AWSPreparedRequest]) -> AWSResponse: ...
