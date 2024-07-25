import sys
from types import TracebackType
from typing import Any, Mapping, Optional, Type, TypeVar

from botocore.awsrequest import AWSResponse as AWSResponse
from botocore.client import BaseClient
from botocore.exceptions import ParamValidationError as ParamValidationError
from botocore.exceptions import StubAssertionError as StubAssertionError
from botocore.exceptions import StubResponseError as StubResponseError
from botocore.exceptions import UnStubbedResponseError as UnStubbedResponseError
from botocore.validate import validate_parameters as validate_parameters

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

class _ANY:
    def __eq__(self, other: object) -> Literal[True]: ...
    def __ne__(self, other: object) -> Literal[False]: ...

ANY: _ANY

_R = TypeVar("_R")

class Stubber:
    def __init__(self, client: BaseClient) -> None:
        self.client: BaseClient = ...

    def __enter__(self: _R) -> _R: ...
    def __exit__(
        self,
        exception_type: Optional[Type[BaseException]],
        exception_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None: ...
    def activate(self) -> None: ...
    def deactivate(self) -> None: ...
    def add_response(
        self,
        method: str,
        service_response: Mapping[str, Any],
        expected_params: Optional[Mapping[str, Any]] = ...,
    ) -> None: ...
    def add_client_error(
        self,
        method: str,
        service_error_code: str = ...,
        service_message: str = ...,
        http_status_code: int = ...,
        service_error_meta: Optional[Mapping[str, Any]] = ...,
        expected_params: Optional[Mapping[str, Any]] = ...,
        response_meta: Optional[Mapping[str, Any]] = ...,
        modeled_fields: Optional[Mapping[str, Any]] = ...,
    ) -> None: ...
    def assert_no_pending_responses(self) -> None: ...
