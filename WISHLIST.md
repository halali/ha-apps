# Wishlist — Future Add-on Candidates

Apps considered for inclusion in this repository but not (yet) shipped, with the rationale. Pull requests welcome — see [CONTRIBUTING.md](./CONTRIBUTING.md).

## Reverse proxies

| Candidate | Status | Notes |
|-----------|--------|-------|
| SWAG (LinuxServer) | Not packaged | Needs DNS + domain ownership. Conflicts with HA's own Cloudflare/Nabu Casa setup. Better as a separate VM/container. |
| Nginx Proxy Manager | Not packaged | Excellent admin UI but its login flow uses absolute paths that fight with HA Ingress. Works fine on a direct port — would only ship without ingress. |
| Caddy | Not packaged | Trivial reverse proxy, but the config-file-only approach is awkward inside an HA add-on; better delivered through HA's own `nginx_proxy` add-on. |
| Traefik | Not packaged | Designed for Docker socket discovery, which HA add-ons don't expose. Poor fit. |

## Download clients

| Candidate | Status | Notes |
|-----------|--------|-------|
| Deluge | Not packaged | qBittorrent already covers the BitTorrent slot. Easy to add later. |
| Transmission | Not packaged | Same as above. |
| NZBGet | Not packaged | Maintenance-mode upstream. SABnzbd is the recommended Usenet client. |
| Gluetun | Not packaged | VPN container that other clients route through. HA add-ons can't share network namespaces with each other, so this is best deployed alongside HA, not inside. |

## Media managers / *arr stack

| Candidate | Status | Notes |
|-----------|--------|-------|
| Readarr | Blocked upstream | LSIO only publishes `develop` / `nightly` images; upstream has no stable channel. Will add when stable resumes. |
| Whisparr | Out of scope | Adult content, intentionally excluded. |
| Mylar3 | Not packaged | Comics manager. Niche; consider adding if requested. |
| Ombi | Not packaged | Pre-Overseerr request system. Seerr already covers this need. |

## Media servers

| Candidate | Status | Notes |
|-----------|--------|-------|
| Plex | Use community add-on | Multiple well-maintained HA add-ons exist. |
| Jellyfin | Use community add-on | Has the official `jellyfin` HA add-on. |
| Emby | Use community add-on | Existing add-ons cover this. |

## Books / comics / photos

| Candidate | Status | Notes |
|-----------|--------|-------|
| Calibre-web | Not packaged | Possible follow-up. Needs `--reverse-proxy` flag and base URL handling. |
| Kavita | Not packaged | Self-hosted reader; ASP.NET base. |
| Komga | Not packaged | Comic / manga server; Java image is large. |
| Photoprism | Not packaged | Big indexer process; better on a NAS. |
| Immich | Not packaged | Multi-container application — incompatible with HA's single-image add-on model. |

## Dashboards

| Candidate | Status | Notes |
|-----------|--------|-------|
| Heimdall | Not packaged | Easy LSIO clone, but Home Assistant itself is a dashboard. |
| Homepage | Not packaged | Same as above. Consider only if there's clear demand. |
| Homarr | Not packaged | Multi-process, awkward in HA add-on. |
| Dashy | Not packaged | Static-build dashboard, simple if needed. |

## Network / security

| Candidate | Status | Notes |
|-----------|--------|-------|
| AdGuard Home | Use official | First-party HA add-on exists. |
| Pi-hole | Use community add-on | DNS port 53 conflicts with the host on most HA installs. |
| Vaultwarden | Use community add-on | Excellent existing add-on; no need to duplicate. |
| Authelia | Not packaged | Identity middleware; only useful in a public-internet setup. |
| Authentik | Not packaged | Same as above; multi-container. |
| Crowdsec | Not packaged | Needs host-network and log access — outside HA add-on sandbox. |

## Misc

| Candidate | Status | Notes |
|-----------|--------|-------|
| Uptime Kuma | Use community add-on | Mature add-ons already exist. |
| FreshRSS | Not packaged | Possible follow-up. |
| Code-server | Use community add-on | First-party VS Code add-on covers this. |
| File browser | Use community add-on | Already available. |
| Glances | Not packaged | HA already exposes system stats. |

## Why this list exists

We deliberately keep the supported set narrow to:

1. Keep the auto-update workflow honest (every shipped add-on is bumped daily).
2. Avoid shipping ingress integrations we cannot test.
3. Avoid duplicating effort on add-ons the HA community already maintains well.

If you want one of the "not packaged" entries, open a feature request linking to the upstream Docker tag and your use case.
