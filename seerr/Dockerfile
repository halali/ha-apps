ARG BUILD_FROM
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Switch to root for setup — dropped back to node via su-exec in entrypoint
USER root

# nginx: reverse proxy with sub_filter for Next.js path rewriting
# jq: parse HA Supervisor API response for ingress_entry
# su-exec: privilege drop to node user (UID 1000)
# hadolint ignore=DL3018
RUN apk add --no-cache nginx jq su-exec

# Seerr config dir: HA mounts addon_config as /config
ENV CONFIG_DIRECTORY=/config
# Seerr internal port — nginx listens on 5055 and proxies here
ENV PORT=5056

# Copy nginx ingress config template and init entrypoint
COPY rootfs/ /
RUN chmod +x /usr/local/bin/ha-seerr-init.sh

EXPOSE 5055

ENTRYPOINT ["/usr/local/bin/ha-seerr-init.sh"]

ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION
LABEL \
    io.hass.name="Seerr" \
    io.hass.description="Media request manager — Plex, Jellyfin, Emby" \
    io.hass.arch="amd64" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="Halali" \
    org.opencontainers.image.title="Seerr" \
    org.opencontainers.image.source="https://github.com/halali/ha-apps" \
    org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.revision="${BUILD_REF}" \
    org.opencontainers.image.version="${BUILD_VERSION}"
