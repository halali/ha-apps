# Home Assistant Add-on: Tautulli

Monitoring, analytics, and notifications for Plex Media Server. View who's watching what, get history, top users, and rich notifications.

## About

Built on [LinuxServer.io](https://docs.linuxserver.io/images/docker-tautulli/) images. Web UI listens on **port 8182** internally; nginx proxies HA Ingress and the external port `8181` to it.

## Installation

1. Make sure the repository `https://github.com/halali/ha-apps` is added.
2. In **Settings → Add-ons → Add-on Store** find **Tautulli** and click **Install**.
3. Start the add-on and open the Web UI from the sidebar.

## Configuration

```yaml
PUID: 0
PGID: 0
TZ: Europe/Bratislava
```

- **PUID / PGID** — user Tautulli runs as.
- **TZ** — timezone.

## Initial Setup

On first launch a wizard asks for your Plex server credentials.

## Paths

| HA path | Container path | Purpose |
|---------|----------------|---------|
| `/addon_configs/<slug>_tautulli` | `/config` | Database, settings |
| `/share` | `/share` | Optional shared folder |

## External Port

- `8181/tcp` — Web UI and API.
