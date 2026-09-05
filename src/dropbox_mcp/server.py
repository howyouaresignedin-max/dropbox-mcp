"""Dropbox MCP Server."""

from __future__ import annotations

import base64
import json
import logging
import os
from typing import Any

from mcp.server.fastmcp import FastMCP

from .client import DropboxClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dropbox-mcp")

mcp = FastMCP("dropbox")

# Lazily created client
_client: DropboxClient | None = None


def get_client() -> DropboxClient:
    global _client
    if _client is None:
        _client = DropboxClient()
    return _client


@mcp.tool()
def dropbox_account_info() -> str:
    """Return the display name of the currently authenticated Dropbox account."""
    return get_client().account_display_name()


@mcp.tool()
def dropbox_list_folder(path: str = "", recursive: bool = False) -> str:
    """
    List files and folders at the given Dropbox path.
    path="" means the root of the app folder or full Dropbox.
    """
    entries = get_client().list_folder(path, recursive=recursive)
    result = []
    for e in entries:
        item = {
            "name": e.name,
            "path": e.path_display,
            "type": "folder" if e.__class__.__name__ == "FolderMetadata" else "file",
        }
        if hasattr(e, "size"):
            item["size"] = e.size
        result.append(item)
    return json.dumps(result, indent=2)


@mcp.tool()
def dropbox_search(query: str, path: str = "", max_results: int = 30) -> str:
    """Search for files and folders matching the query."""
    matches = get_client().search(query, path=path, max_results=max_results)
    result = []
    for m in matches:
        meta = m.metadata.get_metadata()
        result.append({
            "name": meta.name,
            "path": meta.path_display,
            "type": "folder" if meta.__class__.__name__ == "FolderMetadata" else "file",
        })
    return json.dumps(result, indent=2)


@mcp.tool()
def dropbox_upload(path: str, content: str, is_base64: bool = False) -> str:
    """
    Upload content to Dropbox.
    - content: plain text or base64-encoded bytes
    - is_base64: set True if content is base64
    """
    data = base64.b64decode(content) if is_base64 else content.encode("utf-8")
    meta = get_client().upload(path, data)
    return f"Uploaded {meta.path_display} ({meta.size} bytes)"


@mcp.tool()
def dropbox_download(path: str, as_base64: bool = False) -> str:
    """
    Download a file from Dropbox.
    Returns text if the file looks like text, otherwise base64 when as_base64=True.
    """
    data = get_client().download(path)
    if as_base64:
        return base64.b64encode(data).decode("ascii")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return base64.b64encode(data).decode("ascii")


@mcp.tool()
def dropbox_create_folder(path: str) -> str:
    """Create a folder (including parents if needed)."""
    meta = get_client().create_folder(path)
    return f"Created folder {meta.path_display}"


@mcp.tool()
def dropbox_delete(path: str) -> str:
    """Delete a file or folder."""
    get_client().delete(path)
    return f"Deleted {path}"


@mcp.tool()
def dropbox_move(from_path: str, to_path: str) -> str:
    """Move or rename a file/folder."""
    meta = get_client().move(from_path, to_path)
    return f"Moved to {meta.path_display}"


@mcp.tool()
def dropbox_copy(from_path: str, to_path: str) -> str:
    """Copy a file or folder."""
    meta = get_client().copy(from_path, to_path)
    return f"Copied to {meta.path_display}"


@mcp.tool()
def dropbox_create_shared_link(path: str) -> str:
    """Create (or return existing) public shared link for a file or folder."""
    return get_client().create_shared_link(path)


@mcp.tool()
def dropbox_get_temporary_link(path: str) -> str:
    """Get a temporary direct download link (usually valid a few hours)."""
    return get_client().get_temporary_link(path)


def main():
    # Allow override via environment variables
    transport = os.getenv("MCP_TRANSPORT", "http").lower()
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8080"))

    logger.info("Starting Dropbox MCP server...")
    logger.info("Transport: %s | Host: %s | Port: %s", transport, host, port)

    if transport in ("http", "streamable-http", "streamable_http"):
        # Modern recommended HTTP transport
        mcp.run(transport="http", host=host, port=port)
    elif transport == "sse":
        # Legacy SSE transport
        mcp.run(transport="sse", host=host, port=port)
    else:
        # Default stdio
        mcp.run()


if __name__ == "__main__":
    main()
