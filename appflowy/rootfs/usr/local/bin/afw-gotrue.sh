#!/usr/bin/env bash
# shellcheck shell=bash
# GoTrue: waits for PostgreSQL, then runs its bundled start.sh
# (./auth migrate → create admin user → ./auth serve) from its own workdir.
set -eu
/usr/local/bin/afw-wait.sh 127.0.0.1 5432 postgres
set -a
# shellcheck disable=SC1091
. /etc/appflowy/appflowy.env
set +a
cd /opt/gotrue
exec ./start.sh
