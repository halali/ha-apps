# Changelog

## 2.5.2.5491.5

- Make the `PUID`/`PGID` options actually do something. They were declared in
  the schema and written to `options.json`, but no script or Dockerfile ever
  read them, so the container kept the LinuxServer default uid 911 whatever was
  configured. The image now defaults `PUID`/`PGID` to 0, and a new
  `init-ha-puid` oneshot ordered ahead of LinuxServer's `init-adduser` applies
  whatever the options hold. Both the wiring and the oneshot fall back to that
  default rather than blocking start-up.

## 2.5.2.5491.4

- Fix Radarr/Sonarr/Lidarr failing to grab any release with
  `Connection refused (127.0.0.1:9697)`. nginx never set an upstream `Host`
  header, so Prowlarr saw nginx's default `$proxy_host` — its own internal
  port — and built the `downloadUrl` of every search result from it. The peer
  then tried to fetch that URL inside its *own* container, where nothing
  listens on 9697. Indexer settings were correct all along and search kept
  working, which made this look like a download-client fault. Ingress was
  never affected, because Supervisor sets `X-Forwarded-Host`.

## 2.5.2.5491.3

- Fix the initialize.json rewrite actually matching: *arr pretty-prints that
  response, so the real bytes are `"urlBase": ""` with a space after the
  colon and the previous compact-form filter never fired.

## 2.5.2.5491.2

- Fix HA Ingress blank page, part two: the entry bundle overwrites
  `window.<App>` with `initialize.json` and takes the webpack public path
  from there, so rewriting the HTML alone left `urlBase` empty again and
  the lazy chunks still 404ed. nginx now prefixes `urlBase` and `apiRoot`
  in that response too.

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
