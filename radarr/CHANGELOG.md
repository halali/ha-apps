# Changelog

## 6.3.0.10514.6

- Fix every poster and fanart being a grey placeholder over Ingress. The UI
  uses the image URL exactly as the API hands it over -- `MovieImage.tsx`
  reads `image?.url ?? image?.remoteUrl` and only swaps the size suffix, it
  never prepends `urlBase`. *arr bakes its own `UrlBase` into that URL
  server-side, and this add-on keeps `UrlBase` empty so direct port access
  stays clean for Bazarr and Seerr, so the browser got `/MediaCover/...`,
  resolved it against the Home Assistant origin and 404ed. nginx now
  prefixes those paths in the API responses; on direct port access the
  ingress path is empty and the rewrite is a no-op.

- Actually apply the `PUID`/`PGID` options. The previous release added an s6
  oneshot for this, which could never have worked: `S6_KEEP_ENV=1` makes
  s6's `with-contenv` skip its envdir and pass the inherited process
  environment straight through, so nothing started under s6 can change what
  `init-adduser` reads. The options are now read by an entrypoint wrapper
  that runs before `/init`. The image still defaults both to 0.

## 6.3.0.10514.5

- Make the `PUID`/`PGID` options actually do something. They were declared in
  the schema and written to `options.json`, but no script or Dockerfile ever
  read them, so the container kept the LinuxServer default uid 911 whatever was
  configured. `/media` is a bind mount of a root-owned CIFS share with
  `dir_mode 0755`, so that uid could read and traverse it but never write,
  and every import failed with `Access to the path '...' is denied` even
  though the source file read fine. The image now defaults `PUID`/`PGID` to 0, and a new
  `init-ha-puid` oneshot ordered ahead of LinuxServer's `init-adduser` applies
  whatever the options hold. Both the wiring and the oneshot fall back to that
  default rather than blocking start-up.

## 6.3.0.10514.4

- Pass the real `Host` through to the app. nginx was sending its own default
  `$proxy_host` — literally `127.0.0.1:7879` — so every absolute URL the app
  built for a peer that does not send `X-Forwarded-Host` (Prowlarr's app sync,
  Bazarr, another *arr) pointed at a port that does not exist in that peer's
  container. Ingress was never affected, because Supervisor sets
  `X-Forwarded-Host` on ingress requests and the app prefers it.

## 6.3.0.10514.3

- Fix the initialize.json rewrite actually matching: *arr pretty-prints that
  response, so the real bytes are `"urlBase": ""` with a space after the
  colon and the previous compact-form filter never fired.

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
