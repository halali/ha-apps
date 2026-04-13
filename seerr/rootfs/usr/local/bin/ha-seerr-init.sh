#!/bin/sh
# shellcheck shell=sh
# HA init entrypoint for Seerr add-on.
#
# Flow:
#   1. Create config structure, fix ownership for node user (UID 1000)
#   2. Query HA Supervisor API for ingress_entry path
#   3. Substitute ingress_entry into nginx template and start nginx
#   4. Start Seerr (runs on internal port 5056; nginx proxies 5055 → 5056)
set -e

# ── Config structure ─────────────────────────────────────────────────────────
mkdir -p /config/db /config/logs
chown -R node:node /config

# ── Overseerr migration hint ─────────────────────────────────────────────────
if [ -f "/config/settings.json" ]; then
    echo "[ha-seerr] Existing config found. Seerr will auto-migrate Overseerr/Jellyseerr data if needed."
else
    echo "[ha-seerr] Fresh install. Migrating from Overseerr? Copy its config folder contents here first."
fi

# ── Ingress entry ─────────────────────────────────────────────────────────────
# HA Supervisor provides SUPERVISOR_TOKEN; use it to fetch this addon's ingress_entry.
INGRESS_ENTRY=""
if [ -n "${SUPERVISOR_TOKEN:-}" ]; then
    ADDON_INFO=$(wget -q -O- \
        --header="Authorization: Bearer ${SUPERVISOR_TOKEN}" \
        "http://supervisor/addons/self/info" 2>/dev/null || true)
    if [ -n "$ADDON_INFO" ]; then
        INGRESS_ENTRY=$(echo "$ADDON_INFO" | jq -r '.data.ingress_entry // ""' 2>/dev/null || true)
    fi
fi
echo "[ha-seerr] Ingress entry: ${INGRESS_ENTRY:-/}"

# Escape forward slashes for sed replacement (used in the JS \/_next literal)
INGRESS_ENTRY_ESCAPED=$(printf '%s' "$INGRESS_ENTRY" | sed 's|/|\\/|g')

# Substitute placeholders in nginx template
sed -i "s|__INGRESS_ENTRY__|${INGRESS_ENTRY}|g" /etc/nginx/http.d/seerr.conf
sed -i "s|__INGRESS_ENTRY_ESCAPED__|${INGRESS_ENTRY_ESCAPED}|g" /etc/nginx/http.d/seerr.conf

# ── Start nginx ───────────────────────────────────────────────────────────────
echo "[ha-seerr] Starting nginx..."
nginx

# ── Start Seerr ───────────────────────────────────────────────────────────────
echo "[ha-seerr] Starting Seerr ${COMMIT_TAG:-}..."
exec su-exec node npm start
