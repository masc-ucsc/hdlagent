import io
from gzip import GzipFile as GzipFile
from gzip import compress as gzip_compress
from logging import Logger
from typing import Any, Callable, Dict, Mapping

from botocore.compat import urlencode as urlencode
from botocore.config import Config
from botocore.model import OperationModel
from botocore.utils import determine_content_length as determine_content_length

logger: Logger = ...

def maybe_compress_request(
    config: Config, request_dict: Mapping[str, Any], operation_model: OperationModel
) -> None: ...

COMPRESSION_MAPPING: Dict[str, Callable[[io.BytesIO], io.BytesIO]] = ...
