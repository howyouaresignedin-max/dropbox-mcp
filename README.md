# dropbox-mcp

MCP (Model Context Protocol) server that exposes Dropbox as tools for any MCP-compatible client.

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
cp .env.example .env
# Fill in your DROPBOX_* credentials
```

## Running the server

### HTTP mode (recommended for Deepnote / remote access)

```bash
python -m dropbox_mcp
```

By default it starts on **0.0.0.0:8080** using the modern HTTP transport.

You can override with environment variables:

```bash
MCP_TRANSPORT=http MCP_HOST=0.0.0.0 MCP_PORT=8080 python -m dropbox_mcp
```

### Stdio mode (for local Cursor / Claude Desktop)

```bash
MCP_TRANSPORT=stdio python -m dropbox_mcp
```

## Deepnote / Port exposure

Once the server is running on port 8080, use Deepnote’s “Incoming connections” or port-forwarding feature to expose it if you need external access.

## License

MIT
