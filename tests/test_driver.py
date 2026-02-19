"""Smoke test for driver creation — requires a browser installed, no OSW instance."""

from __future__ import annotations

import pytest

from osw_selenium.config import OSWConfig
from osw_selenium.driver import create_driver


def test_create_driver_invalid_browser():
    config = OSWConfig(browser="opera")
    with pytest.raises(ValueError, match="Unsupported browser"):
        create_driver(config)
