# Changelog

## 2.5.2.5491.1

- Fix HA Ingress: the web UI rendered a blank page in the sidebar. The app
  served root-relative asset paths (`/index-*.js`, `/Content/...`) and
  `urlBase: ''`, so the browser requested them from Home Assistant itself
  instead of the add-on and got 404s. nginx now prefixes them with the
  per-request ingress path. Direct port access is unchanged.

## 2.5.2.5491

- Bumped LinuxServer.io `prowlarr` to `2.5.2.5491` (auto-update).

## 2.4.0.5397

- Bumped LinuxServer.io `prowlarr` to `2.4.0.5397` (auto-update).

## 2.3.5.5327

- Bumped LinuxServer.io `prowlarr` to `2.3.5.5327` (auto-update).
