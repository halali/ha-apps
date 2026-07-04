#!/usr/bin/env bash
# shellcheck shell=bash
set -eu
export PGDATA=/config/pgdata
exec gosu postgres postgres -D "${PGDATA}" -c listen_addresses=127.0.0.1 -c port=5432
