from typing import Any, List, NamedTuple, Optional, Type, TypeVar

from botocore.config import Config

_R = TypeVar("_R")

def sanitize_user_agent_string_component(raw_str: str, allow_hash: bool) -> str: ...

class UserAgentComponent(NamedTuple):
    prefix: str
    name: str
    value: Optional[str] = ...

    def to_string(self) -> str: ...

class RawStringUserAgentComponent:
    def __init__(self, value: str) -> None: ...
    def to_string(self) -> str: ...

def modify_components(components: List[Any]) -> List[Any]: ...

class UserAgentString:
    def __init__(
        self,
        platform_name: str,
        platform_version: str,
        platform_machine: str,
        python_version: str,
        python_implementation: str,
        execution_env: str,
        crt_version: Optional[str] = ...,
    ) -> None: ...
    @classmethod
    def from_environment(cls: Type[_R]) -> _R: ...
    def set_session_config(
        self: _R,
        session_user_agent_name: str,
        session_user_agent_version: str,
        session_user_agent_extra: str,
    ) -> _R: ...
    def with_client_config(self: _R, client_config: Config) -> _R: ...
    def to_string(self) -> str: ...
