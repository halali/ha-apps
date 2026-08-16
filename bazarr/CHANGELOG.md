# Changelog

## 1.6.0.1

- Pass the real `Host` through to the app. nginx was sending its own default
  `$proxy_host` — literally `127.0.0.1:6768` — so every absolute URL the app
  built for a peer that does not send `X-Forwarded-Host` (Prowlarr's app sync,
  Bazarr, another *arr) pointed at a port that does not exist in that peer's
  container. Ingress was never affected, because Supervisor sets
  `X-Forwarded-Host` on ingress requests and the app prefers it.

## 1.6.0

- Bumped LinuxServer.io `bazarr` to `1.6.0` (auto-update).

## 1.5.6

- Bumped LinuxServer.io `bazarr` to `1.5.6` (auto-update).

## 1.4.5

- Initial release — LinuxServer.io base, HA Ingress, external port 6767.
