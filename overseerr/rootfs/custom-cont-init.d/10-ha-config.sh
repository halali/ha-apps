#!/usr/bin/with-contenv bash
# shellcheck shell=bash
# Init script for Overseerr inside HA add-on.
# Overseerr uses /config/settings.json. Ensure trustProxy is enabled so
# the X-Forwarded-* headers set by HA Ingress are respected.
set -e

SETTINGS="/config/settings.json"

for _ in $(seq 1 30); do
  [[ -f "$SETTINGS" ]] && break
  sleep 1
done

if [[ ! -f "$SETTINGS" ]]; then
  exit 0
fi

echo "[ha-config] Ensuring Overseerr trusts HA reverse proxy..."

# Use jq to flip trustProxy to true
tmp="$(mktemp)"
jq '.main.trustProxy = true' "$SETTINGS" > "$tmp" && mv "$tmp" "$SETTINGS"

echo "[ha-config] Done."
