from typing import Any

from botocore.client import BaseClient
from botocore.hooks import BaseEventHooks
from botocore.model import ServiceModel
from botocore.waiter import WaiterModel

class WaiterDocumenter:
    def __init__(
        self, client: BaseClient, service_waiter_model: WaiterModel, root_docs_path: str
    ) -> None: ...
    def document_waiters(self, section: Any) -> None: ...

def document_wait_method(
    section: Any,
    waiter_name: str,
    event_emitter: BaseEventHooks,
    service_model: ServiceModel,
    service_waiter_model: WaiterModel,
    include_signature: bool = ...,
) -> None: ...
