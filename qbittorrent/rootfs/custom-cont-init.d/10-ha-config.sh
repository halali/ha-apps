#!/usr/bin/with-contenv bash
# shellcheck shell=bash
# Init script for qBittorrent inside HA add-on.
# Patches qBittorrent.conf so the WebUI works behind HA Ingress:
# - Disable Host header validation and CSRF (we're behind nginx).
# - Disable LocalHostAuth so the nginx proxy can talk without login.
# - Optional: whitelist common Docker/LAN subnets so the user is not
#   re-prompted for credentials when using HA Ingress.

set -e

CONF="/config/qBittorrent/qBittorrent.conf"

# Wait until LSIO has created the config (first launch may take a few seconds)
for _ in $(seq 1 30); do
  [[ -f "$CONF" ]] && break
  sleep 1
done

if [[ ! -f "$CONF" ]]; then
  echo "[ha-config] qBittorrent.conf not found yet — first run, will reconfigure on next start."
  exit 0
fi

TRUST_SUBNETS="true"
if [[ -f /data/options.json ]]; then
  TRUST_SUBNETS="$(jq -r '.trust_subnets // true' /data/options.json 2>/dev/null || echo "true")"
fi

# Helper: set a key=value pair under [Preferences]; create section if missing.
set_pref() {
  local key="$1"
  local value="$2"
  # Escape backslash and slashes for sed
  local esc_key
  esc_key=$(printf '%s' "$key" | sed 's/[\\\/]/\\&/g')
  if grep -q "^\[Preferences\]" "$CONF"; then
    if grep -qE "^${esc_key}=" "$CONF"; then
      sed -i "s|^${esc_key}=.*|${key}=${value}|" "$CONF"
    else
      sed -i "/^\[Preferences\]/a ${key}=${value}" "$CONF"
    fi
  else
    printf '\n[Preferences]\n%s=%s\n' "$key" "$value" >> "$CONF"
  fi
}

echo "[ha-config] Adjusting qBittorrent.conf for HA Ingress..."
set_pref "WebUI\\Address" "*"
set_pref "WebUI\\Port" "8081"
set_pref "WebUI\\HostHeaderValidation" "false"
set_pref "WebUI\\CSRFProtection" "false"
set_pref "WebUI\\LocalHostAuth" "false"
set_pref "WebUI\\HTTPS\\Enabled" "false"

if [[ "${TRUST_SUBNETS}" == "true" ]]; then
  set_pref "WebUI\\AuthSubnetWhitelistEnabled" "true"
  set_pref "WebUI\\AuthSubnetWhitelist" "127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
else
  set_pref "WebUI\\AuthSubnetWhitelistEnabled" "false"
fi

echo "[ha-config] Done."
