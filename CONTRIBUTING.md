# Contributing

Thanks for taking the time to contribute! This repository hosts Home Assistant add-ons for the *arr stack and a couple of related apps.

## Reporting Bugs

Please use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.yml). Include:

- Add-on name and version (visible in the add-on page in HA).
- Home Assistant version and installation type (Supervised, OS, etc.).
- Architecture (amd64 / aarch64 / ...).
- Add-on logs around the failure (redact secrets/tokens).
- Steps to reproduce.

## Suggesting Features

Open a [feature request](.github/ISSUE_TEMPLATE/feature_request.yml) and describe the use case. For new add-ons, link to the upstream image (LinuxServer.io tag or GitHub release) so we can evaluate maintenance cost.

## Local Development

Each add-on lives in its own folder:

```
<addon>/
├── config.yaml          # HA add-on manifest
├── build.yaml           # Build args (base images per arch)
├── Dockerfile
├── CHANGELOG.md
├── README.md
├── icon.png
└── rootfs/              # Files copied into the image
```

### Lint Locally

```sh
# YAML
docker run --rm -v "$PWD":/data cytopia/yamllint .

# Dockerfiles
docker run --rm -i hadolint/hadolint < <addon>/Dockerfile

# Shell scripts
shellcheck $(find . -name '*.sh')
```

CI runs the same checks on every push and PR (`.github/workflows/lint.yml`).

### Build Locally

The `home-assistant/builder` action can be invoked manually, or you can build directly:

```sh
docker build \
  --build-arg BUILD_FROM=lscr.io/linuxserver/sonarr:4.0.17.2952-ls309 \
  -t local/sonarr ./sonarr
```

## Pull Requests

1. Fork and create a branch off `main`.
2. Keep changes focused — one add-on or one concern per PR is easier to review.
3. Update the add-on `CHANGELOG.md` and bump `version` in `config.yaml` if user-visible behaviour changes.
4. Make sure `lint` CI passes.
5. Use the [PR template](.github/PULL_REQUEST_TEMPLATE.md) — it's prefilled when you open a PR.

## Versioning

- Add-ons that wrap LinuxServer.io images use the upstream version directly.
- Custom add-ons (e.g. Seerr) follow `<upstream>.<addon-patch>` — the 4th component is bumped when this repo ships a fix without an upstream change.
- A scheduled GitHub Action bumps versions daily — see `.github/scripts/update_versions.py`.

## Code of Conduct

Be excellent to each other. Personal attacks, harassment, or discriminatory behaviour are not tolerated. Maintainers may close issues or PRs that violate this expectation.
