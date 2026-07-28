import importlib.util
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch


SCRIPT_PATH = Path(__file__).with_name("update_versions.py")
SPEC = importlib.util.spec_from_file_location("update_versions", SCRIPT_PATH)
update_versions = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(update_versions)


class TestGhcrTagExists(TestCase):
    @patch.object(update_versions.requests, "get")
    def test_returns_true_when_manifest_exists(self, mock_get):
        mock_get.return_value = Mock(status_code=200)
        self.assertTrue(update_versions.ghcr_tag_exists("seerr-team/seerr", "v3.3.0"))

    @patch.object(update_versions.requests, "get")
    def test_returns_false_when_manifest_missing(self, mock_get):
        mock_get.return_value = Mock(status_code=404)
        self.assertFalse(update_versions.ghcr_tag_exists("seerr-team/seerr", "v3.3.0"))

    @patch.object(update_versions.time, "sleep")
    @patch.object(update_versions.requests, "get")
    def test_retries_transient_errors(self, mock_get, _mock_sleep):
        mock_get.side_effect = [Mock(status_code=500), Mock(status_code=200)]
        self.assertTrue(update_versions.ghcr_tag_exists("seerr-team/seerr", "v3.3.0"))


# Tags that a single nightly/develop build cycle publishes.  None of these are
# releases, but they are what floods the first page of Docker Hub results.
NIGHTLY_TAGS = [
    "2.6.1-nightly", "nightly-version-2.6.1.5496", "nightly-2.6.1.5496-ls8",
    "nightly", "arm64v8-2.6.1-nightly", "amd64-2.6.1-nightly",
    "2.6.0-develop", "develop-version-2.6.0.5494", "develop-2.6.0.5494-ls269",
]
# Tags published for the stable 2.5.2.5491 release.
RELEASE_TAGS = [
    "2.5.2", "version-2.5.2.5491", "2.5.2.5491-ls155",
    "arm64v8-2.5.2", "amd64-2.5.2.5491-ls155",
]


def _page(tags, next_url=None):
    """Build a fake Docker Hub tag-listing response."""
    return Mock(json=Mock(return_value={
        "results": [{"name": t} for t in tags],
        "next": next_url,
    }))


class TestFetchLatestVersionPagination(TestCase):
    @patch.object(update_versions, "get_with_retry")
    def test_follows_next_page_when_release_is_not_on_first_page(self, mock_get):
        """A release pushed off page 1 by nightly builds must still be found."""
        mock_get.side_effect = [
            _page(NIGHTLY_TAGS, next_url="https://hub.docker.com/page2"),
            _page(RELEASE_TAGS, next_url=None),
        ]
        self.assertEqual(
            update_versions.fetch_latest_version("prowlarr"),
            ("2.5.2.5491", "2.5.2.5491-ls155"),
        )

    @patch.object(update_versions, "get_with_retry")
    def test_reads_one_more_page_when_a_release_straddles_the_boundary(self, mock_get):
        """The tags of one release can be split across two pages.

        Stopping at the first page carrying a release would yield the coarse
        '2.5.2' alias instead of the precise '2.5.2.5491' build version.
        """
        mock_get.side_effect = [
            _page(NIGHTLY_TAGS + ["2.5.2"], next_url="https://hub.docker.com/page2"),
            _page(["version-2.5.2.5491", "2.5.2.5491-ls155"],
                  next_url="https://hub.docker.com/page3"),
        ]
        self.assertEqual(
            update_versions.fetch_latest_version("prowlarr"),
            ("2.5.2.5491", "2.5.2.5491-ls155"),
        )
        self.assertEqual(mock_get.call_count, 2)

    @patch.object(update_versions, "get_with_retry")
    def test_does_not_page_indefinitely_once_a_release_is_found(self, mock_get):
        """One extra page is enough — never walk the whole tag history."""
        mock_get.return_value = _page(
            RELEASE_TAGS, next_url="https://hub.docker.com/next")
        self.assertEqual(
            update_versions.fetch_latest_version("prowlarr"),
            ("2.5.2.5491", "2.5.2.5491-ls155"),
        )
        self.assertEqual(mock_get.call_count, 2)

    @patch.object(update_versions, "get_with_retry")
    def test_stops_after_max_pages_when_no_release_is_ever_found(self, mock_get):
        """An endless nightly stream must not page forever."""
        mock_get.return_value = _page(NIGHTLY_TAGS, next_url="https://hub.docker.com/next")
        self.assertIsNone(update_versions.fetch_latest_version("prowlarr"))
        self.assertEqual(mock_get.call_count, update_versions.MAX_TAG_PAGES)

    @patch.object(update_versions, "get_with_retry")
    def test_returns_none_when_pages_run_out(self, mock_get):
        mock_get.side_effect = [_page(NIGHTLY_TAGS, next_url=None)]
        self.assertIsNone(update_versions.fetch_latest_version("prowlarr"))


class TestIsDowngrade(TestCase):
    def test_older_version_is_a_downgrade(self):
        self.assertTrue(update_versions.is_downgrade("2.4.0.5397", "2.5.2.5491"))

    def test_newer_version_is_not_a_downgrade(self):
        self.assertFalse(update_versions.is_downgrade("2.5.2.5491", "2.4.0.5397"))

    def test_same_version_is_not_a_downgrade(self):
        self.assertFalse(update_versions.is_downgrade("2.5.2.5491", "2.5.2.5491"))

    def test_unparseable_current_version_is_not_a_downgrade(self):
        self.assertFalse(update_versions.is_downgrade("2.5.2.5491", "not-a-version"))


class TestIsLocalPatchOf(TestCase):
    """Add-on fixes ship as <upstream>.<n> without waiting for an upstream release."""

    def test_extra_component_is_a_local_patch(self):
        self.assertTrue(
            update_versions.is_local_patch_of("2.5.2.5491.1", "2.5.2.5491"))

    def test_identical_version_is_not_a_patch(self):
        self.assertFalse(
            update_versions.is_local_patch_of("2.5.2.5491", "2.5.2.5491"))

    def test_newer_upstream_is_not_a_patch(self):
        self.assertFalse(
            update_versions.is_local_patch_of("2.6.0.5500", "2.5.2.5491"))

    def test_unrelated_prefix_is_not_a_patch(self):
        """'1.6.0' must not look like a local patch of '1.6'."""
        self.assertFalse(update_versions.is_local_patch_of("1.60.1", "1.6"))


class MainTestCase(TestCase):
    """Runs main() against a throwaway repo containing a single LSIO add-on."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / ".github").mkdir()
        self.addon_dir = self.root / "prowlarr"
        self.addon_dir.mkdir()
        self.config_yaml = self.addon_dir / "config.yaml"
        self.build_yaml = self.addon_dir / "build.yaml"
        self.config_yaml.write_text('---\nname: Prowlarr\nversion: "2.5.2.5491"\n')
        self.build_yaml.write_text(
            "---\nbuild_from:\n"
            "  amd64: lscr.io/linuxserver/prowlarr:2.5.2.5491-ls155\n"
        )
        (self.addon_dir / "CHANGELOG.md").write_text("# Changelog\n\n")
        patches = [
            patch.object(update_versions, "ROOT", self.root),
            patch.object(update_versions, "LSIO_ADDONS", ["prowlarr"]),
            patch.object(update_versions, "GITHUB_ADDONS", {}),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        self.addCleanup(self._tmp.cleanup)


class TestMainFailsLoudly(MainTestCase):
    @patch.object(update_versions, "fetch_latest_version", return_value=None)
    def test_returns_nonzero_when_no_version_can_be_resolved(self, _mock_fetch):
        """A silent 'no versions found' is what let Prowlarr go stale unnoticed."""
        self.assertEqual(update_versions.main(), 1)

    @patch.object(update_versions, "fetch_latest_version",
                  return_value=("2.5.2.5491", "2.5.2.5491-ls155"))
    def test_returns_zero_when_already_up_to_date(self, _mock_fetch):
        self.assertEqual(update_versions.main(), 0)

    @patch.object(update_versions, "fetch_latest_version",
                  return_value=("2.6.0.5500", "2.6.0.5500-ls160"))
    def test_returns_zero_and_writes_when_upstream_is_newer(self, _mock_fetch):
        self.assertEqual(update_versions.main(), 0)
        self.assertIn('version: "2.6.0.5500"', self.config_yaml.read_text())
        self.assertIn("prowlarr:2.6.0.5500-ls160", self.build_yaml.read_text())


class TestMainKeepsLocalPatch(MainTestCase):
    def setUp(self):
        super().setUp()
        self.config_yaml.write_text('---\nname: Prowlarr\nversion: "2.5.2.5491.1"\n')

    @patch.object(update_versions, "fetch_latest_version",
                  return_value=("2.5.2.5491", "2.5.2.5491-ls155"))
    def test_local_patch_is_not_treated_as_a_downgrade(self, _mock_fetch):
        """Otherwise every daily run goes red until upstream happens to release."""
        self.assertEqual(update_versions.main(), 0)
        self.assertIn('version: "2.5.2.5491.1"', self.config_yaml.read_text())

    @patch.object(update_versions, "fetch_latest_version",
                  return_value=("2.6.0.5500", "2.6.0.5500-ls160"))
    def test_real_upstream_release_resets_the_patch(self, _mock_fetch):
        self.assertEqual(update_versions.main(), 0)
        self.assertIn('version: "2.6.0.5500"', self.config_yaml.read_text())


class TestMainRefusesDowngrade(MainTestCase):
    @patch.object(update_versions, "fetch_latest_version",
                  return_value=("2.4.0.5397", "2.4.0.5397-ls150"))
    def test_returns_nonzero_and_leaves_files_untouched(self, _mock_fetch):
        """A rebuilt old tag must never roll a working add-on backwards."""
        self.assertEqual(update_versions.main(), 1)
        self.assertIn('version: "2.5.2.5491"', self.config_yaml.read_text())
        self.assertIn("prowlarr:2.5.2.5491-ls155", self.build_yaml.read_text())


class TestMainGithubSourcedAddon(TestCase):
    """Same loud-failure contract for GitHub-release based add-ons (Seerr)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / ".github").mkdir()
        addon_dir = self.root / "seerr"
        addon_dir.mkdir()
        self.config_yaml = addon_dir / "config.yaml"
        self.config_yaml.write_text('---\nname: Seerr\nversion: "3.3.0.1"\n')
        (addon_dir / "build.yaml").write_text(
            "---\nbuild_from:\n  amd64: ghcr.io/seerr-team/seerr:v3.3.0\n"
        )
        (addon_dir / "CHANGELOG.md").write_text("# Changelog\n\n")
        patches = [
            patch.object(update_versions, "ROOT", self.root),
            patch.object(update_versions, "LSIO_ADDONS", []),
            patch.object(update_versions, "GITHUB_ADDONS", {"seerr": "seerr-team/seerr"}),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        self.addCleanup(self._tmp.cleanup)

    @patch.object(update_versions, "fetch_latest_github_release", return_value=None)
    def test_returns_nonzero_when_release_cannot_be_fetched(self, _mock_fetch):
        self.assertEqual(update_versions.main(), 1)

    @patch.object(update_versions, "ghcr_tag_exists", return_value=False)
    @patch.object(update_versions, "fetch_latest_github_release", return_value="3.4.0")
    def test_returns_zero_when_image_is_not_published_yet(self, _mock_fetch, _mock_ghcr):
        """Upstream tagging a release before its image builds is normal, not a failure."""
        self.assertEqual(update_versions.main(), 0)
        self.assertIn('version: "3.3.0.1"', self.config_yaml.read_text())

