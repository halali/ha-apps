#!/bin/bash
# Bridge Home Assistant's add-on options into the environment before s6 starts.
#
# HA writes the add-on options to /data/options.json, but the LinuxServer base
# reads PUID/PGID from the *environment*, in its init-adduser service. And
# because this image sets S6_KEEP_ENV=1, s6's with-contenv skips its envdir
# altogether and hands every service the inherited process environment:
#
#   ifelse
#     importas -D 0 S6_KEEP_ENV S6_KEEP_ENV
#     eltest 0${S6_KEEP_ENV} -eq 0
#     emptyenv -p
#     s6-envdir -Lfn -- /run/s6/container_environment
#     exec $@
#
# That is why /run/s6/container_environment does not even exist here, and why
# no service started later can change what init-adduser goes on to read. The
# value has to be in place before /init runs -- hence this entrypoint.
#
# Getting it wrong is not cosmetic. The LinuxServer default is uid 911, and HA
# mounts /media from a root-owned CIFS share with dir_mode 0755, where 911 can
# read and traverse but never write. Imports failed with
#
#   UnauthorizedAccessException: Access to the path
#   '/media/NAS/series/Reacher/Season 4' is denied.
#
# while reading the finished download perfectly well.
#
# Deliberately tolerant: a missing or malformed options.json leaves the
# Dockerfile's PUID/PGID=0 standing rather than stopping the add-on.
set -u

if [ -f /data/options.json ]; then
    for _var in PUID PGID; do
        _value="$(jq -r --arg k "$_var" '.[$k] // empty' /data/options.json 2>/dev/null || true)"
        case "${_value}" in
            "" | *[!0-9]*) ;;
            *) export "${_var}=${_value}"; echo "[ha-puid] ${_var}=${_value}" ;;
        esac
    done
else
    echo "[ha-puid] no /data/options.json; keeping image default PUID=${PUID:-unset}"
fi

exec /init "$@"
