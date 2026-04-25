#!/usr/bin/with-contenv bash
# shellcheck shell=bash
# Init script for Tautulli inside HA add-on.
# Patches Tautulli/config.ini under [General] so the WebUI works behind nginx:
# - Bind to 0.0.0.0 on the internal port.
# - http_proxy = 1 makes Tautulli respect X-Forwarded-* headers.
# - http_root empty — nginx strips the ingress prefix.

set -e

CONF="/config/config.ini"

for _ in $(seq 1 30); do
  [[ -f "$CONF" ]] && break
  sleep 1
done

if [[ ! -f "$CONF" ]]; then
  echo "[ha-config] Tautulli config.ini not found yet — first run."
  exit 0
fi

set_general() {
  local key="$1"
  local value="$2"
  if grep -q "^\[General\]" "$CONF"; then
    if grep -qE "^${key}\s*=" "$CONF"; then
      sed -i "s|^${key}\s*=.*|${key} = ${value}|" "$CONF"
    else
      sed -i "/^\[General\]/a ${key} = ${value}" "$CONF"
    fi
  else
    printf '\n[General]\n%s = %s\n' "$key" "$value" >> "$CONF"
  fi
}

echo "[ha-config] Adjusting Tautulli config.ini for HA Ingress..."
set_general http_host "0.0.0.0"
set_general http_port "8182"
set_general http_root ""
set_general http_proxy "1"
set_general enable_https "0"

echo "[ha-config] Done."
