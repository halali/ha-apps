# Home Assistant Add-on: Radarr

Správa filmovej kolekcie — automatické sťahovanie a monitorovanie filmov cez Usenet / BitTorrent.

## O add-one

Postavený na [LinuxServer.io](https://docs.linuxserver.io/images/docker-radarr/) image-och. Podporuje **HA Ingress** aj **externý port 7878**.

## Inštalácia

1. Pridaj repozitár `https://github.com/halali/ha-apps`.
2. Nainštaluj **Radarr** zo store.
3. Spusti a otvor cez sidebar.

## Konfigurácia

```yaml
PUID: 0
PGID: 0
TZ: Europe/Bratislava
reset_auth: false
```

## Cesty

| HA cesta | Kontajner | Popis |
|----------|-----------|-------|
| `/addon_configs/<slug>_radarr` | `/config` | Databáza, nastavenia |
| `/media` | `/media` | Filmy |
| `/share` | `/share` | Zdieľané dáta |

## Externý port

- `7878/tcp` — Web UI a API.
