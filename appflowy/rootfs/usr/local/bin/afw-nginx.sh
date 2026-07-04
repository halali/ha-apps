#!/usr/bin/env bash
# shellcheck shell=bash
# nginx gateway + HA ingress landing page. Waits for the API before accepting
# traffic so the very first request doesn't 502.
set -eu
/usr/local/bin/afw-wait.sh 127.0.0.1 8000 appflowy_cloud
/usr/local/bin/afw-wait.sh 127.0.0.1 3000 admin_frontend
exec nginx -g 'daemon off;'
