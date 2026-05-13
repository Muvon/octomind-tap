# google-maps/maps

Google Maps MCP server. Geocoding, directions, distance matrix, elevation, places, timezone, weather, air quality, static map images, and composite tools (explore area, plan route, compare places, local rank tracking).

Replaces the deprecated `@modelcontextprotocol/server-google-maps`.

## MCP Server

- Package: `@cablate/mcp-google-map`
- Transport: stdio (also supports streamable HTTP — we use stdio)
- Command: `npx -y @cablate/mcp-google-map --stdio`

## Authentication

Google Maps API key from [Google Cloud Console](https://console.cloud.google.com).

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_MAPS_API_KEY` | Yes | API key with Places API (New), Geocoding, Directions, Distance Matrix, Elevation, Timezone, Weather, and Air Quality APIs enabled |

## Available Tools

| Tool | Description |
|------|-------------|
| `maps_search_nearby` | Nearby places by type with radius, rating, open-now filters |
| `maps_search_places` | Natural-language place search ("ramen in Tokyo") |
| `maps_place_details` | Full details by `place_id` — reviews, phone, hours, photos |
| `maps_geocode` | Address → GPS coordinates |
| `maps_reverse_geocode` | GPS coordinates → street address |
| `maps_distance_matrix` | Travel distance/time between origin/destination sets |
| `maps_directions` | Turn-by-turn directions |
| `maps_elevation` | Elevation in meters for coordinates |
| `maps_timezone` | Timezone ID, offset, local time for coordinates |
| `maps_weather` | Current weather or forecast |
| `maps_air_quality` | AQI, pollutants, health recommendations |
| `maps_static_map` | Map image with markers/paths/routes |
| `maps_batch_geocode` | Geocode up to 50 addresses in one call |
| `maps_search_along_route` | Places along a route, sorted by detour time |
| `maps_explore_area` | Composite: multi-type search + details around a location |
| `maps_plan_route` | Composite: geocode, optimize stop order, return directions |
| `maps_compare_places` | Composite: side-by-side place comparison |
| `maps_local_rank_tracker` | Geographic grid rank tracking (ARP / ATRP / SoLV) |

All tools are `readOnlyHint: true` / `destructiveHint: false` — clients may auto-approve.

## Configuration Example

```toml
[[mcp.servers]]
name = "google-maps"
type = "stdio"
command = "npx"
args = ["-y", "@cablate/mcp-google-map", "--stdio"]
timeout_seconds = 120
env = { GOOGLE_MAPS_API_KEY = "your-key" }
tools = []
```

Notes:
- Enable Places API (New) in GCP before using place-search / place-details tools.
- First launch downloads the package via `npx` — keep `timeout_seconds` ≥120 for cold caches.

## Links

- [npm](https://www.npmjs.com/package/@cablate/mcp-google-map)
- [GitHub](https://github.com/cablate/mcp-google-map)
