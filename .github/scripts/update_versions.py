#!/usr/bin/env python3
"""
Auto-update add-on versions from LinuxServer.io Docker Hub tags.

Rules:
- For each add-on folder, read build.yaml to know the upstream LSIO image.
- Query Docker Hub for tags and pick the newest semver-style tag that is NOT
  'latest', 'develop', 'nightly' or an '-ls<number>' suffix-only tag.
- Keep the most recent production tag (e.g. 4.0.10 or 4.0.10.2544).
- Update config.yaml `version:` and build.yaml `build_from:` entries.
- Prepend a CHANGELOG.md entry on change.
- Write a summary file for the workflow to use in the commit message.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

import requests
import yaml
from packaging.version import InvalidVersion, Version

ROOT = Path(__file__).resolve().parents[2]
ADDONS = ["sonarr", "radarr", "bazarr", "prowlarr"]  # seerr uses non-LSIO image, skipped
DOCKERHUB_URL = (
    "https://hub.docker.com/v2/repositories/linuxserver/{image}/tags"
    "?page_size=100&ordering=last_updated"
)

# Ignore tags like "latest", "develop", "nightly", and dated/develop tags.
SKIP_TAGS = {"latest", "develop", "nightly", "arm32v7-latest", "arm64v8-latest",
             "amd64-latest"}
# Accept tags like "4.0.10", "4.0.10.2544", "5.11.0.9244-ls253"
TAG_RE = re.compile(r"^(?P<ver>\d+(?:\.\d+){1,3})(?:-ls\d+)?$")


def get_lsio_image(build_yaml: Path) -> Optional[str]:
    data = yaml.safe_load(build_yaml.read_text())
    for arch, ref in (data.get("build_from") or {}).items():
        # ref: lscr.io/linuxserver/sonarr:4.0.10
        if "linuxserver/" in ref:
            image = ref.split("linuxserver/", 1)[1].split(":", 1)[0]
            return image
    return None


def fetch_latest_version(image: str) -> Optional[str]:
    url = DOCKERHUB_URL.format(image=image)
    versions: list[tuple[Version, str]] = []
    while url:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        for item in payload.get("results", []):
            name = item.get("name", "")
            if name in SKIP_TAGS:
                continue
            m = TAG_RE.match(name)
            if not m:
                continue
            ver_str = m.group("ver")
            try:
                versions.append((Version(ver_str), ver_str))
            except InvalidVersion:
                continue
        url = payload.get("next")
        # Safety: cap pagination
        if len(versions) > 500:
            break
    if not versions:
        return None
    versions.sort(key=lambda x: x[0], reverse=True)
    return versions[0][1]


def update_build_yaml(path: Path, image: str, new_version: str) -> bool:
    raw = path.read_text()
    new_raw = re.sub(
        rf"(lscr\.io/linuxserver/{re.escape(image)}):[^\s\"']+",
        rf"\1:{new_version}",
        raw,
    )
    if new_raw != raw:
        path.write_text(new_raw)
        return True
    return False


def update_config_yaml(path: Path, new_version: str) -> tuple[bool, str]:
    raw = path.read_text()
    match = re.search(r'^version:\s*"?([^"\n]+)"?\s*$', raw, flags=re.MULTILINE)
    old_version = match.group(1) if match else "?"
    new_raw = re.sub(
        r'^version:\s*"?[^"\n]+"?\s*$',
        f'version: "{new_version}"',
        raw,
        flags=re.MULTILINE,
    )
    if new_raw != raw:
        path.write_text(new_raw)
        return True, old_version
    return False, old_version


def prepend_changelog(path: Path, version: str, image: str) -> None:
    header = f"## {version}\n\n- Bumped LinuxServer.io `{image}` to `{version}` (auto-update).\n\n"
    existing = path.read_text() if path.exists() else "# Changelog\n\n"
    # Put new entry just after the top "# Changelog" line
    if existing.startswith("# Changelog"):
        parts = existing.split("\n", 1)
        new_content = parts[0] + "\n\n" + header + (parts[1].lstrip("\n") if len(parts) > 1 else "")
    else:
        new_content = "# Changelog\n\n" + header + existing
    path.write_text(new_content)


def main() -> int:
    summary_lines: list[str] = []
    changed_any = False

    for addon in ADDONS:
        addon_dir = ROOT / addon
        build_yaml = addon_dir / "build.yaml"
        config_yaml = addon_dir / "config.yaml"
        changelog = addon_dir / "CHANGELOG.md"
        if not build_yaml.exists() or not config_yaml.exists():
            print(f"[skip] {addon}: missing build.yaml or config.yaml")
            continue

        image = get_lsio_image(build_yaml)
        if not image:
            print(f"[skip] {addon}: no LinuxServer.io image detected")
            continue

        latest = fetch_latest_version(image)
        if not latest:
            print(f"[warn] {addon}: no versions found for {image}")
            continue

        cfg_changed, old_ver = update_config_yaml(config_yaml, latest)
        bld_changed = update_build_yaml(build_yaml, image, latest)

        if cfg_changed or bld_changed:
            prepend_changelog(changelog, latest, image)
            summary_lines.append(f"- **{addon}**: {old_ver} → {latest}")
            changed_any = True
            print(f"[update] {addon}: {old_ver} -> {latest}")
        else:
            print(f"[ok] {addon}: already at {latest}")

    summary_path = ROOT / ".github" / ".update_summary"
    summary_path.write_text("\n".join(summary_lines) if summary_lines else "")
    return 0 if changed_any or True else 1


if __name__ == "__main__":
    sys.exit(main())
