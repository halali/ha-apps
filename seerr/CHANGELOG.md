# Changelog

## 3.3.0.6

- Experiment: all injected runtime patches (fetch / XHR / script.src /
  crypto polyfill) disabled, diagnostics kept, to test whether the shim is
  what prevents React from hydrating under ingress. Temporary.

## 3.3.0.5

- Diagnostics now report through `document.title` instead of network pings,
  which the browser tooling drops on navigation. Still temporary.

## 3.3.0.4

- Temporary diagnostic build. Adds click / window.open / error tracing to the
  injected ingress shim so the Plex login failure can be traced from the
  network log. No behaviour change; to be removed once the cause is known.

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
