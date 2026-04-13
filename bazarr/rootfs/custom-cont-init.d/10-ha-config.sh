#!/usr/bin/with-contenv bash
# shellcheck shell=bash
# Init script for Bazarr inside HA add-on.
# Bazarr uses config.ini (INI format). Ensure base_url is empty and bind 0.0.0.0.
set -e

CONFIG_INI="/config/config/config.ini"

for _ in $(seq 1 30); do
  [[ -f "$CONFIG_INI" ]] && break
  sleep 1
done

if [[ ! -f "$CONFIG_INI" ]]; then
  # First run — let Bazarr create it.
  exit 0
fi

echo "[ha-config] Adjusting Bazarr config.ini for HA Ingress..."

python3 - <<'PY'
import configparser, os
path = "/config/config/config.ini"
cp = configparser.ConfigParser()
cp.read(path)
if not cp.has_section("general"):
    cp.add_section("general")
cp.set("general", "base_url", "")
cp.set("general", "ip", "0.0.0.0")
cp.set("general", "port", "6768")
with open(path, "w") as f:
    cp.write(f)
PY

echo "[ha-config] Done."
