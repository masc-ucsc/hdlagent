import json
import logging
import time
from octoai.uploading_asset_library import AsyncUploadingAssetLibraryClient, UploadingAssetLibraryClient
from .base_client import BaseOctoAI, AsyncBaseOctoAI

import os
import typing
import httpx

from .asset_library.client import AssetLibraryClient, AsyncAssetLibraryClient
from .core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .core.pydantic_utilities import pydantic_v1
from .environment import OctoAIEnvironment
from .fine_tuning.client import AsyncFineTuningClient, FineTuningClient
from .image_gen.client import AsyncImageGenClient, ImageGenClient
from .text_gen.client import AsyncTextGenClient, TextGenClient
from .util import retry


_LOG = logging.getLogger(__name__)

DEFAULT_HEALTH_CHECK_TIMEOUT_SECONDS = 900.0

class _JSONEncoder(json.JSONEncoder):
    def default(self, o: typing.Any) -> typing.Any:
        if isinstance(o, bytes):
            return o.decode()
        return json.JSONEncoder.default(self, o)


class InferenceFuture(pydantic_v1.BaseModel):
    """Response class for endpoints that support server side async inferences.

    :param response_id: Unique identifier for inference
    :type response_id: str
    :param poll_url: URL to poll status of inference.
    :type poll_url: str
    """

    response_id: str
    poll_url: str


class OctoAI(BaseOctoAI):
    asset_library: UploadingAssetLibraryClient

    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters:
        - environment: OctoAIEnvironment. The environment to use for requests from the client. from .environment import OctoAIEnvironment

                                          Defaults to OctoAIEnvironment.PRODUCTION

        - api_key: typing.Optional[typing.Union[str, typing.Callable[[], str]]].

        - timeout: typing.Optional[float]. The timeout to be used, in seconds, for requests by default the timeout is 60 seconds.

        - httpx_client: typing.Optional[httpx.Client]. The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.
    ---
    from octoai.client import OctoAI

    client = OctoAI(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        environment: OctoAIEnvironment = OctoAIEnvironment.PRODUCTION,
        api_key: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = os.getenv("OCTOAI_TOKEN"),
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.Client] = None,
    ):
        super().__init__(
            environment=environment,
            api_key=api_key,
            timeout=timeout,
            httpx_client=httpx_client
        )

        self._httpx_client = self._client_wrapper.httpx_client
        self.asset_library = UploadingAssetLibraryClient(client_wrapper=self._client_wrapper)

    def _error(self, resp: httpx.Response):
        resp.raise_for_status()

    def infer(self, endpoint_url: str, inputs: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """Send a request to the given endpoint URL with inputs as request body.

        :param endpoint_url: target endpoint
        :type endpoint_url: str
        :param inputs: inputs for target endpoint
        :type inputs: Mapping[str, Any]

        :raises OctoAIServerError: server-side failures (unreachable, etc)
        :raises OctoAIClientError: client-side failures (throttling, unset token)

        :return: outputs from endpoint
        :rtype: Mapping[str, Any]
        """
        resp = retry(
            lambda: self._httpx_client.httpx_client.post(
                url=endpoint_url,
                headers={"Content-Type": "application/json"},
                content=json.dumps(inputs, cls=_JSONEncoder),
            )
        )
        if resp.status_code != 200:
            self._error(resp)
        return resp.json()

    def infer_async(
        self, endpoint_url: str, inputs: typing.Mapping[str, typing.Any]
    ) -> InferenceFuture:
        """Execute an inference in the background on the server.

        :class:`InferenceFuture` allows you to query status and get results
        once it's ready.

        :param endpoint_url: url to post inference request
        :type endpoint_url: str
        :param inputs: inputs to send to endpoint
        :type inputs: Mapping[str, Any]
        """
        resp = retry(
            lambda: self._httpx_client.httpx_client.post(
                url=endpoint_url, json=inputs, headers={"X-OctoAI-Async": "1"}
            )
        )
        if resp.status_code >= 400:
            self._error(resp)
        resp_json = resp.json()
        future = InferenceFuture(**resp_json)
        return future

    def infer_stream(
        self, endpoint_url: str, inputs: typing.Mapping[str, typing.Any], map_fn: typing.Optional[typing.Callable] = None
    ) -> typing.Iterator[dict]:
        """Stream text event response body for supporting endpoints.

        This is an alternative to loading all response body into memory at once.

        :param endpoint_url: target endpoint
        :type endpoint_url: str
        :param inputs: inputs for target endpoint such as a prompt and other parameters
        :type inputs: Mapping[str, Any]
        :param inputs: function to map over each response
        :type inputs: Callable
        :return: Yields a :class:`dict` that contains the server response data.
        :rtype: Iterator[:class:`dict`]
        """
        with self._httpx_client.httpx_client.stream(
            method="POST",
            url=endpoint_url,
            content=json.dumps(inputs, cls=_JSONEncoder),
            headers={"accept": "text/event-stream"},
        ) as resp:
            if resp.status_code >= 400:
                # Loads response body on error for streaming responses
                resp.read()
                self._error(resp)

            for payload in resp.iter_lines():
                # Empty lines used to separate payloads.
                if payload == "":
                    continue
                # End of stream (OpenAPI /v1/chat/completions).
                elif payload == "data: [DONE]":
                    break
                # Event data identified with "data:"  JSON inside.
                elif payload.startswith("data:"):
                    payload_dict = json.loads(payload.lstrip("data:"))
                    if map_fn:
                        yield map_fn(payload_dict)
                    else:
                        yield payload_dict
                # Any other input is a malformed response.
                else:
                    raise ValueError(
                        f"Stream response is malformed: {payload}"
                    )


    def _poll_future(self, future: InferenceFuture) -> typing.Dict[str, str]:
        """Get from poll_url and return response.

        :param future: Future from :meth:`OctoAI.infer_async`
        :type future: :class:`InferenceFuture`
        :returns: Dictionary with response
        :rtype: Dict[str, str]
        """
        response = self._httpx_client.httpx_client.get(url=future.poll_url)
        if response.status_code >= 400:
            self._error(response)
        return response.json()

    def is_future_ready(self, future: InferenceFuture) -> bool:
        """Return whether the future's result has been computed.

        This class will raise any errors if the status code is >= 400.

        :param future: Future from :meth:`OctoAI.infer_async`
        :type future: :class:`InferenceFuture`
        :returns: True if able to use :meth:`OctoAI.get_future_result`
        """
        resp_dict = self._poll_future(future)
        return "completed" == resp_dict.get("status")

    def get_future_result(self, future: InferenceFuture) -> typing.Optional[typing.Dict[str, typing.Any]]:
        """Return the result of an inference.

        This class will raise any errors if the status code is >= 400.

        :param future: Future from :meth:`Client.infer_async`
        :type future: :class:`InferenceFuture`
        :returns: None if future is not ready, or dict of the response.
        :rtype: Dict[str, Any], optional
        """
        resp_dict = self._poll_future(future)
        if resp_dict.get("status") != "completed":
            return None
        response_url = resp_dict.get("response_url")
        assert response_url is not None, "response_url is missing from response"
        response = self._httpx_client.httpx_client.get(response_url)
        if response.status_code >= 400:
            self._error(response)
        return response.json()

    def health_check(
        self, endpoint_url: str, timeout: float = DEFAULT_HEALTH_CHECK_TIMEOUT_SECONDS
    ) -> int:
        """Check health of an endpoint using a get request.  Try until timeout.

        :param endpoint_url: URL as a str starting with https permitting get requests.
        :type endpoint_url: str
        :param timeout: Seconds before request times out, defaults to 900.
        :type timeout: float
        :return: status code from get request.  200 means ready.
        :rtype: int
        """
        resp = self._health_check(
            lambda: self._httpx_client.httpx_client.get(url=endpoint_url), timeout=timeout
        )
        if resp.status_code >= 400:
            self._error(resp)
        return resp.status_code

    def _health_check(
        self,
        fn: typing.Callable[[], httpx.Response],
        timeout: float = DEFAULT_HEALTH_CHECK_TIMEOUT_SECONDS,
        interval: float = 1.0,
        iteration_count: int = 0,
    ) -> httpx.Response:
        """Check the health of an endpoint.

        :param fn: Get request for endpoint health check.
        :type fn: Callable[[], httpx.Response]
        :param timeout: seconds before health_check times out, defaults to 900.0
        :type timeout: int, optional
        :param interval: seconds to wait before checking endpoint health again,
            defaults to 1.0
        :type interval: int, optional
        :param iteration_count: count total attempts for cold start warning,
            defaults to 0
        :type iteration_count: int
        :return: Response once timeout has passed
        :rtype: httpx.Response
        """
        start = time.time()
        try:
            resp = fn()
            if timeout <= 0:
                return resp
            # Raise HTTPStatusError for 4xx or 5xx.
            resp.raise_for_status()
        except httpx.HTTPStatusError:
            if 400 <= resp.status_code < 500:
                # Raise client errors. Do not retry.
                return resp
            if iteration_count == 0 and self.__class__.__name__ == "Client":
                _LOG.warning(
                    "Your endpoint may take several minutes to start and be ready to "
                    "serve inferences. You can increase your endpoint's min replicas "
                    "to mitigate cold starts."
                )
            if resp.status_code >= 500:
                stop = time.time()
                current = stop - start
                time.sleep(interval)
                return self._health_check(
                    fn, timeout - current - interval, interval, iteration_count + 1
                )
        # Raise error without retry on all other exceptions.
        return resp


class AsyncOctoAI(AsyncBaseOctoAI):
    asset_library: AsyncUploadingAssetLibraryClient

    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters:
        - environment: OctoAIEnvironment. The environment to use for requests from the client. from .environment import OctoAIEnvironment

                                          Defaults to OctoAIEnvironment.PRODUCTION

        - api_key: typing.Optional[typing.Union[str, typing.Callable[[], str]]].

        - timeout: typing.Optional[float]. The timeout to be used, in seconds, for requests by default the timeout is 60 seconds.

        - httpx_client: typing.Optional[httpx.AsyncClient]. The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.
    ---
    from octoai.client import AsyncOctoAI

    client = AsyncOctoAI(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        environment: OctoAIEnvironment = OctoAIEnvironment.PRODUCTION,
        api_key: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = os.getenv("OCTOAI_TOKEN"),
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
    ):
        super().__init__(
            environment=environment,
            api_key=api_key,
            timeout=timeout,
            httpx_client=httpx_client
        )

        self.asset_library = AsyncUploadingAssetLibraryClient(client_wrapper=self._client_wrapper)