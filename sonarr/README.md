# Home Assistant Add-on: Sonarr

Smart PVR pre TV seriály. Sleduje RSS feedy tvojho indexera a automaticky sťahuje nové epizódy.

## O add-one

Postavený na [LinuxServer.io](https://docs.linuxserver.io/images/docker-sonarr/) image-och. Podporuje **HA Ingress** (tlačítko v sidebare) aj **externý port 8989** (pre mobilnú app, integráciu s Overseerr, Bazarr).

## Inštalácia

1. Uisti sa, že máš pridaný repozitár `https://github.com/halali/ha-apps`.
2. V **Settings → Add-ons → Add-on Store** nájdi **Sonarr** a klikni **Install**.
3. Spusti add-on a klikni **Open Web UI** v sidebare.

## Konfigurácia

```yaml
PUID: 0
PGID: 0
TZ: Europe/Bratislava
reset_auth: false
```

- **PUID / PGID** — user ID, pod ktorým beží Sonarr. Pre prístup k `/media` možno budeš chcieť 1000.
- **TZ** — timezone pre plánovanie.
- **reset_auth** — ak `true`, pri štarte deaktivuje autentifikáciu (užitočné keď používaš iba Ingress a nechceš dvojité prihlasovanie).

## Cesty

| HA cesta | Cesta v kontajneri | Použitie |
|----------|---------------------|----------|
| `/addon_configs/<slug>_sonarr` | `/config` | Databáza, nastavenia, logy |
| `/media` | `/media` | TV seriály |
| `/share` | `/share` | Zdieľané dáta |

Sťahovacie adresáre (torrenty, usenet) si namapuj do `/share` alebo `/media`.

## Externý port

- `8989/tcp` — Web UI a API.

Používaj tento port pre mobilnú **Sonarr** app, **Overseerr** integráciu, **Bazarr** integráciu atď.

## API kľúč

API kľúč nájdeš v Sonarr **Settings → General → API Key**.
