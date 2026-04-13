# Home Assistant Add-on: Seerr

Open-source media request and discovery manager for Plex, Jellyfin, and Emby. Active fork of Overseerr with added Emby/Jellyfin support.

## Installation

1. Add the repository `https://github.com/halali/ha-apps` in the HA Add-on Store.
2. Install **Seerr**, start it and open via the sidebar.

## Configuration

```yaml
TZ: Europe/Bratislava
LOG_LEVEL: info
```

## Migrating from Overseerr

Seerr automatically migrates your data on first startup. Steps:

1. **Stop** the Overseerr add-on in HA.
2. Copy the contents of the Overseerr add-on config folder into the Seerr add-on config folder using the HA **File editor** or **Terminal** add-on:
   - Source: `/addon_configs/<overseerr-slug>/`
   - Destination: `/addon_configs/<seerr-slug>/`
3. Start the Seerr add-on — migration runs automatically on startup.
4. Once you have verified everything works, you can uninstall the Overseerr add-on.

> Back up your data before migrating by copying the folder somewhere safe.

## External Port

- `5055/tcp` — Web UI and API.
