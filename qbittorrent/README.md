# Home Assistant Add-on: qBittorrent

Open-source BitTorrent client with a web UI. Drop-in download client for Sonarr/Radarr/Lidarr/Prowlarr.

## About

Built on [LinuxServer.io](https://docs.linuxserver.io/images/docker-qbittorrent/) images. Web UI listens on **port 8081** internally; nginx proxies HA Ingress and the external port `8080` to it. BitTorrent peer port `6881` (TCP/UDP) is exposed for incoming peer connections.

## Installation

1. Make sure the repository `https://github.com/halali/ha-apps` is added.
2. In **Settings → Add-ons → Add-on Store** find **qBittorrent** and click **Install**.
3. Start the add-on and open the Web UI from the sidebar.

## Configuration

```yaml
PUID: 0
PGID: 0
TZ: Europe/Bratislava
trust_subnets: true
```

- **PUID / PGID** — user qBittorrent runs as.
- **TZ** — timezone.
- **trust_subnets** — when `true`, the WebUI auth subnet whitelist is set to common Docker / LAN ranges (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`). Disables the login prompt when accessed via HA Ingress. Set to `false` to enforce normal login.

## Default credentials

On first start, qBittorrent generates a random admin password and prints it in the add-on **Logs**. Change it under **Tools → Options → Web UI**.

## Paths

| HA path | Container path | Purpose |
|---------|----------------|---------|
| `/addon_configs/<slug>_qbittorrent` | `/config` | Database, settings, torrent state |
| `/media` | `/media` | Completed downloads / library |
| `/share` | `/share` | Watched folder for `.torrent` files |

## Connecting from Sonarr / Radarr / Lidarr

In each *arr app, add a download client:

- **Type**: qBittorrent
- **Host**: HA host IP
- **Port**: `8080`
- **Username / Password**: as configured in qBittorrent
- **Category**: e.g. `tv`, `movies`, `music`
