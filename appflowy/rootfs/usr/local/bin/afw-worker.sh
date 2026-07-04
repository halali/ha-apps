#!/usr/bin/env bash
# shellcheck shell=bash
# AppFlowy background worker (imports, notifications).
set -eu
/usr/local/bin/afw-wait.sh 127.0.0.1 5432 postgres
/usr/local/bin/afw-wait.sh 127.0.0.1 6379 redis
/usr/local/bin/afw-wait.sh 127.0.0.1 8000 appflowy_cloud
set -a
# shellcheck disable=SC1091
. /etc/appflowy/appflowy.env
set +a
exec appflowy_worker
