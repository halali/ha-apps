ARG BUILD_FROM
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

ENV LANG=C.UTF-8 \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_KEEP_ENV=1 \
    HOME=/config

# LinuxServer base uses /config as data volume; we remap it to HA's /config
# so user data persists in /addon_configs/<slug>/sonarr.
# HA maps /addon_configs/<slug> as /config inside the container.

# Copy custom s6-overlay init scripts (URL base + auth handling)
COPY rootfs/ /

# LSIO images already expose 8989; keep it documented
EXPOSE 8989

# Labels
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION
LABEL \
    io.hass.name="Sonarr" \
    io.hass.description="Smart PVR for TV series" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="Halali" \
    org.opencontainers.image.title="Sonarr" \
    org.opencontainers.image.source="https://github.com/halali/ha-apps" \
    org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.revision="${BUILD_REF}" \
    org.opencontainers.image.version="${BUILD_VERSION}"
