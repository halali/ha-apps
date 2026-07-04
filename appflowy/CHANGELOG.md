# Changelog

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
