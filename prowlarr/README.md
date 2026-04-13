# Home Assistant Add-on: Prowlarr

Indexer manager and proxy for Sonarr, Radarr, and other *arr applications. Manage all your torrent and Usenet indexers in one place — changes sync automatically to connected apps.

## Installation

1. Add the repository `https://github.com/halali/ha-apps` in the HA Add-on Store.
2. Install **Prowlarr**, start it and open via the sidebar.

## Configuration

```yaml
PUID: 0
PGID: 0
TZ: Europe/Bratislava
reset_auth: false
```

- **PUID / PGID** — user ID Prowlarr runs as.
- **TZ** — timezone for scheduling.
- **reset_auth** — if `true`, disables authentication on startup.

## Paths

| HA path | Container path | Purpose |
|---------|----------------|---------|
| `/addon_configs/<slug>_prowlarr` | `/config` | Database, settings, logs |
| `/share` | `/share` | Shared data |

## External Port

- `9696/tcp` — Web UI and API.

## Connecting to Sonarr / Radarr

In Prowlarr under **Settings → Apps**, add Sonarr and Radarr using their internal HA addresses and API keys. Prowlarr will automatically sync all configured indexers to them.
