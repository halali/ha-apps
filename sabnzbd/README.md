# Home Assistant Add-on: SABnzbd

Open-source Usenet binary newsreader. Companion download client for Sonarr/Radarr/Lidarr/Prowlarr (alternative or complement to qBittorrent).

## About

Built on [LinuxServer.io](https://docs.linuxserver.io/images/docker-sabnzbd/) images. Web UI listens on **port 8086** internally; nginx proxies HA Ingress and the external port `8085` to it. The non-default external port avoids conflict with qBittorrent's `8080`.

## Installation

1. Make sure the repository `https://github.com/halali/ha-apps` is added.
2. In **Settings → Add-ons → Add-on Store** find **SABnzbd** and click **Install**.
3. Start the add-on and open the Web UI from the sidebar.

## Configuration

```yaml
PUID: 0
PGID: 0
TZ: Europe/Bratislava
```

- **PUID / PGID** — user SABnzbd runs as. Set to `1000` if you need write access to `/media`.
- **TZ** — timezone for scheduling.

## Initial Setup

The first launch shows a setup wizard. The API key for *arr integrations is in **Config → General → API Key**.

## Paths

| HA path | Container path | Purpose |
|---------|----------------|---------|
| `/addon_configs/<slug>_sabnzbd` | `/config` | Database, settings |
| `/media` | `/media` | Completed downloads |
| `/share` | `/share` | Watched folder for `.nzb` files |

## External Port

- `8085/tcp` — Web UI and API.

## Connecting from Sonarr / Radarr / Lidarr

In each *arr app, add a download client:

- **Type**: SABnzbd
- **Host**: HA host IP
- **Port**: `8085`
- **API Key**: from SABnzbd **Config → General**
- **Category**: e.g. `tv`, `movies`, `music`
