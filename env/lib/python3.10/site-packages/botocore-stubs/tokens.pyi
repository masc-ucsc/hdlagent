import datetime
import logging
from typing import Any, Callable, Iterable, NamedTuple, Optional, Type

from botocore.session import Session
from botocore.utils import JSONFileCache

logger: logging.Logger

def create_token_resolver(session: Session) -> TokenProviderChain: ...

class FrozenAuthToken(NamedTuple):
    token: str
    expiration: Optional[datetime.datetime] = ...

class DeferredRefreshableToken:
    def __init__(
        self,
        method: Any,
        refresh_using: Callable[[], FrozenAuthToken],
        time_fetcher: Callable[[], datetime.datetime] = ...,
    ) -> None: ...
    def get_frozen_token(self) -> FrozenAuthToken: ...

class TokenProviderChain:
    def __init__(self, providers: Optional[Iterable[Any]] = ...) -> None: ...
    def load_token(self) -> DeferredRefreshableToken: ...

class SSOTokenProvider:
    METHOD: str = ...
    DEFAULT_CACHE_CLS: Type[JSONFileCache] = ...

    def __init__(
        self,
        session: Session,
        cache: Optional[JSONFileCache] = ...,
        time_fetcher: Callable[[], datetime.datetime] = ...,
        profile_name: Optional[str] = ...,
    ) -> None: ...
    def load_token(self) -> DeferredRefreshableToken: ...
