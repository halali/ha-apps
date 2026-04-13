ARG BUILD_FROM
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Switch to root for setup — dropped back to node via su-exec in entrypoint
USER root

# su-exec: minimal privilege-drop tool for Alpine
RUN apk add --no-cache su-exec

# Copy HA init entrypoint
COPY rootfs/usr/local/bin/ha-seerr-init.sh /usr/local/bin/ha-seerr-init.sh
RUN chmod +x /usr/local/bin/ha-seerr-init.sh

EXPOSE 5055

# Override Seerr's default CMD — our init script handles setup then execs npm start
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
