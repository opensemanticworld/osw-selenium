"""Integration tests for the login flow — requires a running OSW instance."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration


def test_login_standard(logged_in_driver, osw_config):
    """After login, the main page should be accessible."""
    logged_in_driver.get(osw_config.base_url.rstrip("/") + "/wiki/Main_Page")
    assert "Main Page" in logged_in_driver.page_source
