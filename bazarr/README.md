# Home Assistant Add-on: Bazarr

Bazarr je sprievodca pre Sonarr a Radarr — automaticky sťahuje titulky k seriálom a filmom.

## Inštalácia

1. Repozitár `https://github.com/halali/ha-apps` v HA Add-on Store.
2. Nainštaluj **Bazarr**, spusti a otvor cez sidebar.

## Konfigurácia

```yaml
PUID: 0
PGID: 0
TZ: Europe/Bratislava
```

## Cesty

| HA cesta | Kontajner | Popis |
|----------|-----------|-------|
| `/addon_configs/<slug>_bazarr` | `/config` | DB, nastavenia |
| `/media` | `/media` | Zdieľané s Sonarr/Radarr |
| `/share` | `/share` | Zdieľané dáta |

## Externý port

- `6767/tcp` — Web UI a API.

## Prepojenie s Sonarr / Radarr

V Bazarr **Settings → Sonarr / Radarr**, použi:
- Host: `a0d7b954-sonarr` alebo IP HA
- Port: `8989` (Sonarr) / `7878` (Radarr)
- API Key: z Sonarr/Radarr **Settings → General**
