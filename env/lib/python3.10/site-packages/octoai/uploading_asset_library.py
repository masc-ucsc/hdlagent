import asyncio
import contextlib
import functools
import pathlib
from time import sleep
import time
import typing

from octoai.asset_library.types.status import Status
from .asset_library.client import AsyncAssetLibraryClient
from .asset_library.types.create_asset_response import CreateAssetResponse
from .asset_library.types.create_asset_response_transfer_api import CreateAssetResponseTransferApi, CreateAssetResponseTransferApi_PresignedUrl, CreateAssetResponseTransferApi_Sts
import boto3
from .core.client_wrapper import AsyncClientWrapper
import httpx
from octoai.asset_library.types.asset import Asset

from .asset_library.client import OMIT
from .asset_library.types.data import Data
from .asset_library.types.file_structure import FileStructure
from .asset_library.types.transfer_api_type import TransferApiType
from .core.request_options import RequestOptions
from .core.client_wrapper import SyncClientWrapper
from .asset_library.client import AssetLibraryClient
from .core.api_error import ApiError


_TERMINAL_STATUSES: typing.Set[Status] = {"ready", "deleted", "rejected", "error"}


class AssetReadyTimeout(Exception):
    pass


class AssetNotReady(Exception):
    pass


class IncompatibleFileStructure(Exception):
    pass


def _sts_upload(x_api: CreateAssetResponseTransferApi_Sts, file_structure: FileStructure, file: typing.Union[str, typing.BinaryIO]):
    is_dir = isinstance(file, str) and pathlib.Path(file).is_dir()

    if is_dir and file_structure != "multiple_files":
        raise IncompatibleFileStructure("Asset's file structure is a multiple_files but file is not a directory")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=x_api.aws_access_key_id,
        aws_secret_access_key=x_api.aws_secret_access_key,
        aws_session_token=x_api.aws_session_token,
    )

    if isinstance(file, str) and is_dir:
        for file_path in pathlib.Path(file).rglob("*"):
            if file_path.is_file():
                s3_client.upload_file(
                    str(file_path),
                    x_api.s3bucket,
                    f"{x_api.s3key}{file_path.relative_to(file).as_posix()}",
                )
    else:
        try:
            s3_client.upload_file(file, x_api.s3bucket, x_api.s3key)
        except Exception as e:
            raise Exception(f"Error uploading file to server: {e}")


class UploadingAssetLibraryClient(AssetLibraryClient):
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    def create_from_file(
        self,
        file: typing.Union[str, typing.BinaryIO],
        data: Data,
        name: str,
        description: typing.Optional[str] = OMIT,
        is_public: typing.Optional[bool] = OMIT,
        transfer_api_type: typing.Optional[TransferApiType] = OMIT
    ) -> Asset:
        """
        Parameters:
            - file: typing.Union[str, typing.BinaryIO]. File to upload.

            - data: Data. Asset data.

            - name: str. Asset name.

            - description: typing.Optional[str].

            - is_public: typing.Optional[bool]. True if asset is public.

            - transfer_api_type: typing.Optional[TransferApiType]. Transfer API type.
        """
        if isinstance(file, str) and not pathlib.Path(file).exists():
            raise FileNotFoundError(f"File {file} does not exist")

        response: CreateAssetResponse = self.create(
            data=data,
            name=name,
            asset_type=data.asset_type,
            description=description,
            is_public=is_public,
            transfer_api_type=transfer_api_type
        )
        self._transfer_file(response.transfer_api, response.asset.file_structure, file=file)

        self.complete_upload(response.asset.id)

        return self.wait_for_ready(response.asset, transfer_api_type=transfer_api_type)


    def create_from_url(
        self,
        url: str,
        data: Data,
        name: str,
        description: typing.Optional[str] = OMIT,
        is_public: typing.Optional[bool] = OMIT,
        transfer_api_type: typing.Optional[TransferApiType] = "sts"
    ) -> Asset:
        """
        Create an asset from a URL.

        Parameters:
            - url: str. URL to create asset from.

            - data: Data. Asset data.

            - name: str. Asset name.

            - description: typing.Optional[str].

            - is_public: typing.Optional[bool]. True if asset is public.

            - transfer_api_type: typing.Optional[TransferApiType]. Transfer API type.
        """
        response: CreateAssetResponse = self.create(
            data=data,
            name=name,
            asset_type=data.asset_type,
            description=description,
            is_public=is_public,
            url=url,
            transfer_api_type=transfer_api_type,
        )

        return self.wait_for_ready(response.asset, transfer_api_type=transfer_api_type)


    def wait_for_ready(
        self,
        asset: Asset,
        poll_interval=10,
        timeout_seconds=900,
        transfer_api_type: typing.Optional[TransferApiType] = OMIT
    ):
        """
        Wait for asset to be ready to use.

        This waits until the asset's status is READY or an error status.

        Parameters:
            - asset: Asset. Asset to wait on.

            - poll_interval: int. Poll interval in seconds.

            - timeout_seconds: int. Timeout in seconds.

            - transfer_api_type: typing.Optional[TransferApiType]. Transfer API type.
        """
        start_time = time.monotonic()

        while asset.status not in _TERMINAL_STATUSES:
            now = time.monotonic()
            if now - start_time > timeout_seconds:
                raise AssetReadyTimeout("Asset creation timed out")

            time.sleep(poll_interval)
            if transfer_api_type is not OMIT:
                asset = self.get(asset.id, transfer_api_type=transfer_api_type).asset
            else:
                asset = self.get(asset.id).asset

        if asset.status != "ready":
            raise AssetNotReady(f"Asset creation failed with status: {asset.status}")

        return asset


    def _transfer_file(self, transfer_api_used: CreateAssetResponseTransferApi, file_structure: FileStructure, file: typing.Union[str, typing.BinaryIO]):
        if isinstance(transfer_api_used, CreateAssetResponseTransferApi_PresignedUrl):
            with contextlib.ExitStack() as exit_stack:
                file_data = exit_stack.enter_context(open(file, "rb")) if isinstance(file, str) else file
                upload_resp = httpx.put(
                    url=transfer_api_used.put_url, content=file_data, timeout=60000
                )
                upload_resp.raise_for_status()
        elif isinstance(transfer_api_used, CreateAssetResponseTransferApi_Sts):
            _sts_upload(transfer_api_used, file_structure, file)


class AsyncUploadingAssetLibraryClient(AsyncAssetLibraryClient):
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)
        self._signed_url_client = httpx.AsyncClient()

    async def create_from_file(
        self,
        file: typing.Union[str, typing.BinaryIO],
        data: Data,
        name: str,
        description: typing.Optional[str] = OMIT,
        is_public: typing.Optional[bool] = OMIT,
        transfer_api_type: typing.Optional[TransferApiType] = OMIT
    ) -> Asset:
        """
        Parameters:
            - file: typing.Union[str, typing.BinaryIO]. File to upload.

            - data: Data. Asset data.

            - name: str. Asset name.

            - description: typing.Optional[str].

            - is_public: typing.Optional[bool]. True if asset is public.

            - transfer_api_type: typing.Optional[TransferApiType]. Transfer API type.
        """
        if isinstance(file, str) and not pathlib.Path(file).exists():
            raise FileNotFoundError(f"File {file} does not exist")

        response: CreateAssetResponse = await self.create(
            data=data,
            name=name,
            asset_type=data.asset_type,
            description=description,
            is_public=is_public,
            transfer_api_type=transfer_api_type
        )

        await self._transfer_file(response.transfer_api, response.asset.file_structure, file=file)

        await self.complete_upload(response.asset.id)

        return await self.wait_for_ready(response.asset, transfer_api_type=transfer_api_type)

    async def create_from_url(
        self,
        url: str,
        data: Data,
        name: str,
        description: typing.Optional[str] = OMIT,
        is_public: typing.Optional[bool] = OMIT,
        transfer_api_type: typing.Optional[TransferApiType] = "sts"
    ) -> Asset:
        """
        Create an asset from a URL.

        Parameters:
            - url: str. URL to create asset from.

            - data: Data. Asset data.

            - name: str. Asset name.

            - description: typing.Optional[str].

            - is_public: typing.Optional[bool]. True if asset is public.

            - transfer_api_type: typing.Optional[TransferApiType]. Transfer API type.
        """
        response: CreateAssetResponse = await self.create(
            data=data,
            name=name,
            asset_type=data.asset_type,
            description=description,
            is_public=is_public,
            url=url,
            transfer_api_type=transfer_api_type,
        )

        return await self.wait_for_ready(response.asset, transfer_api_type=transfer_api_type)

    async def wait_for_ready(
        self,
        asset: Asset,
        poll_interval=10,
        timeout_seconds=900,
        transfer_api_type: typing.Optional[TransferApiType] = OMIT
    ):
        """
        Wait for asset to be ready to use.

        This waits until the asset's status is READY or an error status.

        Parameters:
            - asset: Asset. Asset to wait on.

            - poll_interval: int. Poll interval in seconds.

            - timeout_seconds: int. Timeout in seconds.

            - transfer_api_type: typing.Optional[TransferApiType]. Transfer API type.
        """
        start_time = time.monotonic()

        while asset.status not in _TERMINAL_STATUSES:
            now = time.monotonic()
            if now - start_time > timeout_seconds:
                raise AssetReadyTimeout("Asset creation timed out")

            await asyncio.sleep(poll_interval)
            if transfer_api_type is not OMIT:
                asset = (await self.get(asset.id, transfer_api_type=transfer_api_type)).asset
            else:
                asset = (await self.get(asset.id)).asset

        if asset.status != "ready":
            raise AssetNotReady(f"Asset creation failed with status: {asset.status}")

        return asset

    async def _transfer_file(self, transfer_api_used: CreateAssetResponseTransferApi, file_structure: FileStructure, file: typing.Union[str, typing.BinaryIO]):
        if isinstance(transfer_api_used, CreateAssetResponseTransferApi_PresignedUrl):
            # TODO: Use aiofiles to make this fully async?
            file_data_bytes = await asyncio.get_running_loop().run_in_executor(
                None,
                functools.partial(
                    _read_entire_file,
                    file
                )
            )

            upload_resp = await self._signed_url_client.put(
                url=transfer_api_used.put_url, content=file_data_bytes, timeout=60000
            )
            upload_resp.raise_for_status()
        elif isinstance(transfer_api_used, CreateAssetResponseTransferApi_Sts):
            _sts_upload(transfer_api_used, file_structure, file)


def _read_entire_file(file: typing.Union[str, typing.BinaryIO]) -> bytes:
    if isinstance(file, str):
        with open(file, "rb") as f:
            return f.read()
    else:
        return file.read()