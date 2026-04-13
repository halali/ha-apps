ARG BUILD_FROM
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

ENV LANG=C.UTF-8 \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_KEEP_ENV=1 \
    HOME=/config

COPY rootfs/ /

EXPOSE 7878

ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION
LABEL \
    io.hass.name="Radarr" \
    io.hass.description="Movie collection manager" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="Halali" \
    org.opencontainers.image.title="Radarr" \
    org.opencontainers.image.source="https://github.com/halali/ha-apps" \
    org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.revision="${BUILD_REF}" \
    org.opencontainers.image.version="${BUILD_VERSION}"
