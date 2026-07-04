# Changelog

## 0.16.5.1

- Fixed a runtime crash (`GLIBC_2.39 not found`) — the AppFlowy binaries are
  built against glibc 2.39, so the base image was moved from Debian bookworm
  (glibc 2.36) to `pgvector/pgvector:pg16-trixie` (glibc 2.41).

## 0.16.5

- Initial release — self-hosted **AppFlowy Cloud** `0.16.5` as an all-in-one add-on.
- Bundles PostgreSQL 16 + pgvector, Redis, MinIO, GoTrue, the AppFlowy Cloud API
  and the background worker behind an nginx gateway, managed by supervisord.
- External port `9080` for desktop/mobile clients; the HA Ingress sidebar button
  opens a status/landing page.
- The browser UI (admin console / web editor) and AI/search services are not
  bundled — the desktop and mobile apps connect to the API directly.
- Secrets (JWT, database and object-storage credentials) are generated on first
  start and persisted under `/addon_configs/appflowy`.
