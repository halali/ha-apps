# Changelog

## 3.3.0.3

- Revert the 3.3.0.2 buffering change. It was based on a bad measurement:
  the page looked truncated only because the tool used to inspect it caps
  responses at 50 kB. The real page is 298 kB, its `__NEXT_DATA__` parses
  fine and does carry `plexClientIdentifier`. Forcing `proxy_buffering on`
  and ignoring `X-Accel-Buffering` fixed nothing and risked breaking Seerr's
  streamed responses.

## 3.3.0

- Bumped upstream `seerr-team/seerr` to `v3.3.0` (auto-update).

## 3.2.0

- Initial release — Seerr v3.2.0 (Overseerr fork with Jellyfin/Emby support).
- HA Ingress with Next.js path rewriting, external port 5055.
- Automatic Overseerr config migration on first start.
