ARG BUILD_FROM
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

RUN apk add --no-cache nginx jq

ENV LANG=C.UTF-8 \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_KEEP_ENV=1 \
    HOME=/config

# The LinuxServer base runs as uid/gid 911 (abc) unless told otherwise. HA's
# /media is a bind mount of a root-owned CIFS share with dir_mode 0755, so any
# other uid can read it but not write -- that is what broke every import with
# "Access to the path ... is denied". init-ha-puid (below) overrides these from
# the add-on options; this is the fallback if that oneshot is ever skipped.
ENV PUID=0 \
    PGID=0

COPY rootfs/ /

# PUID/PGID must be in the environment before /init hands off to s6, so the
# add-on options are read here rather than by any later service. See the
# script for why an s6 service cannot do this while S6_KEEP_ENV=1 is set.
ENTRYPOINT ["/usr/local/bin/ha-puid-entrypoint.sh"]


EXPOSE 9696

ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION
LABEL \
    io.hass.name="Prowlarr" \
    io.hass.description="Indexer manager and proxy for *arr applications" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="Halali" \
    org.opencontainers.image.title="Prowlarr" \
    org.opencontainers.image.source="https://github.com/halali/ha-apps" \
    org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.revision="${BUILD_REF}" \
    org.opencontainers.image.version="${BUILD_VERSION}"
