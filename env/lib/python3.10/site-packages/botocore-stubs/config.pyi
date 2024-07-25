import sys
from typing import Dict, Mapping, Optional, Tuple, TypeVar, Union

from botocore.compat import OrderedDict as OrderedDict
from botocore.endpoint import DEFAULT_TIMEOUT as DEFAULT_TIMEOUT
from botocore.endpoint import MAX_POOL_CONNECTIONS as MAX_POOL_CONNECTIONS
from botocore.exceptions import InvalidMaxRetryAttemptsError as InvalidMaxRetryAttemptsError
from botocore.exceptions import InvalidRetryConfigurationError as InvalidRetryConfigurationError
from botocore.exceptions import InvalidRetryModeError as InvalidRetryModeError
from botocore.exceptions import InvalidS3AddressingStyleError as InvalidS3AddressingStyleError

if sys.version_info >= (3, 9):
    from typing import Literal, TypedDict
else:
    from typing_extensions import Literal, TypedDict

class _RetryDict(TypedDict, total=False):
    total_max_attempts: int
    max_attempts: int
    mode: Literal["legacy", "standard", "adaptive"]

class _S3Dict(TypedDict, total=False):
    use_accelerate_endpoint: bool
    payload_signing_enabled: bool
    addressing_style: Literal["auto", "virtual", "path"]
    us_east_1_regional_endpoint: Literal["regional", "legacy"]

class _ProxiesConfigDict(TypedDict, total=False):
    proxy_ca_bundle: str
    proxy_client_cert: Union[str, Tuple[str, str]]
    proxy_use_forwarding_for_https: bool

_Config = TypeVar("_Config", bound="Config")

class Config:
    OPTION_DEFAULTS: OrderedDict[str, None]
    NON_LEGACY_OPTION_DEFAULTS: Dict[str, None]
    def __init__(
        self,
        region_name: Optional[str] = None,
        signature_version: Optional[str] = None,
        user_agent: Optional[str] = None,
        user_agent_extra: Optional[str] = None,
        connect_timeout: Optional[Union[float, int]] = 60,
        read_timeout: Optional[Union[float, int]] = 60,
        parameter_validation: Optional[bool] = True,
        max_pool_connections: Optional[int] = 10,
        proxies: Optional[Mapping[str, str]] = None,
        proxies_config: Optional[_ProxiesConfigDict] = None,
        s3: Optional[_S3Dict] = None,
        retries: Optional[_RetryDict] = None,
        client_cert: Optional[Union[str, Tuple[str, str]]] = None,
        inject_host_prefix: Optional[bool] = True,
        endpoint_discovery_enabled: Optional[bool] = None,
        use_dualstack_endpoint: Optional[bool] = None,
        use_fips_endpoint: Optional[bool] = None,
        defaults_mode: Optional[bool] = None,
        tcp_keepalive: Optional[bool] = False,
    ) -> None: ...
    def merge(self: _Config, other_config: _Config) -> _Config: ...
