"""Minimal Dropbox client used by the MCP server."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Union

from dotenv import load_dotenv
import dropbox
from dropbox.files import FileMetadata, FolderMetadata, WriteMode
from dropbox.exceptions import ApiError


def load_credentials() -> dict[str, str]:
    load_dotenv()
    app_key = os.getenv("DROPBOX_APP_KEY", "").strip()
    app_secret = os.getenv("DROPBOX_APP_SECRET", "").strip()
    refresh_token = os.getenv("DROPBOX_REFRESH_TOKEN", "").strip()

    if not app_key or not app_secret:
        raise ValueError("DROPBOX_APP_KEY and DROPBOX_APP_SECRET must be set")
    if not refresh_token:
        raise ValueError("DROPBOX_REFRESH_TOKEN must be set")

    return {
        "app_key": app_key,
        "app_secret": app_secret,
        "refresh_token": refresh_token,
    }


def get_dbx() -> dropbox.Dropbox:
    creds = load_credentials()
    return dropbox.Dropbox(
        app_key=creds["app_key"],
        app_secret=creds["app_secret"],
        oauth2_refresh_token=creds["refresh_token"],
    )


class DropboxClient:
    def __init__(self):
        self.dbx = get_dbx()

    def account_display_name(self) -> str:
        return self.dbx.users_get_current_account().name.display_name

    def list_folder(self, path: str = "", recursive: bool = False):
        result = self.dbx.files_list_folder(path, recursive=recursive)
        entries = list(result.entries)
        while result.has_more:
            result = self.dbx.files_list_folder_continue(result.cursor)
            entries.extend(result.entries)
        return entries

    def search(self, query: str, path: str = "", max_results: int = 50):
        result = self.dbx.files_search_v2(
            query,
            options=dropbox.files.SearchOptions(path=path or None, max_results=max_results),
        )
        return result.matches

    def upload(self, dropbox_path: str, content: bytes, mode: str = "overwrite") -> FileMetadata:
        return self.dbx.files_upload(content, dropbox_path, mode=WriteMode(mode))

    def download(self, dropbox_path: str) -> bytes:
        _, response = self.dbx.files_download(dropbox_path)
        return response.content

    def create_folder(self, path: str) -> FolderMetadata:
        return self.dbx.files_create_folder_v2(path).metadata

    def delete(self, path: str):
        return self.dbx.files_delete_v2(path).metadata

    def move(self, from_path: str, to_path: str):
        return self.dbx.files_move_v2(from_path, to_path).metadata

    def copy(self, from_path: str, to_path: str):
        return self.dbx.files_copy_v2(from_path, to_path).metadata

    def create_shared_link(self, path: str) -> str:
        settings = dropbox.sharing.SharedLinkSettings(
            requested_visibility=dropbox.sharing.RequestedVisibility.public
        )
        try:
            link = self.dbx.sharing_create_shared_link_with_settings(path, settings=settings)
            return link.url
        except ApiError as e:
            if e.error.is_shared_link_already_exists():
                return e.error.get_shared_link_already_exists().metadata.url
            raise

    def get_temporary_link(self, path: str) -> str:
        return self.dbx.files_get_temporary_link(path).link
