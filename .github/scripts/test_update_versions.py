import importlib.util
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

    @patch.object(update_versions.time, "sleep")
    @patch.object(update_versions.requests, "get")
    def test_returns_false_after_exhausting_retries(self, mock_get, _mock_sleep):
        mock_get.side_effect = [Mock(status_code=500) for _ in range(update_versions.MAX_RETRIES)]
        self.assertFalse(update_versions.ghcr_tag_exists("seerr-team/seerr", "v3.3.0"))
        self.assertEqual(mock_get.call_count, update_versions.MAX_RETRIES)
