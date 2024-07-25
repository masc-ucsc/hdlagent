from typing import Set

from botocore.session import Session

DEPRECATED_SERVICE_NAMES: Set[str] = ...

def generate_docs(root_dir: str, session: Session) -> None: ...
