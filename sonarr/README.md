# Home Assistant Add-on: Sonarr

Smart PVR for TV series. Monitors your indexer RSS feeds and automatically downloads new episodes.

## About

Built on [LinuxServer.io](https://docs.linuxserver.io/images/docker-sonarr/) images. Supports **HA Ingress** (sidebar button) and **external port 8989** (for the mobile app, Seerr integration, Bazarr integration).

## Installation

1. Make sure the repository `https://github.com/halali/ha-apps` is added.
2. In **Settings → Add-ons → Add-on Store** find **Sonarr** and click **Install**.
3. Start the add-on and click **Open Web UI** in the sidebar.

## Configuration

```yaml
PUID: 0
PGID: 0
TZ: Europe/Bratislava
reset_auth: false
```

- **PUID / PGID** — user ID Sonarr runs as. Set to `1000` if you need write access to `/media`.
- **TZ** — timezone for scheduling.
- **reset_auth** — if `true`, disables authentication on startup (useful when using Ingress only and want to avoid double login).

## Paths

| HA path | Container path | Purpose |
|---------|----------------|---------|
| `/addon_configs/<slug>_sonarr` | `/config` | Database, settings, logs |
| `/media` | `/media` | TV series |
| `/share` | `/share` | Shared data |

Map your download directories (torrents, usenet) into `/share` or `/media`.

## External Port

- `8989/tcp` — Web UI and API.

Use this port for the **Sonarr** mobile app, **Seerr** integration, **Bazarr** integration, etc.

## API Key

Find the API key in Sonarr under **Settings → General → API Key**.
