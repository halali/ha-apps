#!/usr/bin/env bash
# shellcheck shell=bash
# AppFlowy Cloud API — waits for its backing services, then serves on :8000.
set -eu
/usr/local/bin/afw-wait.sh 127.0.0.1 5432 postgres
/usr/local/bin/afw-wait.sh 127.0.0.1 6379 redis
/usr/local/bin/afw-wait.sh 127.0.0.1 9000 minio
/usr/local/bin/afw-wait.sh 127.0.0.1 9999 gotrue
set -a
# shellcheck disable=SC1091
. /etc/appflowy/appflowy.env
set +a
exec appflowy_cloud
