# Changelog

## 4.0.19.2979.1

- Fix HA Ingress: the web UI rendered a blank page in the sidebar. The app
  served root-relative asset paths (`/index-*.js`, `/Content/...`) and
  `urlBase: ''`, so the browser requested them from Home Assistant itself
  instead of the add-on and got 404s. nginx now prefixes them with the
  per-request ingress path. Direct port access is unchanged.

## 4.0.19.2979

- Bumped LinuxServer.io `sonarr` to `4.0.19.2979` (auto-update).

## 4.0.18.2971

- Bumped LinuxServer.io `sonarr` to `4.0.18.2971` (auto-update).

## 4.0.17.2952

- Bumped LinuxServer.io `sonarr` to `4.0.17.2952` (auto-update).

## 4.0.10.2544

- Initial release — LinuxServer.io base, HA Ingress, external port 8989.
