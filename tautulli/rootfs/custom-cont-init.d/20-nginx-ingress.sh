#!/usr/bin/with-contenv bash
# shellcheck shell=bash
# Configure and start nginx ingress proxy.
set -e

INGRESS_ENTRY=""
if [[ -n "${SUPERVISOR_TOKEN:-}" ]]; then
    ADDON_INFO=$(wget -q -O- \
        --header="Authorization: Bearer ${SUPERVISOR_TOKEN}" \
        "http://supervisor/addons/self/info" 2>/dev/null || true)
    if [[ -n "$ADDON_INFO" ]]; then
        INGRESS_ENTRY=$(echo "$ADDON_INFO" | jq -r '.data.ingress_entry // ""' 2>/dev/null || true)
    fi
fi

echo "[nginx] Ingress entry: ${INGRESS_ENTRY:-/}"
sed -i "s|__INGRESS_ENTRY__|${INGRESS_ENTRY}|g" /etc/nginx/http.d/ingress.conf

nginx
echo "[nginx] Started."
