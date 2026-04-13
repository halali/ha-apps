ARG BUILD_FROM
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

ENV LANG=C.UTF-8 \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_KEEP_ENV=1 \
    HOME=/config \
    PORT=5055

COPY rootfs/ /

EXPOSE 5055

ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION
LABEL \
    io.hass.name="Overseerr" \
    io.hass.description="Request management for Plex / Jellyfin" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="Halali" \
    org.opencontainers.image.title="Overseerr" \
    org.opencontainers.image.source="https://github.com/halali/ha-apps" \
    org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.revision="${BUILD_REF}" \
    org.opencontainers.image.version="${BUILD_VERSION}"
