# Changelog

## 3.1.0.4875.4

- Pass the real `Host` through to the app. nginx was sending its own default
  `$proxy_host` — literally `127.0.0.1:8687` — so every absolute URL the app
  built for a peer that does not send `X-Forwarded-Host` (Prowlarr's app sync,
  Bazarr, another *arr) pointed at a port that does not exist in that peer's
  container. Ingress was never affected, because Supervisor sets
  `X-Forwarded-Host` on ingress requests and the app prefers it.

## 3.1.0.4875.3

- Fix the initialize.json rewrite actually matching: *arr pretty-prints that
  response, so the real bytes are `"urlBase": ""` with a space after the
  colon and the previous compact-form filter never fired.

## 3.1.0.4875.2

- Fix HA Ingress blank page, part two: the entry bundle overwrites
  `window.<App>` with `initialize.json` and takes the webpack public path
  from there, so rewriting the HTML alone left `urlBase` empty again and
  the lazy chunks still 404ed. nginx now prefixes `urlBase` and `apiRoot`
  in that response too.

## 3.1.0.4875.1

- Fix HA Ingress: the web UI rendered a blank page in the sidebar. The app
  served root-relative asset paths (`/index-*.js`, `/Content/...`) and
  `urlBase: ''`, so the browser requested them from Home Assistant itself
  instead of the add-on and got 404s. nginx now prefixes them with the
  per-request ingress path. Direct port access is unchanged.

## 3.1.0.4875

- Initial release — LinuxServer.io base, HA Ingress, external port 8686.
