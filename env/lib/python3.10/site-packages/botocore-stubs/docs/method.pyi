from typing import Any, Dict, Optional, Sequence

from botocore.hooks import BaseEventHooks
from botocore.model import OperationModel

AWS_DOC_BASE: str = ...

def get_instance_public_methods(instance: Any) -> Dict[str, Any]: ...
def document_model_driven_signature(
    section: Any,
    name: str,
    operation_model: OperationModel,
    include: Optional[Sequence[str]] = ...,
    exclude: Optional[Sequence[str]] = ...,
) -> None: ...
def document_custom_signature(
    section: Any,
    name: str,
    method: Any,
    include: Optional[Sequence[str]] = ...,
    exclude: Optional[Sequence[str]] = ...,
) -> None: ...
def document_custom_method(section: Any, method_name: str, method: Any) -> None: ...
def document_model_driven_method(
    section: Any,
    method_name: str,
    operation_model: OperationModel,
    event_emitter: BaseEventHooks,
    method_description: Optional[str] = ...,
    example_prefix: Optional[str] = ...,
    include_input: Optional[Dict[str, Any]] = ...,
    include_output: Optional[Dict[str, Any]] = ...,
    exclude_input: Optional[Sequence[str]] = ...,
    exclude_output: Optional[Sequence[str]] = ...,
    document_output: bool = ...,
    include_signature: bool = ...,
) -> None: ...
