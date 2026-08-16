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

# Order init-ha-puid ahead of LinuxServer's init-adduser so the PUID/PGID it
# reads have already been taken from the add-on options. Guarded on purpose: if
# the base image ever drops init-adduser, the oneshot is deleted instead of
# being left half-wired, because a malformed s6-rc service fails the compile and
# the add-on would then not start at all. The ENV above still applies.
RUN set -eu; \
    d=/etc/s6-overlay/s6-rc.d; \
    if [ -d "$d/init-adduser" ] && [ -f "$d/init-ha-puid/run" ]; then \
        mkdir -p "$d/init-adduser/dependencies.d"; \
        touch "$d/init-adduser/dependencies.d/init-ha-puid"; \
        chmod 0755 "$d/init-ha-puid/run"; \
        echo "[build] init-ha-puid wired ahead of init-adduser"; \
    else \
        rm -rf "$d/init-ha-puid"; \
        echo "[build] init-adduser absent; relying on ENV PUID/PGID"; \
    fi


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
