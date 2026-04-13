#!/bin/sh
# shellcheck shell=sh
# HA init entrypoint for Seerr add-on.
#
# Responsibilities:
#   1. Bridge /config (HA addon_config mount) → /app/config (Seerr's expected path)
#   2. Ensure required subdirectories and marker file exist
#   3. Detect and log Overseerr migration status
#   4. Fix ownership so the node user (UID 1000) can read/write config
#   5. Drop privileges and exec Seerr (npm start)
set -e

HA_CONFIG="/config"
APP_CONFIG="/app/config"

# ── 1. Config path bridge ────────────────────────────────────────────────────
# HA Supervisor mounts addon_config as /config.
# Seerr expects its config at /app/config — remove the image placeholder and
# replace it with a symlink to HA's mount point.
if [ ! -L "$APP_CONFIG" ]; then
    rm -rf "$APP_CONFIG"
    ln -sf "$HA_CONFIG" "$APP_CONFIG"
    echo "[ha-seerr] Linked $APP_CONFIG → $HA_CONFIG"
fi

# ── 2. Required structure ────────────────────────────────────────────────────
mkdir -p "$HA_CONFIG/db" "$HA_CONFIG/logs"
# DOCKER marker tells Seerr it is running in a container
touch "$HA_CONFIG/DOCKER"

# ── 3. Migration detection ───────────────────────────────────────────────────
if [ -f "$HA_CONFIG/settings.json" ]; then
    echo "[ha-seerr] Existing config detected."
    # Seerr automatically detects whether this is an Overseerr or Jellyseerr
    # database and runs the appropriate migrations on startup — no manual steps needed.
    echo "[ha-seerr] Seerr will auto-migrate Overseerr/Jellyseerr data if needed."
else
    echo "[ha-seerr] No existing config — fresh install."
    echo "[ha-seerr] Migrating from Overseerr addon?"
    echo "[ha-seerr]   Stop the Overseerr addon, then copy its config data into"
    echo "[ha-seerr]   this addon's config folder via HA File Manager or Terminal:"
    echo "[ha-seerr]   /addon_configs/<overseerr-slug>/  →  /addon_configs/<seerr-slug>/"
    echo "[ha-seerr]   Seerr will auto-migrate the data on next start."
fi

# ── 4. Permissions ───────────────────────────────────────────────────────────
# Seerr runs as node (UID/GID 1000). HA mounts /config root-owned — fix it.
chown -R node:node "$HA_CONFIG"

# ── 5. Start Seerr ───────────────────────────────────────────────────────────
echo "[ha-seerr] Starting Seerr ${COMMIT_TAG:-}..."
exec su-exec node npm start
