#!/usr/bin/with-contenv bash
# shellcheck shell=bash
# Init script for SABnzbd inside HA add-on.
# Patches sabnzbd.ini so the WebUI works behind HA Ingress:
# - Bind to 0.0.0.0 on the internal port.
# - Disable HTTPS (TLS terminated at HA edge / nginx).
# - Empty url_base — nginx strips the ingress prefix.
# - host_whitelist set wide enough to accept the proxy Host header.

set -e

CONF="/config/sabnzbd.ini"

for _ in $(seq 1 30); do
  [[ -f "$CONF" ]] && break
  sleep 1
done

if [[ ! -f "$CONF" ]]; then
  echo "[ha-config] sabnzbd.ini not found yet — first run, will reconfigure on next start."
  exit 0
fi

set_misc() {
  local key="$1"
  local value="$2"
  if grep -q "^\[misc\]" "$CONF"; then
    if grep -qE "^${key}\s*=" "$CONF"; then
      sed -i "s|^${key}\s*=.*|${key} = ${value}|" "$CONF"
    else
      sed -i "/^\[misc\]/a ${key} = ${value}" "$CONF"
    fi
  else
    printf '\n[misc]\n%s = %s\n' "$key" "$value" >> "$CONF"
  fi
}

echo "[ha-config] Adjusting sabnzbd.ini for HA Ingress..."
set_misc host "0.0.0.0"
set_misc port "8086"
set_misc enable_https "0"
set_misc url_base ""
set_misc host_whitelist "localhost,127.0.0.1,homeassistant.local"
set_misc inet_exposure "4"

echo "[ha-config] Done."
