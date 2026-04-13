# Halali — Home Assistant Add-ons

A collection of Home Assistant add-ons for popular *arr applications built on [LinuxServer.io](https://www.linuxserver.io/) images. All add-ons support **Home Assistant Ingress** (sidebar button), an **external port** for direct API access and mobile apps, and **automatic updates** when a new upstream version is released.

## Repository Installation

1. In Home Assistant open **Settings → Add-ons → Add-on Store**.
2. Click the menu (three dots top right) → **Repositories**.
3. Add URL: `https://github.com/halali/ha-apps`
4. The add-ons will appear in the store shortly.

## Available Add-ons

| Add-on | Description | Upstream |
|--------|-------------|----------|
| [Sonarr](./sonarr) | TV series management and download automation | [linuxserver/sonarr](https://hub.docker.com/r/linuxserver/sonarr) |
| [Radarr](./radarr) | Movie collection management and download automation | [linuxserver/radarr](https://hub.docker.com/r/linuxserver/radarr) |
| [Bazarr](./bazarr) | Automatic subtitle downloading for Sonarr and Radarr | [linuxserver/bazarr](https://hub.docker.com/r/linuxserver/bazarr) |
| [Prowlarr](./prowlarr) | Indexer manager and proxy for Sonarr, Radarr and other *arr apps | [linuxserver/prowlarr](https://hub.docker.com/r/linuxserver/prowlarr) |
| [Seerr](./seerr) | Media request manager for Plex, Jellyfin and Emby — successor to Overseerr | [seerr-team/seerr](https://github.com/seerr-team/seerr) |

## Features

- ✅ **HA Ingress** — open the app directly from the HA sidebar, no separate login
- ✅ **External port** — direct LAN access for API clients (e.g. Seerr ↔ Sonarr, mobile apps)
- ✅ **amd64** — built for x86-64 hosts
- ✅ **Auto-update** — GitHub Actions checks for new upstream versions daily and bumps the add-on automatically
- ✅ **Persistent data** — configuration stored in `/addon_configs/<slug>`, media in `/media`

## License

MIT © Halali
