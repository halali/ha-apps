# Changelog

## 6.3.0.10514.2

- Fix HA Ingress blank page, part two: the entry bundle overwrites
  `window.<App>` with `initialize.json` and takes the webpack public path
  from there, so rewriting the HTML alone left `urlBase` empty again and
  the lazy chunks still 404ed. nginx now prefixes `urlBase` and `apiRoot`
  in that response too.

## 6.3.0.10514.1

- Fix HA Ingress: the web UI rendered a blank page in the sidebar. The app
  served root-relative asset paths (`/index-*.js`, `/Content/...`) and
  `urlBase: ''`, so the browser requested them from Home Assistant itself
  instead of the add-on and got 404s. nginx now prefixes them with the
  per-request ingress path. Direct port access is unchanged.

## 6.3.0.10514

- Bumped LinuxServer.io `radarr` to `6.3.0.10514` (auto-update).

## 6.2.1.10461

- Bumped LinuxServer.io `radarr` to `6.2.1.10461` (auto-update).

## 6.1.1.10360

- Bumped LinuxServer.io `radarr` to `6.1.1.10360` (auto-update).

## 5.11.0.9244

- Initial release — LinuxServer.io base, HA Ingress, external port 7878.
