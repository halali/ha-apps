#!/usr/bin/env bash
# shellcheck shell=bash
# Block until a TCP endpoint accepts connections (bounded), then return.
# Usage: afw-wait.sh HOST PORT [LABEL]
set -u
host="$1"; port="$2"; label="${3:-${1}:${2}}"
for _ in $(seq 1 180); do
    if (exec 3<>"/dev/tcp/${host}/${port}") 2>/dev/null; then
        exec 3>&- 3<&-
        exit 0
    fi
    sleep 1
done
echo "[appflowy] timed out waiting for ${label}" >&2
exit 1
