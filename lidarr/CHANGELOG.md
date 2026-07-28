# Changelog

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
