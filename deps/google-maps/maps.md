# google-maps/maps

Google Maps MCP server. Geocoding, directions, distance matrix, elevation, and nearby place search.

## MCP Server

- **Package**: `@iflow-mcp/mcp-google-map`
- **Transport**: stdio
- **Command**: `npx @iflow-mcp/mcp-google-map --port 3000 --apikey "YOUR_KEY"`

## Authentication

Google Maps API key

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_MAPS_API_KEY` | Yes | API key from Google Cloud Console |

## Available Tools

| Tool | Description |
|------|-------------|
| `search_nearby` | Search nearby places |
| `get_place_details` | Place details |
| `maps_geocode` | Address to coordinates |
| `maps_reverse_geocode` | Coordinates to address |
| `maps_distance_matrix` | Calculate distances |
| `maps_directions` | Turn-by-turn directions |
| `maps_elevation` | Elevation data |

## Configuration Example

```toml
[[mcp.servers]]
name = "maps"
type = "stdio"
command = "npx"
args = ["-y", "@iflow-mcp/mcp-google-map"]
timeout_seconds = 60
env = { GOOGLE_MAPS_API_KEY = "your-value" }
tools = []
```

**Notes:** HTTP transport only (not stdio). Requires Places API and Maps API enabled in GCP.

## Links

- [Homepage](https://www.npmjs.com/package/@iflow-mcp/mcp-google-map)
