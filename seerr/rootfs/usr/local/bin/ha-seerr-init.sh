#!/bin/sh
# shellcheck shell=sh
# HA init entrypoint for Seerr add-on.
#
# CONFIG_DIRECTORY=/config (set in Dockerfile) tells Seerr to use /config
# directly — no symlink needed. HA Supervisor mounts addon_config as /config.
set -e

# ── Required structure ───────────────────────────────────────────────────────
mkdir -p /config/db /config/logs

# ── Migration detection ──────────────────────────────────────────────────────
if [ -f "/config/settings.json" ]; then
    echo "[ha-seerr] Existing config detected. Seerr will auto-migrate Overseerr/Jellyseerr data if needed."
else
    echo "[ha-seerr] Fresh install."
    echo "[ha-seerr] Migrating from Overseerr? Copy /addon_configs/<overseerr-slug>/ contents here first."
fi

# ── Permissions ──────────────────────────────────────────────────────────────
# Seerr runs as node (UID/GID 1000). HA mounts /config root-owned.
chown -R node:node /config

# ── Start ────────────────────────────────────────────────────────────────────
echo "[ha-seerr] Starting Seerr ${COMMIT_TAG:-}..."
exec su-exec node npm start
