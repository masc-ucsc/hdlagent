from typing import Any

class BaseRetryBackoff:
    def delay_amount(self, context: Any) -> float: ...

class BaseRetryableChecker:
    def is_retryable(self, context: Any) -> bool: ...
