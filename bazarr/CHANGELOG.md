# Changelog

## 1.6.0.3

- Actually apply the `PUID`/`PGID` options. The previous release added an s6
  oneshot for this, which could never have worked: `S6_KEEP_ENV=1` makes
  s6's `with-contenv` skip its envdir and pass the inherited process
  environment straight through, so nothing started under s6 can change what
  `init-adduser` reads. The options are now read by an entrypoint wrapper
  that runs before `/init`. The image still defaults both to 0.

## 1.6.0.2

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
