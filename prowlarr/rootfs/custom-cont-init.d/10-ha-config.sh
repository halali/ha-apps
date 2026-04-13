#!/usr/bin/with-contenv bash
# shellcheck shell=bash
# Init script for Prowlarr inside HA add-on.
# - Ensures UrlBase is empty (HA Ingress handles paths).
# - Optionally resets auth when reset_auth=true in add-on options.
set -e

CONFIG_XML="/config/config.xml"

# Wait until Prowlarr's own init created the config
for _ in $(seq 1 30); do
  [[ -f "$CONFIG_XML" ]] && break
  sleep 1
done

if [[ ! -f "$CONFIG_XML" ]]; then
  # First run — let Prowlarr create it, we'll adjust on next boot.
  exit 0
fi

RESET_AUTH="false"
if [[ -f /data/options.json ]]; then
  RESET_AUTH="$(jq -r '.reset_auth // false' /data/options.json 2>/dev/null || echo "false")"
fi

echo "[ha-config] Adjusting Prowlarr config.xml for HA Ingress..."

set_xml() {
  local key="$1"
  local value="$2"
  if grep -q "<${key}>" "$CONFIG_XML"; then
    sed -i "s|<${key}>.*</${key}>|<${key}>${value}</${key}>|" "$CONFIG_XML"
  else
    sed -i "s|</Config>|  <${key}>${value}</${key}>\n</Config>|" "$CONFIG_XML"
  fi
}

set_xml UrlBase ""
set_xml BindAddress "*"
set_xml Port "9697"
set_xml EnableSsl "False"

if [[ "${RESET_AUTH}" == "true" ]]; then
  echo "[ha-config] Resetting auth to None."
  set_xml AuthenticationMethod "None"
  set_xml AuthenticationRequired "DisabledForLocalAddresses"
fi

echo "[ha-config] Done."
