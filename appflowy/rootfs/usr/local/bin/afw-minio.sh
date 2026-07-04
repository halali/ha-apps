#!/usr/bin/env bash
# shellcheck shell=bash
set -eu
set -a
# shellcheck disable=SC1091
. /etc/appflowy/appflowy.env
set +a
exec minio server /config/minio-data \
    --address 127.0.0.1:9000 \
    --console-address 127.0.0.1:9001
