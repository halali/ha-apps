import importlib.util
from pathlib import Path
from unittest import TestCase


SCRIPT_PATH = Path(__file__).with_name("check_version_bump.py")
SPEC = importlib.util.spec_from_file_location("check_version_bump", SCRIPT_PATH)
check_version_bump = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(check_version_bump)

verdict = lambda **kw: check_version_bump.check_addon(**kw)


class TestImageAffectingPaths(TestCase):
    def test_recognises_files_that_go_into_the_image(self):
        for p in ("seerr/config.yaml", "seerr/build.yaml", "seerr/Dockerfile",
                  "seerr/rootfs/etc/nginx/http.d/seerr.conf"):
            self.assertTrue(check_version_bump.affects_image(p), p)

    def test_ignores_documentation(self):
        for p in ("seerr/README.md", "seerr/CHANGELOG.md", "README.md"):
            self.assertFalse(check_version_bump.affects_image(p), p)


class TestCheckAddon(TestCase):
    def test_accepts_a_normal_bump(self):
        self.assertIsNone(verdict(addon="seerr", base="3.3.0.10",
                                  head="3.3.0.11", image_changed=True))

    def test_rejects_a_version_that_went_backwards(self):
        """The 3.3.0.8 -> 3.3.0.5 slip: a revert took the bump with it."""
        msg = verdict(addon="seerr", base="3.3.0.8", head="3.3.0.5",
                      image_changed=True)
        self.assertIsNotNone(msg)
        self.assertIn("backwards", msg)

    def test_rejects_image_change_without_a_bump(self):
        msg = verdict(addon="seerr", base="3.3.0.10", head="3.3.0.10",
                      image_changed=True)
        self.assertIsNotNone(msg)
        self.assertIn("unchanged", msg)

    def test_allows_docs_only_change_without_a_bump(self):
        self.assertIsNone(verdict(addon="seerr", base="3.3.0.10",
                                  head="3.3.0.10", image_changed=False))

    def test_still_rejects_a_downgrade_on_a_docs_only_change(self):
        self.assertIsNotNone(verdict(addon="seerr", base="3.3.0.10",
                                     head="3.3.0.9", image_changed=False))

    def test_accepts_a_brand_new_addon(self):
        self.assertIsNone(verdict(addon="newthing", base=None,
                                  head="1.0.0", image_changed=True))

    def test_reports_unparseable_versions_instead_of_crashing(self):
        msg = verdict(addon="seerr", base="3.3.0.10", head="not-a-version",
                      image_changed=True)
        self.assertIsNotNone(msg)
        self.assertIn("not-a-version", msg)


class TestChangedAddons(TestCase):
    def test_groups_paths_by_addon_and_flags_image_changes(self):
        got = check_version_bump.group_changes([
            "seerr/config.yaml",
            "seerr/README.md",
            "radarr/README.md",
            "README.md",
            ".github/workflows/lint.yml",
        ])
        self.assertEqual(got, {"seerr": True, "radarr": False})
