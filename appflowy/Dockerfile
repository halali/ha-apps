ARG BUILD_FROM

# ── AppFlowy Cloud stack version ─────────────────────────────────────────────
# appflowy_cloud, appflowy_worker and gotrue are released together under the
# same version tag. Keep this in sync with config.yaml.
ARG APPFLOWY_VERSION=0.16.5

# hadolint ignore=DL3006
FROM appflowyinc/appflowy_cloud:${APPFLOWY_VERSION}-amd64 AS cloud
# hadolint ignore=DL3006
FROM appflowyinc/appflowy_worker:${APPFLOWY_VERSION}-amd64 AS worker
# hadolint ignore=DL3006
FROM appflowyinc/gotrue:${APPFLOWY_VERSION}-amd64 AS gotrue

# ── Final image: PostgreSQL 16 + pgvector (Debian bookworm) ──────────────────
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PGDATA=/config/pgdata \
    MINIO_VERSION=RELEASE.2024-09-13T20-26-02Z

# nginx        — gateway / reverse proxy (also the HA ingress landing page)
# redis-server — realtime collaboration cache
# supervisor   — process manager for the bundled services
# gosu         — privilege drop for the postgres process
# jq           — read HA add-on options from /data/options.json
# curl/openssl — health checks, secret generation, minio download
# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nginx \
        redis-server \
        supervisor \
        gosu \
        jq \
        curl \
        ca-certificates \
        openssl \
        tzdata \
    && curl -fsSL "https://dl.min.io/server/minio/release/linux-amd64/archive/minio.${MINIO_VERSION}" \
        -o /usr/local/bin/minio \
    && chmod +x /usr/local/bin/minio \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /etc/nginx/sites-enabled/default

# ── AppFlowy service binaries (copied from the official images) ──────────────
COPY --from=cloud  /usr/local/bin/appflowy_cloud  /usr/local/bin/appflowy_cloud
COPY --from=worker /usr/local/bin/appflowy_worker /usr/local/bin/appflowy_worker
# GoTrue ships as /auth + /start.sh + /migrations and runs from its own workdir
COPY --from=gotrue /auth        /opt/gotrue/auth
COPY --from=gotrue /start.sh    /opt/gotrue/start.sh
COPY --from=gotrue /migrations  /opt/gotrue/migrations

# ── Add-on rootfs (entrypoint, service wrappers, supervisor, nginx) ──────────
COPY rootfs/ /
RUN chmod +x /usr/local/bin/afw-*.sh /opt/gotrue/start.sh /opt/gotrue/auth

EXPOSE 9080
ENTRYPOINT ["/usr/local/bin/afw-entrypoint.sh"]

ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION
LABEL \
    io.hass.name="AppFlowy" \
    io.hass.description="Self-hosted AppFlowy Cloud — open-source Notion alternative" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="Halali" \
    org.opencontainers.image.title="AppFlowy" \
    org.opencontainers.image.source="https://github.com/halali/ha-apps" \
    org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.revision="${BUILD_REF}" \
    org.opencontainers.image.version="${BUILD_VERSION}"
