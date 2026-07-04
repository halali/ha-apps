# Changelog

## 0.16.5.3

- Clarified sign-in: the `GOTRUE_ADMIN_EMAIL` account is a *system admin* and
  AppFlowy blocks it from the desktop/mobile/web apps (`System admin accounts
  must use the admin console…`). The landing page and README now tell users to
  register a normal, non-admin account for everyday use. No functional change.

## 0.16.5.2

- Added the **AppFlowy web front-end** (`appflowy_web` `0.15.5`). The gateway now
  serves the browser workspace at the add-on's base URL; runtime backend URLs are
  injected into the SPA on start. Open it from the HA sidebar or `APPFLOWY_BASE_URL`.

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
