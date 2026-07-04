#!/usr/bin/env bash
# shellcheck shell=bash
set -eu
exec redis-server \
    --bind 127.0.0.1 \
    --port 6379 \
    --dir /config/redis \
    --save "" \
    --appendonly no \
    --maxmemory-policy noeviction
