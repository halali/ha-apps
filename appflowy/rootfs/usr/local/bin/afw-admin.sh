#!/usr/bin/env bash
# shellcheck shell=bash
# AppFlowy admin console (web sign-in / workspace management) on :3000.
# Runs from /app so it can locate its bundled ./assets directory.
set -eu
/usr/local/bin/afw-wait.sh 127.0.0.1 9999 gotrue
/usr/local/bin/afw-wait.sh 127.0.0.1 8000 appflowy_cloud
set -a
# shellcheck disable=SC1091
. /etc/appflowy/appflowy.env
set +a
export PORT=3000
export ADMIN_FRONTEND_PORT=3000
cd /app
exec admin_frontend
