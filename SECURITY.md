# Security Policy

## Reporting a Vulnerability

If you believe you have found a security vulnerability in any of the add-ons in this repository, **please do not open a public issue**.

Instead, report it privately via GitHub's built-in advisory workflow:

1. Go to <https://github.com/halali/ha-apps/security/advisories/new>.
2. Describe the issue, affected add-on(s), and a proof of concept if available.
3. We will acknowledge receipt within 7 days.

Alternatively, email the maintainer at the address listed in `repository.yaml`.

## Scope

This repository packages upstream applications (Sonarr, Radarr, Bazarr, Prowlarr, Seerr) into Home Assistant add-ons. Vulnerabilities in the **upstream applications** themselves should be reported to the upstream projects:

- Sonarr / Radarr / Bazarr / Prowlarr — via [LinuxServer.io](https://www.linuxserver.io/) and the upstream *arr projects.
- Seerr — via <https://github.com/seerr-team/seerr>.

In scope for this repository:

- Add-on packaging (Dockerfiles, init scripts, nginx ingress configs).
- HA configuration exposed to users (`config.yaml`, options schema).
- The version-update GitHub Action and any other workflows.

## Supported Versions

Only the latest published version of each add-on receives security updates. Pinning to older versions is at your own risk — upstream containers are tagged for reproducibility, but old base images quickly accumulate unpatched OS-level CVEs.
