#!/usr/bin/env python3
"""
Verify that a changed add-on's version actually moves forward.

Home Assistant only offers an update when config.yaml carries a higher version,
and the Builder tags the published image with whatever it finds there. So a
version that stands still republishes an existing tag with different contents,
and a version that goes backwards leaves the fix unreachable — in both cases the
build is green and nothing looks wrong.

Both happened in this repository: a revert took a version bump with it, the
follow-up edit no longer matched, and the rebuilt image was pushed over an
existing tag while Home Assistant kept offering nothing.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Optional

import yaml
from packaging.version import InvalidVersion, Version

ROOT = Path(__file__).resolve().parents[2]
# Everything the Builder puts into the image. Docs are deliberately excluded so
# fixing a typo in a README does not demand a version bump.
IMAGE_PATHS = ("config.yaml", "build.yaml", "Dockerfile", "rootfs/")


def affects_image(path: str) -> bool:
    """True when a repo-relative path is baked into an add-on image."""
    parts = path.split("/", 1)
    if len(parts) != 2:
        return False
    rest = parts[1]
    return any(rest == p or rest.startswith(p) for p in IMAGE_PATHS)


def group_changes(paths: list[str]) -> dict[str, bool]:
    """Map each touched add-on to whether its image contents changed."""
    addons: dict[str, bool] = {}
    for path in paths:
        top = path.split("/", 1)[0]
        if not (ROOT / top / "config.yaml").exists():
            continue
        addons[top] = addons.get(top, False) or affects_image(path)
    return addons


def check_addon(addon: str, base: Optional[str], head: str,
                image_changed: bool) -> Optional[str]:
    """Return a complaint about this add-on's version, or None when it is fine."""
    if base is None:
        return None  # newly added add-on, nothing to compare against

    try:
        head_v, base_v = Version(head), Version(base)
    except InvalidVersion:
        return f"{addon}: cannot compare versions {base!r} -> {head!r}"

    if head_v < base_v:
        return (f"{addon}: version went backwards, {base} -> {head}. "
                f"Home Assistant will not offer it and the older image tag stays.")
    if image_changed and head_v == base_v:
        return (f"{addon}: image contents changed but the version is unchanged "
                f"({head}). The Builder would republish tag {head} with different "
                f"contents and Home Assistant would offer no update.")
    return None


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout


def version_at(ref: str, addon: str) -> Optional[str]:
    """Read an add-on's version as of a git ref, or None if it did not exist."""
    try:
        raw = git("show", f"{ref}:{addon}/config.yaml")
    except subprocess.CalledProcessError:
        return None
    data = yaml.safe_load(raw) or {}
    version = data.get("version")
    return str(version) if version is not None else None


def main() -> int:
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "HEAD~1"
    changed = git("diff", "--name-only", base_ref, "HEAD").split()
    addons = group_changes(changed)

    if not addons:
        print("No add-on changes to check.")
        return 0

    problems = []
    for addon, image_changed in sorted(addons.items()):
        head = version_at("HEAD", addon)
        base = version_at(base_ref, addon)
        if head is None:
            continue
        complaint = check_addon(addon, base, head, image_changed)
        if complaint:
            problems.append(complaint)
            print(f"::error::{complaint}")
        else:
            what = "image" if image_changed else "docs"
            print(f"[ok] {addon}: {base} -> {head} ({what} changed)")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
