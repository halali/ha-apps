# Home Assistant Add-on: Overseerr

Overseerr je request management systém pre Plex/Jellyfin. Používatelia môžu žiadať filmy a seriály, ktoré Overseerr automaticky pošle do Sonarr/Radarr.

## Inštalácia

1. Pridaj repozitár `https://github.com/halali/ha-apps`.
2. Nainštaluj **Overseerr**, spusti a otvor cez sidebar.
3. Pri prvom spustení prejdi setup wizardom (pripojenie k Plex/Jellyfin, Sonarr, Radarr).

## Konfigurácia

```yaml
PUID: 0
PGID: 0
TZ: Europe/Bratislava
LOG_LEVEL: info
```

## Cesty

| HA cesta | Kontajner | Popis |
|----------|-----------|-------|
| `/addon_configs/<slug>_overseerr` | `/config` | Settings, DB |
| `/media` | `/media` (read-only) | Pre kontrolu existujúcich súborov |
| `/share` | `/share` | Zdieľané dáta |

## Externý port

- `5055/tcp` — Web UI, API, webhooks (napr. pre push z Plexu).

## Prepojenie

- **Sonarr**: Host `a0d7b954-sonarr` (slug add-on), port `8989`, API key z Sonarr
- **Radarr**: Host `a0d7b954-radarr`, port `7878`, API key z Radarr

**Tip**: Namiesto slug host mena sa dá použiť IP adresa HA v LAN.
