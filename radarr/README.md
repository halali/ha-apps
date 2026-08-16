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

- **PUID / PGID** — user and group ID Radarr runs as. Leave at `0` (root) unless you know better: Home Assistant mounts `/media` from a CIFS share owned by root with `dir_mode 0755`, so any other uid can read it but not write to it. Lower it only when `/media` is local storage the target uid can write.
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
