
import base64
import random
import time
import typing

import httpx

from .image_gen.types import ImageGeneration, VideoGeneration


def to_file(data: typing.Union[str, ImageGeneration, VideoGeneration], file_name: str):
    """Write data to local file.

    :param file_name: path to local file
    :type file_name: str
    """
    if isinstance(data, ImageGeneration):
        assert data.image_b64 is not None
        to_file(data.image_b64, file_name)
    if isinstance(data, VideoGeneration):
        assert data.video is not None
        to_file(data.video, file_name)
    elif isinstance(data, str):
        with open(file_name, "wb") as fd:
            fd.write(base64.b64decode(data))


def from_file(file_name: str) -> str:
    """Read data from local file.

    :param file_name: path to local file
    :type file_name: str
    :return: data read from file
    :rtype: str
    """
    with open(file_name, "rb") as fd:
        return base64.b64encode(fd.read()).decode()


def retry(
    fn: typing.Callable[[], httpx.Response],
    retry_count: int = 5,
    interval: float = 1.0,
    exp_backoff: float = 2.0,
    jitter: float = 1.0,
    maximum_backoff: float = 30.0,
) -> httpx.Response:
    """Retry an HTTP request with exponential backoff and jitter.

    :param fn: function to call
    :type fn: Callable[[], httpx.Response]
    :param retry_count: number of times to retry, defaults to 5
    :type retry_count: int, optional
    :param interval: duration to wait before retry, defaults to 1.0
    :type interval: float, optional
    :param exp_backoff: exponent to increase interval each try, defaults to 2.0
    :type exp_backoff: float, optional
    :param jitter: , defaults to 1.0
    :type jitter: float, optional
    :param maximum_backoff: max duration to wait, defaults to 30.0
    :type maximum_backoff: float, optional
    :raises OctoAIClientError: occurs when a client error is thrown.
    :return: response from api server
    :rtype: httpx.Response
    """
    try:
        resp = fn()
        if retry_count - 1 == 0:
            return resp
        # Raise HTTPStatusError for 4xx or 5xx.
        resp.raise_for_status()
    except httpx.HTTPStatusError:
        if resp.status_code >= 500 or resp.status_code == 429:
            time.sleep(interval + random.uniform(0, jitter))
            return retry(
                fn,
                retry_count - 1,
                interval * exp_backoff,
                exp_backoff,
                jitter,
                maximum_backoff,
            )

        # Raise error on all other client errors.
        elif 400 <= resp.status_code < 499 and resp.status_code != 429:
            # Raise error. Do not retry.
            return resp

    # Raise error without retry on all other exceptions.
    return resp
