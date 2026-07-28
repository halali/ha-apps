# Changelog

## 3.3.0.2

- Fix the whole UI being dead under HA Ingress (Plex login, language picker,
  every control). Seerr answers with `X-Accel-Buffering: no`, which turns
  nginx's proxy buffering off; `sub_filter` then truncated the login page
  mid-response, so `__NEXT_DATA__` ended mid-string, `JSON.parse` threw and
  Next.js never hydrated. nginx now ignores that header and buffers enough
  for the ~51 kB page. Direct port access was never affected.

## 3.3.0

- Bumped upstream `seerr-team/seerr` to `v3.3.0` (auto-update).

## 3.2.0

- Initial release — Seerr v3.2.0 (Overseerr fork with Jellyfin/Emby support).
- HA Ingress with Next.js path rewriting, external port 5055.
- Automatic Overseerr config migration on first start.
