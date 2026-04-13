# Halali — Home Assistant Add-ons

Kolekcia Home Assistant add-onov pre populárne *arr aplikácie postavené na [LinuxServer.io](https://www.linuxserver.io/) image-och. Všetky add-ony podporujú **Home Assistant Ingress** (tlačítko v sidebare), **externý port** pre priame API a mobilné aplikácie a **automatické aktualizácie** pri vydaní novej upstream verzie.

## Inštalácia repozitára

1. V Home Assistant otvor **Settings → Add-ons → Add-on Store**.
2. Klikni na menu (tri bodky vpravo hore) → **Repositories**.
3. Pridaj URL: `https://github.com/halali/ha-apps`
4. Po chvíli sa zobrazia add-ony v store.

## Dostupné add-ony

| Add-on | Popis | Upstream |
|--------|-------|----------|
| [Sonarr](./sonarr) | Správa a sťahovanie TV seriálov | [linuxserver/sonarr](https://hub.docker.com/r/linuxserver/sonarr) |
| [Radarr](./radarr) | Správa a sťahovanie filmov | [linuxserver/radarr](https://hub.docker.com/r/linuxserver/radarr) |
| [Bazarr](./bazarr) | Automatické sťahovanie titulkov | [linuxserver/bazarr](https://hub.docker.com/r/linuxserver/bazarr) |
| [Seerr](./seerr) | Request management pre Plex/Jellyfin/Emby — nástupca Overseerr | [seerr-team/seerr](https://github.com/seerr-team/seerr) |

## Funkcie

- ✅ **HA Ingress** — otvor aplikáciu priamo z HA sidebaru, bez loginu
- ✅ **Externý port** — priamy prístup z LAN pre API klientov (napr. Overseerr ↔ Sonarr, mobilné apps)
- ✅ **Multi-arch** — `amd64`, `aarch64`, `armv7`, `armhf`
- ✅ **Auto-update** — GitHub Actions denne kontrolujú nové verzie a automaticky bumpnú add-on
- ✅ **Persistentné dáta** — konfigurácia v `/addon_configs/<slug>`, médiá v `/media`

## Podporované architektúry

Všetky add-ony podporujú: `amd64`, `aarch64`, `armv7`, `armhf`.

## Licencia

MIT © Halali
