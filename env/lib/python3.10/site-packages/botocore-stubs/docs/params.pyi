from typing import Any, Optional, Sequence

from botocore.docs.shape import ShapeDocumenter
from botocore.model import Shape

class BaseParamsDocumenter(ShapeDocumenter):
    def document_params(
        self,
        section: Any,
        shape: Shape,
        include: Optional[Sequence[str]] = ...,
        exclude: Optional[Sequence[str]] = ...,
    ) -> None: ...
    def document_recursive_shape(self, section: Any, shape: Shape, **kwargs: Any) -> None: ...
    def document_shape_default(
        self,
        section: Any,
        shape: Shape,
        history: Any,
        include: Optional[Sequence[str]] = ...,
        exclude: Optional[Sequence[str]] = ...,
        **kwargs: Any,
    ) -> None: ...
    def document_shape_type_list(
        self,
        section: Any,
        shape: Shape,
        history: Any,
        include: Optional[Sequence[str]] = ...,
        exclude: Optional[Sequence[str]] = ...,
        **kwargs: Any,
    ) -> None: ...
    def document_shape_type_map(
        self,
        section: Any,
        shape: Shape,
        history: Any,
        include: Optional[Sequence[str]] = ...,
        exclude: Optional[Sequence[str]] = ...,
        **kwargs: Any,
    ) -> None: ...
    def document_shape_type_structure(
        self,
        section: Any,
        shape: Shape,
        history: Any,
        include: Optional[Sequence[str]] = ...,
        exclude: Optional[Sequence[str]] = ...,
        name: Optional[str] = ...,
        **kwargs: Any,
    ) -> None: ...

class ResponseParamsDocumenter(BaseParamsDocumenter):
    EVENT_NAME: str = ...
    def document_shape_type_event_stream(
        self,
        section: Any,
        shape: Shape,
        history: Any,
        **kwargs: Any,
    ) -> None: ...

class RequestParamsDocumenter(BaseParamsDocumenter):
    EVENT_NAME: str = ...
    def document_shape_type_structure(  # type: ignore[override]
        self,
        section: Any,
        shape: Shape,
        history: Any,
        include: Optional[Sequence[str]] = ...,
        exclude: Optional[Sequence[str]] = ...,
        **kwargs: Any,
    ) -> None: ...
