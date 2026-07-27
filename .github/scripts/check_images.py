#!/usr/bin/env python3
"""
Verify that every add-on's config.yaml version has a matching image on GHCR.

Home Assistant reads the version straight from config.yaml and then pulls
`<image>:<version>`.  When a version is bumped but no image is published, the
supervisor offers an update that fails with "[404] manifest unknown" — the
add-on looks upgradeable but cannot be installed.

That drift is invisible in the repository itself, so it is checked here and
reported as a failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Optional

import requests
import yaml

ROOT = Path(__file__).resolve().parents[2]
GHCR_TOKEN_URL = "https://ghcr.io/token?scope=repository:{repo}:pull&service=ghcr.io"
GHCR_TAGS_URL = "https://ghcr.io/v2/{repo}/tags/list"


def discover_addons(root: Path) -> list[str]:
    """Every top-level directory holding a config.yaml is an add-on."""
    return sorted(p.parent.name for p in root.glob("*/config.yaml"))


def image_repository(config_yaml: Path) -> Optional[str]:
    """Return the GHCR repository path an add-on publishes to.

    'ghcr.io/halali/ha-apps-{arch}-prowlarr' -> 'halali/ha-apps-amd64-prowlarr'
    """
    data = yaml.safe_load(config_yaml.read_text()) or {}
    image = data.get("image")
    if not image:
        return None
    arches = data.get("arch") or ["amd64"]
    image = image.replace("{arch}", arches[0])
    return re.sub(r"^ghcr\.io/", "", image)


def published_tags(repo: str) -> Optional[set[str]]:
    """Return the tags published for a GHCR repository.

    An empty set means the repository exists but has no tags (or is unknown);
    None means the registry could not be asked and the answer is unknown — the
    caller must not read that as "everything is fine".
    """
    try:
        token_resp = requests.get(GHCR_TOKEN_URL.format(repo=repo), timeout=30)
        token = token_resp.json().get("token", "")
        resp = requests.get(
            GHCR_TAGS_URL.format(repo=repo),
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
    except requests.RequestException as exc:
        print(f"[warn] could not query ghcr.io/{repo}: {exc}")
        return None

    # 403 is what GHCR returns for a package that was never pushed publicly.
    # Home Assistant pulls anonymously as well, so it is as unusable as a 404.
    if resp.status_code in (403, 404):
        return set()
    if resp.status_code != 200:
        print(f"[warn] unexpected HTTP {resp.status_code} from ghcr.io/{repo}")
        return None
    return set(resp.json().get("tags") or [])


def find_drift(root: Path, addons: list[str]) -> list[dict[str, str]]:
    """Return one entry per add-on whose config version has no published image."""
    drift: list[dict[str, str]] = []
    for addon in addons:
        config_yaml = root / addon / "config.yaml"
        if not config_yaml.exists():
            continue
        data = yaml.safe_load(config_yaml.read_text()) or {}
        version = str(data.get("version", ""))
        repo = image_repository(config_yaml)
        if not repo or not version:
            print(f"[skip] {addon}: no image or version in config.yaml")
            continue

        tags = published_tags(repo)
        if tags is None:
            drift.append({"addon": addon, "version": version, "image": repo,
                          "reason": "registry could not be queried"})
            continue
        if version not in tags:
            newest = max(tags - {"latest"}, default="none")
            drift.append({"addon": addon, "version": version, "image": repo,
                          "reason": f"no image for this version (newest built: {newest})"})
        else:
            print(f"[ok] {addon}: {repo}:{version} is published")
    return drift


def main() -> int:
    addons = discover_addons(ROOT)
    drift = find_drift(ROOT, addons)
    if not drift:
        print(f"\nAll {len(addons)} add-ons have a published image.")
        return 0

    print()
    for item in drift:
        print(f"::error::{item['addon']} {item['version']}: {item['reason']} "
              f"— Home Assistant will fail to install it (404 manifest unknown)")
    print(f"\n{len(drift)} add-on(s) advertise a version that was never built.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
