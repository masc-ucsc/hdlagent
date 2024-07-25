from typing import Any

from botocore.model import OperationModel, Shape

class SharedExampleDocumenter:
    def document_shared_example(
        self, example: Any, prefix: str, section: Any, operation_model: OperationModel
    ) -> None: ...
    def document_input(self, section: Any, example: Any, prefix: str, shape: Shape) -> None: ...
    def document_output(self, section: Any, example: Any, shape: Shape) -> None: ...

def document_shared_examples(
    section: Any, operation_model: OperationModel, example_prefix: str, shared_examples: Any
) -> None: ...
