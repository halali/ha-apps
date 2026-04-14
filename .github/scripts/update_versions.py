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
import time
from pathlib import Path
from typing import Optional

import requests
import yaml
from packaging.version import InvalidVersion, Version


def get_with_retry(url: str, max_retries: int = 3, timeout: int = 30) -> requests.Response:
    """GET with exponential backoff on 429 / 5xx."""
    for attempt in range(max_retries):
        resp = requests.get(url, timeout=timeout)
        if resp.status_code == 429 or resp.status_code >= 500:
            wait = 2 ** attempt * 5  # 5s, 10s, 20s
            print(f"[warn] HTTP {resp.status_code} from {url} — retrying in {wait}s")
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp
    resp.raise_for_status()
    return resp

ROOT = Path(__file__).resolve().parents[2]
LSIO_ADDONS = ["sonarr", "radarr", "bazarr", "prowlarr"]
GITHUB_ADDONS = {
    "seerr": "seerr-team/seerr",
}
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


def fetch_latest_version(image: str) -> Optional[tuple[str, str]]:
    """Return (version_for_config, docker_tag_for_build) for the latest release.

    Fetches only the first page (100 tags, ordered by last_updated desc).
    The newest release is always in the first page — no pagination needed.

    Some LSIO images only publish full tags like '2.3.5.5327-ls141' without a
    short '2.3.5.5327' alias.  We use the clean version in config.yaml but must
    use the actual published tag in build.yaml.  Prefer the short tag when it
    exists; fall back to the full '-ls' tag otherwise.
    """
    url = DOCKERHUB_URL.format(image=image)
    version_tags: dict[str, list[str]] = {}
    resp = get_with_retry(url)
    for item in resp.json().get("results", []):
        name = item.get("name", "")
        if name in SKIP_TAGS:
            continue
        m = TAG_RE.match(name)
        if not m:
            continue
        ver_str = m.group("ver")
        try:
            Version(ver_str)
        except InvalidVersion:
            continue
        version_tags.setdefault(ver_str, []).append(name)
    if not version_tags:
        return None
    latest_ver = max(version_tags.keys(), key=lambda v: Version(v))
    tags = version_tags[latest_ver]
    # Prefer the short tag (no -ls suffix) when it exists
    short = [t for t in tags if not re.search(r"-ls\d+$", t)]
    docker_tag = short[0] if short else tags[0]
    return latest_ver, docker_tag


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


def fetch_latest_github_release(repo: str) -> Optional[str]:
    """Return the latest semver tag from a GitHub repo (strips leading 'v')."""
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    tag = resp.json().get("tag_name", "")
    ver_str = tag.lstrip("v")
    try:
        Version(ver_str)
        return ver_str
    except InvalidVersion:
        return None


def update_github_build_yaml(path: Path, repo: str, new_version: str) -> bool:
    """Update the ghcr.io image tag in build.yaml for a GitHub-sourced addon."""
    owner = repo.split("/")[1]
    raw = path.read_text()
    new_raw = re.sub(
        rf"(ghcr\.io/{re.escape(repo.split('/')[0])}/{re.escape(owner)}):[^\s\"']+",
        rf"\1:v{new_version}",
        raw,
    )
    if new_raw != raw:
        path.write_text(new_raw)
        return True
    return False


def main() -> int:
    summary_lines: list[str] = []
    changed_any = False

    for addon in LSIO_ADDONS:
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

        result = fetch_latest_version(image)
        if not result:
            print(f"[warn] {addon}: no versions found for {image}")
            continue
        latest, docker_tag = result

        cfg_changed, old_ver = update_config_yaml(config_yaml, latest)
        bld_changed = update_build_yaml(build_yaml, image, docker_tag)

        if cfg_changed or bld_changed:
            prepend_changelog(changelog, latest, image)
            summary_lines.append(f"- **{addon}**: {old_ver} → {latest}")
            changed_any = True
            print(f"[update] {addon}: {old_ver} -> {latest}")
        else:
            print(f"[ok] {addon}: already at {latest}")

    # GitHub-release based addons (e.g. Seerr)
    # Versioning scheme: <upstream>.<addon_patch> e.g. "3.1.1.1"
    # The 4th component is a local addon patch counter and is reset when
    # upstream bumps. We only update when upstream releases a newer version
    # than the upstream base already tracked (first 3 components).
    for addon, repo in GITHUB_ADDONS.items():
        addon_dir = ROOT / addon
        build_yaml = addon_dir / "build.yaml"
        config_yaml = addon_dir / "config.yaml"
        if not build_yaml.exists() or not config_yaml.exists():
            print(f"[skip] {addon}: missing build.yaml or config.yaml")
            continue

        latest = fetch_latest_github_release(repo)
        if not latest:
            print(f"[warn] {addon}: could not fetch latest release from {repo}")
            continue

        # Read current version and strip optional 4th addon-patch component
        raw_cfg = config_yaml.read_text()
        m = re.search(r'^version:\s*"?([^"\n]+)"?\s*$', raw_cfg, flags=re.MULTILINE)
        current_full = m.group(1) if m else "0"
        parts = current_full.split(".")
        current_upstream = ".".join(parts[:3])  # e.g. "3.1.1" from "3.1.1.1"

        try:
            upstream_newer = Version(latest) > Version(current_upstream)
        except InvalidVersion:
            upstream_newer = False

        if not upstream_newer:
            print(f"[ok] {addon}: upstream still at {latest} (addon is {current_full})")
            continue

        # Upstream has a new release — reset addon patch, set to bare upstream version
        cfg_changed, old_ver = update_config_yaml(config_yaml, latest)
        bld_changed = update_github_build_yaml(build_yaml, repo, latest)

        if cfg_changed or bld_changed:
            summary_lines.append(f"- **{addon}**: {old_ver} → {latest}")
            changed_any = True
            print(f"[update] {addon}: {old_ver} -> {latest}")

    summary_path = ROOT / ".github" / ".update_summary"
    summary_path.write_text("\n".join(summary_lines) if summary_lines else "")
    return 0 if changed_any or True else 1


if __name__ == "__main__":
    sys.exit(main())
