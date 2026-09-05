# dropbox-mcp

MCP (Model Context Protocol) server that exposes Dropbox as tools for any MCP-compatible client (Cursor, Claude Desktop, etc.).

Built on top of a clean OAuth2 + refresh-token Dropbox client.

## Features

Tools currently exposed:

| Tool | Description |
|------|-------------|
| `dropbox_list_folder` | List files and folders |
| `dropbox_search` | Search files/folders |
| `dropbox_upload` | Upload text or base64 content |
| `dropbox_download` | Download a file (returns text or base64) |
| `dropbox_create_folder` | Create a folder |
| `dropbox_delete` | Delete a file or folder |
| `dropbox_move` | Move / rename |
| `dropbox_copy` | Copy a file or folder |
| `dropbox_create_shared_link` | Create a public shared link |
| `dropbox_get_temporary_link` | Get a short-lived direct download link |
| `dropbox_account_info` | Get current account display name |

## Requirements

- Python 3.11+
- A Dropbox App with appropriate scopes

## Quick Setup

```bash
git clone https://github.com/howyouaresignedin-max/dropbox-mcp.git
cd dropbox-mcp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy and fill credentials:

```bash
cp .env.example .env
# Edit .env with your DROPBOX_APP_KEY, DROPBOX_APP_SECRET
# and DROPBOX_REFRESH_TOKEN (from the authorize flow)
```

If you don't have a refresh token yet, you can use the authorize script from the companion repo:
https://github.com/howyouaresignedin-max/dropbox-python-client

## Running the server

```bash
python -m dropbox_mcp
```

or

```bash
uvx dropbox-mcp   # once published
```

## Configure in your MCP client

### Cursor / Claude Desktop example

Add to your MCP config:

```json
{
  "mcpServers": {
    "dropbox": {
      "command": "python",
      "args": ["-m", "dropbox_mcp"],
      "cwd": "/path/to/dropbox-mcp",
      "env": {
        "DROPBOX_APP_KEY": "your_key",
        "DROPBOX_APP_SECRET": "your_secret",
        "DROPBOX_REFRESH_TOKEN": "your_refresh_token"
      }
    }
  }
}
```

You can also rely on a `.env` file in the project directory.

## Status

- Beta quality
- Ready for local testing with Cursor / Claude Desktop / other MCP clients
- Designed so it can later be turned into an official platform connector

## License

MIT
