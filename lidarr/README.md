# Home Assistant Add-on: Lidarr

Music collection manager for Usenet and BitTorrent users — automatic downloading, organising and tagging of albums.

## About

Built on [LinuxServer.io](https://docs.linuxserver.io/images/docker-lidarr/) images. Supports **HA Ingress** (sidebar button) and **external port 8686** (for the Lidarr mobile app and API integrations).

## Installation

1. Make sure the repository `https://github.com/halali/ha-apps` is added.
2. In **Settings → Add-ons → Add-on Store** find **Lidarr** and click **Install**.
3. Start the add-on and click **Open Web UI** in the sidebar.

## Configuration

```yaml
PUID: 0
PGID: 0
TZ: Europe/Bratislava
reset_auth: false
```

- **PUID / PGID** — user ID Lidarr runs as. Set to `1000` if you need write access to `/media`.
- **TZ** — timezone for scheduling.
- **reset_auth** — if `true`, disables authentication on startup (useful when using Ingress only).

## Paths

| HA path | Container path | Purpose |
|---------|----------------|---------|
| `/addon_configs/<slug>_lidarr` | `/config` | Database, settings, logs |
| `/media` | `/media` | Music library |
| `/share` | `/share` | Shared data |

## External Port

- `8686/tcp` — Web UI and API.

## Connecting to Prowlarr

In Prowlarr under **Settings → Apps**, add Lidarr using its internal HA address and API key from Lidarr **Settings → General**.
