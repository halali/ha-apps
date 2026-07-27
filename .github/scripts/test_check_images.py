import importlib.util
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch


SCRIPT_PATH = Path(__file__).with_name("check_images.py")
SPEC = importlib.util.spec_from_file_location("check_images", SCRIPT_PATH)
check_images = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(check_images)


CONFIG = """---
name: Prowlarr
version: "{version}"
slug: prowlarr
arch:
  - amd64
image: ghcr.io/halali/ha-apps-{{arch}}-prowlarr
"""


class TestImageRepository(TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.path = Path(self._tmp.name) / "config.yaml"

    def test_resolves_arch_placeholder_and_strips_registry(self):
        self.path.write_text(CONFIG.format(version="2.5.2.5491"))
        self.assertEqual(
            check_images.image_repository(self.path),
            "halali/ha-apps-amd64-prowlarr",
        )

    def test_handles_image_without_placeholder(self):
        self.path.write_text(
            '---\nversion: "1.0"\narch:\n  - amd64\n'
            "image: ghcr.io/halali/ha-apps-amd64-seerr\n"
        )
        self.assertEqual(
            check_images.image_repository(self.path),
            "halali/ha-apps-amd64-seerr",
        )

    def test_returns_none_when_image_is_absent(self):
        self.path.write_text('---\nversion: "1.0"\n')
        self.assertIsNone(check_images.image_repository(self.path))


class FindDriftTestCase(TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        addon = self.root / "prowlarr"
        addon.mkdir()
        (addon / "config.yaml").write_text(CONFIG.format(version="2.5.2.5491"))


class TestFindDrift(FindDriftTestCase):
    @patch.object(check_images, "published_tags",
                  return_value={"2.5.2.5491", "latest"})
    def test_reports_nothing_when_the_image_is_published(self, _tags):
        self.assertEqual(check_images.find_drift(self.root, ["prowlarr"]), [])

    @patch.object(check_images, "published_tags",
                  return_value={"2.3.5.5328", "latest"})
    def test_reports_the_addon_when_its_version_was_never_built(self, _tags):
        """The exact failure Home Assistant surfaces as '404 manifest unknown'."""
        drift = check_images.find_drift(self.root, ["prowlarr"])
        self.assertEqual(len(drift), 1)
        self.assertEqual(drift[0]["addon"], "prowlarr")
        self.assertEqual(drift[0]["version"], "2.5.2.5491")

    @patch.object(check_images, "published_tags", return_value=set())
    def test_reports_the_addon_when_no_image_exists_at_all(self, _tags):
        drift = check_images.find_drift(self.root, ["prowlarr"])
        self.assertEqual(len(drift), 1)

    @patch.object(check_images, "published_tags", return_value=None)
    def test_reports_the_addon_when_the_registry_cannot_be_queried(self, _tags):
        """Unknown is not the same as fine — never report a clean bill blindly."""
        drift = check_images.find_drift(self.root, ["prowlarr"])
        self.assertEqual(len(drift), 1)


class TestMain(FindDriftTestCase):
    def setUp(self):
        super().setUp()
        p = patch.object(check_images, "ROOT", self.root)
        p.start()
        self.addCleanup(p.stop)

    @patch.object(check_images, "published_tags",
                  return_value={"2.5.2.5491"})
    def test_returns_zero_when_every_addon_has_its_image(self, _tags):
        self.assertEqual(check_images.main(), 0)

    @patch.object(check_images, "published_tags",
                  return_value={"2.3.5.5328"})
    def test_returns_nonzero_when_any_addon_is_missing_its_image(self, _tags):
        self.assertEqual(check_images.main(), 1)


class TestPublishedTags(TestCase):
    @patch.object(check_images.requests, "get")
    def test_returns_tag_set(self, mock_get):
        mock_get.side_effect = [
            Mock(status_code=200, json=Mock(return_value={"token": "t"})),
            Mock(status_code=200,
                 json=Mock(return_value={"tags": ["1.0", "latest"]})),
        ]
        self.assertEqual(check_images.published_tags("halali/x"), {"1.0", "latest"})

    @patch.object(check_images.requests, "get")
    def test_returns_empty_set_for_unknown_repository(self, mock_get):
        mock_get.side_effect = [
            Mock(status_code=200, json=Mock(return_value={"token": "t"})),
            Mock(status_code=404, json=Mock(return_value={})),
        ]
        self.assertEqual(check_images.published_tags("halali/x"), set())

    @patch.object(check_images.requests, "get")
    def test_treats_403_as_not_published(self, mock_get):
        """GHCR answers 403 for a package that was never pushed publicly.

        Home Assistant pulls anonymously too, so 403 means exactly as broken
        as 404 — reporting it as 'could not query' would misdiagnose it.
        """
        mock_get.side_effect = [
            Mock(status_code=200, json=Mock(return_value={"token": "t"})),
            Mock(status_code=403, json=Mock(return_value={})),
        ]
        self.assertEqual(check_images.published_tags("halali/x"), set())

    @patch.object(check_images.requests, "get")
    def test_returns_none_when_the_registry_errors(self, mock_get):
        mock_get.side_effect = [
            Mock(status_code=200, json=Mock(return_value={"token": "t"})),
            Mock(status_code=500, json=Mock(return_value={})),
        ]
        self.assertIsNone(check_images.published_tags("halali/x"))
