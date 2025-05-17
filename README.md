# YC Directory Server

A MCP (Model Context Protocal) server that provides tools to access and search Y Combinator company data.

## Features

- List top YC companies
- Search companies by name or description
- Browse companies by batch (e.g., W21, S22)
- List all YC batches with company counts
- Search batches by name or year

## Installation

### Prerequisites

- Python 3.8 or higher
- MCP library

### Setup

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Install the MCP Server

```bash
mcp install yc_mcp.py --name "YC Directory Server"
Will auto install in Claude Desktop as a tool
May have to go into task manager, end the Claude Desktop task and restart Desktop to see the tool

```

## API Tools

The server provides the following tools:

- `list_top_companies(limit=10)`: Lists the top YC companies
- `list_companies_by_batch(batch)`: Lists companies from a specific batch
- `search_companies(keyword)`: Searches companies by name or description
- `list_all_batches()`: Lists all YC batches with company counts
- `search_batches(query)`: Searches batches by name or year

## Data Source

This server uses the YC OSS API to fetch company data from:
`https://yc-oss.github.io/api/`

## License

MIT