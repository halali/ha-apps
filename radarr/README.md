# Home Assistant Add-on: Radarr

Movie collection manager — automatic downloading and monitoring of movies via Usenet / BitTorrent.

## About

Built on [LinuxServer.io](https://docs.linuxserver.io/images/docker-radarr/) images. Supports **HA Ingress** and **external port 7878**.

## Installation

1. Add the repository `https://github.com/halali/ha-apps`.
2. Install **Radarr** from the store.
3. Start it and open via the sidebar.

## Configuration

```yaml
PUID: 0
PGID: 0
TZ: Europe/Bratislava
reset_auth: false
```

- **PUID / PGID** — user ID Radarr runs as. Set to `1000` if you need write access to `/media`.
- **TZ** — timezone for scheduling.
- **reset_auth** — if `true`, disables authentication on startup.

## Paths

| HA path | Container path | Purpose |
|---------|----------------|---------|
| `/addon_configs/<slug>_radarr` | `/config` | Database, settings |
| `/media` | `/media` | Movies |
| `/share` | `/share` | Shared data |

## External Port

- `7878/tcp` — Web UI and API.
