# Home Assistant Add-on: Bazarr

Companion app for Sonarr and Radarr — automatically downloads subtitles for your TV series and movies.

## Installation

1. Add the repository `https://github.com/halali/ha-apps` in the HA Add-on Store.
2. Install **Bazarr**, start it and open via the sidebar.

## Configuration

```yaml
PUID: 0
PGID: 0
TZ: Europe/Bratislava
```

- **PUID / PGID** — user ID Bazarr runs as. Set to `1000` if you need write access to `/media`.
- **TZ** — timezone for scheduling.

> Bazarr does not enforce a separate login by default — Home Assistant authenticates the Ingress session, so no `reset_auth` option is exposed.

## Paths

| HA path | Container path | Purpose |
|---------|----------------|---------|
| `/addon_configs/<slug>_bazarr` | `/config` | Database, settings |
| `/media` | `/media` | Shared with Sonarr/Radarr |
| `/share` | `/share` | Shared data |

## External Port

- `6767/tcp` — Web UI and API.

## Connecting to Sonarr / Radarr

In Bazarr under **Settings → Sonarr / Radarr**, use:
- **Host**: the IP of your Home Assistant instance
- **Port**: `8989` (Sonarr) / `7878` (Radarr)
- **API Key**: from Sonarr/Radarr **Settings → General**
