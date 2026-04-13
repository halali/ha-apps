# Seerr

Open-source media request and discovery manager for Plex, Jellyfin, and Emby.
Fork of Overseerr with added Emby/Jellyfin support and active maintenance.

## Migrácia z Overseerr

Seerr automaticky migruje dáta pri prvom spustení. Postup:

1. **Zastav** Overseerr addon v HA.
2. Skopíruj obsah config adresára Overseerr addonu do config adresára Seerr addonu:
   - Cez HA **File Manager** alebo **Terminal** addon
   - Zdrojový adresár: `/addon_configs/<overseerr-slug>/`
   - Cieľový adresár: `/addon_configs/<seerr-slug>/`
3. Spusti Seerr addon — migrácia prebehne automaticky pri štarte.
4. Po overení funkčnosti môžeš odinštalovať Overseerr addon.

> Pred migráciou odporúčame zálohu: skopíruj celý adresár niekde bezpečne.
